import re
import csv
import json
import sqlite3
import subprocess
from pathlib import Path
from typing import Dict, List, Any

DB_PATH = "/home/izi-system/Documents/Vana_BOMAutomation/data/vana_catalog.db"

class SpecExtractorEngine:
    """
    Automated tool for:
    1. Requirement Extraction from unstructured RFP text / PDF specs.
    2. Compliance Categorization (Technical, Operational, Commercial, Quality/Inspection, Legal).
    3. Actionable Deliverable List Generation (Hardware Deliverables, Testing Deliverables, Document Submissions).
    4. Auto-Mapping to VANA Component Catalog & Gap/Risk Identification.
    """

    CATEGORIES = {
        "TECHNICAL_HARDWARE": [
            r"propeller|prop\b|prop set", r"motor|bldc|kv", r"esc\b|speed controller",
            r"flight controller|autopilot|pixhawk|cube", r"battery|lipo|li-ion|mah|cell",
            r"camera|payload|gimbal|eo|ir|lwir|thermal|lrf", r"frame|airframe|carbon",
            r"antenna|rf|mimo", r"gps|gnss|rtk|navic", r"transmitter|receiver|gcs|datalink",
            r"hard case|transport case|box", r"tool set|tools|kit", r"charger|balance charger",
            r"release mechanism|ordnance|payload holder|drop"
        ],
        "OPERATIONAL_PERFORMANCE": [
            r"endurance|flight time|minutes|hours", r"range|km|los|bvlos",
            r"payload capacity|payload weight|gram|kg", r"altitude|amsl|operating height",
            r"wind resistance|speed|m/s|kmph", r"operating temperature|temp range|-?\d+\s?°c",
            r"ip\s?rating|ip65|ip67|ip54|ingress|weatherproof"
        ],
        "QUALITY_TESTING": [
            r"advance sample|sample clause|trial", r"fat\b|sat\b|acceptance test|atp\b",
            r"board of officers|inspection authority|inspection agency",
            r"pre-dispatch|post dispatch|stage-wise inspection",
            r"iso\s?9001|bis\s?licence|type test|qap\b"
        ],
        "LEGAL_REGULATORY": [
            r"china|chinese|land border", r"make in india|mii|class 1 local|local content",
            r"malicious code|backdoor|embedded", r"ipv6", r"non-disclosure|nda\b",
            r"residual market life|end-of-life|eol\b", r"arbitration|dpm"
        ],
        "COMMERCIAL_SLA": [
            r"warranty|guarantee", r"option clause|increase or decrease|percentage of bid",
            r"reverse auction|ra qualification", r"delivery period|days|consignee",
            r"training|operator training|commissioning", r"shelf life|years",
            r"service centre|functional service centre|toll free"
        ]
    }

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def extract_from_pdf(self, pdf_path: str) -> str:
        """Extracts text from PDF file using pdftotext."""
        cmd = ["pdftotext", pdf_path, "-"]
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            return res.stdout
        except Exception as e:
            raise RuntimeError(f"Failed to extract PDF text: {e}")

    def analyze_specification_text(self, text: str) -> Dict[str, Any]:
        """
        Parses technical specification text, classifies sentences/clauses,
        extracts numeric parameters, flags compliance requirements, and builds deliverable lists.
        """
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        
        extracted_requirements = []
        hardware_deliverables = []
        testing_deliverables = []
        document_deliverables = []
        critical_flags = []

        # Tracking set to avoid duplicates
        seen_deliverables = set()

        for line in lines:
            if len(line) < 5 or line.startswith("---") or line.startswith("=="):
                continue

            # Match against category regex patterns
            matched_cats = []
            for cat, patterns in self.CATEGORIES.items():
                for pat in patterns:
                    if re.search(pat, line, re.IGNORECASE):
                        matched_cats.append(cat)
                        break

            if not matched_cats:
                continue

            primary_cat = matched_cats[0]
            
            # Extract requirement
            req_item = {
                "raw_text": line,
                "category": primary_cat,
                "risk_level": "NORMAL"
            }

            # 1. Check for Strict Compliance & Risk Keywords
            if re.search(r"china|chinese|land border", line, re.IGNORECASE):
                req_item["risk_level"] = "CRITICAL"
                critical_flags.append({
                    "flag": "STRICT_NON_CHINESE",
                    "clause": line,
                    "action": "Ensure zero components originate from China. Use indigenous or western alternatives."
                })
                doc = "Non-Chinese Origin Undertaking Certificate (MoD Format)"
                if doc not in seen_deliverables:
                    document_deliverables.append({"name": doc, "type": "Statutory Certificate", "mandatory": True})
                    seen_deliverables.add(doc)

            if re.search(r"advance sample|sample approval", line, re.IGNORECASE):
                req_item["risk_level"] = "HIGH"
                qty_match = re.search(r"(\d+)\s*(?:samples|units)", line, re.IGNORECASE)
                days_match = re.search(r"within\s*(\d+)\s*days", line, re.IGNORECASE)
                sample_qty = qty_match.group(1) if qty_match else "3"
                sample_days = days_match.group(1) if days_match else "5"
                critical_flags.append({
                    "flag": "ADVANCE_SAMPLE_SUBMISSION",
                    "clause": line,
                    "action": f"Prepare {sample_qty} physical samples for submission within {sample_days} days of contract."
                })
                test_item = f"Advance Samples ({sample_qty} units within {sample_days} days) for Buyer Test"
                if test_item not in seen_deliverables:
                    testing_deliverables.append({"name": test_item, "type": "Physical Pre-Supply Test", "timeline": f"{sample_days} Days"})
                    seen_deliverables.add(test_item)

            if re.search(r"option clause|increase.*?quantity", line, re.IGNORECASE):
                pct_match = re.search(r"(\d+)\s*(?:percent|%)", line, re.IGNORECASE)
                pct = pct_match.group(1) if pct_match else "25"
                critical_flags.append({
                    "flag": "OPTION_CLAUSE_RISK",
                    "clause": line,
                    "action": f"Vendor prices must remain valid for +{pct}% additional repeat order at contract price."
                })

            if re.search(r"training", line, re.IGNORECASE) and not line.startswith("Searched String"):
                pers_match = re.search(r"(\d+)\s*(?:employees|personnel|operators)", line, re.IGNORECASE)
                days_match = re.search(r"(\d+)\s*days", line, re.IGNORECASE)
                testing_deliverables.append({
                    "name": f"Operator Training ({pers_match.group(1) if pers_match else 'Army'} Personnel, {days_match.group(1) if days_match else '10'} Days)",
                    "type": "Commissioning & Training",
                    "timeline": "Post Delivery"
                })

            if re.search(r"malicious code", line, re.IGNORECASE):
                doc = "Certificate on Absence of Embedded Malicious Code"
                if doc not in seen_deliverables:
                    document_deliverables.append({"name": doc, "type": "Cybersecurity Undertaking", "mandatory": True})
                    seen_deliverables.add(doc)

            if re.search(r"ipv6", line, re.IGNORECASE):
                doc = "IPv6 Ready Compliance Certificate"
                if doc not in seen_deliverables:
                    document_deliverables.append({"name": doc, "type": "Technical Specification Undertaking", "mandatory": True})
                    seen_deliverables.add(doc)

            if re.search(r"make in india|local supplier|local content", line, re.IGNORECASE):
                doc = "Class-1 Local Supplier Self-Declaration Certificate (Min 50% MII)"
                if doc not in seen_deliverables:
                    document_deliverables.append({"name": doc, "type": "Eligibility Certificate", "mandatory": True})
                    seen_deliverables.add(doc)

            # 2. Extract Hardware Deliverables
            hardware_keywords = [
                ("Airframe / Frame", r"\bframe\b|\bquad\b|\bhex\b"),
                ("Brushless Motors", r"brushless motor|bldc motor"),
                ("Propeller Set", r"propeller|prop set|folding prop"),
                ("Speed Controllers (ESC)", r"\besc\b|electronic speed controller"),
                ("Flight Controller / Autopilot", r"flight controller|autopilot"),
                ("EO/IR Camera Gimbal", r"camera|fpv camera|gimbal|payload|thermal|lwir"),
                ("GPS / Navigation Unit", r"gps module|gnss|rtk"),
                ("Battery Pack", r"battery pack|li-ion pack|lipo pack"),
                ("Radio Controller & GCS", r"radio controller|handheld gcs|transmitter"),
                ("Payload Release Mechanism", r"payload holder|release mechanism|ordnance release"),
                ("Field Battery Charger", r"battery charger|dual charger|fast charger"),
                ("Military Hard Case", r"hard case|transport case"),
                ("Tool Kit & Spares", r"tool set|tools|allied accessories"),
                ("Flight Logbook & Manual", r"log book|logbook|technical manual|user manual")
            ]

            for hw_name, hw_regex in hardware_keywords:
                if re.search(hw_regex, line, re.IGNORECASE) and not line.startswith("Searched String"):
                    if hw_name not in seen_deliverables:
                        qty_match = re.search(r"\b(\d+)\s*(?:nos|pcs|units|set|pieces)?\b", line, re.IGNORECASE)
                        hardware_deliverables.append({
                            "subsystem": hw_name,
                            "tender_ref": line[:90] + ("..." if len(line) > 90 else ""),
                            "source_clause": primary_cat
                        })
                        seen_deliverables.add(hw_name)

            extracted_requirements.append(req_item)

        # Fallback default required documentation for defence tenders
        default_docs = [
            ("PAN, GSTIN & EFT Mandate", "Vendor Financial KYC"),
            ("OEM Authorization Certificate (MAF)", "Manufacturer Authorization"),
            ("ISO 9001:2015 Quality Certificate", "Quality Accreditation"),
            ("3 Years Past Performance / CRAC Proofs", "Experience Eligibility"),
            ("Audited Balance Sheets (Last 3 Financial Years)", "Financial Eligibility")
        ]
        for d_name, d_type in default_docs:
            if d_name not in seen_deliverables:
                document_deliverables.append({"name": d_name, "type": d_type, "mandatory": True})
                seen_deliverables.add(d_name)

        return {
            "summary": {
                "total_requirements_analyzed": len(extracted_requirements),
                "hardware_deliverables_count": len(hardware_deliverables),
                "testing_deliverables_count": len(testing_deliverables),
                "document_deliverables_count": len(document_deliverables),
                "critical_risks_identified": len(critical_flags)
            },
            "critical_flags": critical_flags,
            "hardware_deliverables": hardware_deliverables,
            "testing_deliverables": testing_deliverables,
            "document_deliverables": document_deliverables,
            "categorized_requirements": extracted_requirements
        }

    def export_analysis_to_csv(self, analysis_result: Dict[str, Any], output_path: str):
        """Exports the extraction and deliverables into an Excel-ready CSV format."""
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["VANA DEFENCE & AEROSPACE — SPECIFICATION EXTRACTION & COMPLIANCE MATRIX"])
            writer.writerow([])
            
            # Critical Risks
            writer.writerow(["1. CRITICAL RED FLAGS & HIGH-RISK CLAUSES"])
            writer.writerow(["Risk Flag", "Action Required", "Clause Reference"])
            for cf in analysis_result["critical_flags"]:
                writer.writerow([cf["flag"], cf["action"], cf["clause"]])
            writer.writerow([])

            # Hardware Deliverables
            writer.writerow(["2. MANDATORY HARDWARE DELIVERABLES LIST"])
            writer.writerow(["Item #", "Subsystem / Deliverable", "Tender Specification Snippet", "Category"])
            for idx, hw in enumerate(analysis_result["hardware_deliverables"], 1):
                writer.writerow([idx, hw["subsystem"], hw["tender_ref"], hw["source_clause"]])
            writer.writerow([])

            # Testing Deliverables
            writer.writerow(["3. MANDATORY TESTING, INSPECTION & SLA DELIVERABLES"])
            writer.writerow(["Item #", "Test / Inspection Event", "Type", "Execution Timeline"])
            for idx, td in enumerate(analysis_result["testing_deliverables"], 1):
                writer.writerow([idx, td["name"], td["type"], td.get("timeline", "Scheduled")])
            writer.writerow([])

            # Document Deliverables
            writer.writerow(["4. MANDATORY BID SUBMISSION DOCUMENTS CHECKLIST"])
            writer.writerow(["Doc #", "Document Name", "Classification", "Mandatory?", "Verification Status"])
            for idx, doc in enumerate(analysis_result["document_deliverables"], 1):
                writer.writerow([idx, doc["name"], doc["type"], "YES" if doc.get("mandatory") else "OPTIONAL", "[ ] PENDING"])

        print(f"Extraction matrix successfully exported to: {output_path}")

if __name__ == "__main__":
    extractor = SpecExtractorEngine()
    sample_text = """
    BOQ Title: 10 Inch Ord Dropping Drone
    Item Category: Frame, Brushless Motors, 10 Inch Prop Set, Flight Controller, ESC, FPV Camera, VTX, GPS Module with Compass, Battery Pack, Dual Band Receiver, Radio Controller, Payload Holder with servo Release Mechanism, Allied Accessories, Connectors, Cables, Tool Set, Hard Case, Log Book
    OPTION CLAUSE: The Purchaser reserves the right to increase or decrease the quantity to be ordered up to 25 percent of bid quantity.
    Sample Clause: After award of contract - Successful Bidder shall submit 3 samples for Buyer approval within 5 days.
    Undertaking Certificate: We hereby confirm that we shall not use any components, parts, material and product sourced from china for the manufacturing of drone.
    Malicious Code Certificate: Hardware and software being offered does not contain Embedded Malicious code.
    IT equipment shall be IPv6 ready from day one.
    Scope of supply includes Training: 5 employees to be trained at HQ 4 Arty Bde for duration of 10 days.
    """
    res = extractor.analyze_specification_text(sample_text)
    extractor.export_analysis_to_csv(res, "/home/izi-system/Documents/Vana_BOMAutomation/data/Extracted_Tender_Deliverables.csv")
