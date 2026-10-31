#!/usr/bin/env python3
import sys
import os
import json
import argparse
from pathlib import Path

# Add src to path
current_dir = Path(__file__).resolve().parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from spec_extractor import SpecExtractorEngine
from tender_engine import TenderRuleEngine

def main():
    parser = argparse.ArgumentParser(description="VANA Automated Tender & Spec Extraction CLI Tool")
    parser.add_argument("--pdf", type=str, help="Path to PDF tender or technical specification document")
    parser.add_argument("--text", type=str, help="Direct specification text string")
    parser.add_argument("--file", type=str, help="Text file containing specifications/clauses")
    parser.add_argument("--export-csv", type=str, default="Extracted_Tender_Deliverables.csv", help="CSV output filename")
    parser.add_argument("--qty", type=int, default=1, help="Quantity for BOM costing calculation")

    args = parser.parse_args()

    extractor = SpecExtractorEngine()
    engine = TenderRuleEngine()

    content = ""
    if args.pdf:
        print(f"[*] Extracting technical specifications from PDF: {args.pdf}")
        content = extractor.extract_from_pdf(args.pdf)
    elif args.file:
        print(f"[*] Reading specifications from file: {args.file}")
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
    elif args.text:
        content = args.text
    else:
        # Default sample if nothing supplied
        print("[*] No file supplied. Running with default Indian Army 10-Inch Ordnance Dropping Drone RFP...")
        content = """
        BOQ Title: 10 Inch Ord Dropping Drone
        Item Category: Frame, Brushless Motors, 10 Inch Prop Set, Flight Controller, ESC, FPV Camera, VTX, GPS Module with Compass, Battery Pack, Dual Band Receiver, Radio Controller, Payload Holder with servo Release Mechanism, Allied Accessories, Connectors and Cables, Tool Set Etc, User Technical Manual & Log book, Hard Case
        Total Quantity: 48
        OPTION CLAUSE: The Purchaser reserves the right to increase or decrease the quantity to be ordered up to 25 percent of bid quantity.
        Sample Clause: After award of contract - Successful Bidder shall submit 3 samples for Buyer approval within 5 days of award of contract.
        Undertaking Certificate: We hereby confirm that we shall not use any components, parts, material and product sourced from china for the manufacturing of drone.
        Malicious Code Certificate: Hardware and software being offered does not contain Embedded Malicious code.
        IT equipment shall be IPv6 ready from day one.
        Scope of supply includes Training: 5 employees to be trained at HQ 4 Arty Bde for duration of 10 days.
        Reverse Auction: RA would be conducted amongst first 50% lowest priced technically qualified bidders.
        """

    print("\n" + "="*70)
    print(" 1. SPECIFICATION EXTRACTION & COMPLIANCE CATEGORIZATION")
    print("="*70)
    analysis = extractor.analyze_specification_text(content)

    print(f"[+] Total Requirements Evaluated : {analysis['summary']['total_requirements_analyzed']}")
    print(f"[+] Hardware Deliverables Extracted: {analysis['summary']['hardware_deliverables_count']}")
    print(f"[+] Testing & SLA Deliverables     : {analysis['summary']['testing_deliverables_count']}")
    print(f"[+] Mandatory Submission Documents : {analysis['summary']['document_deliverables_count']}")
    print(f"[+] Critical Risk Flags Detected   : {analysis['summary']['critical_risks_identified']}")

    print("\n" + "-"*70)
    print(" CRITICAL RED FLAGS (DISQUALIFICATION & PENALTY RISKS)")
    print("-" * 70)
    for flag in analysis["critical_flags"]:
        print(f" [!] {flag['flag']}:")
        print(f"     Action: {flag['action']}")

    print("\n" + "-"*70)
    print(" EXTRACTED HARDWARE DELIVERABLES LIST")
    print("-" * 70)
    for idx, hw in enumerate(analysis["hardware_deliverables"], 1):
        print(f" {idx:02d}. {hw['subsystem']:<30} | {hw['tender_ref'][:40]}")

    print("\n" + "-"*70)
    print(" TESTING, INSPECTION & TRAINING DELIVERABLES")
    print("-" * 70)
    for idx, t in enumerate(analysis["testing_deliverables"], 1):
        print(f" {idx:02d}. {t['name']:<50} | {t['type']}")

    print("\n" + "-"*70)
    print(" MANDATORY BID SUBMISSION DOCUMENTS")
    print("-" * 70)
    for idx, d in enumerate(analysis["document_deliverables"], 1):
        print(f" [ ] {idx:02d}. {d['name']}")

    # Export to CSV
    csv_out = Path(args.export_csv)
    if not csv_out.is_absolute():
        csv_out = current_dir / "data" / args.export_csv
    extractor.export_analysis_to_csv(analysis, str(csv_out))

    print("\n" + "="*70)
    print(" 2. NON-CHINESE COMPLIANT BOM GENERATION & COST ROLLUP")
    print("="*70)
    # Determine type
    is_ord = "dropping" in content.lower() or "ordnance" in content.lower() or "holder" in content.lower()
    ttype = "ORDNANCE_DROPPING" if is_ord else "SURVEILLANCE_DAY_NIGHT"
    qty = 48 if is_ord else (args.qty if args.qty > 1 else 2)

    tender_res = engine.evaluate_tender({
        "tender_type": ttype,
        "quantity": qty,
        "client": "INDIAN_ARMY",
        "no_chinese_components": True,
        "advance_sample_required": True,
        "reverse_auction_enabled": True
    })

    summary = tender_res["tender_summary"]
    print(f"[+] Target Variant      : {summary['tender_type']}")
    print(f"[+] Total Quantity      : {summary['quantity']} Units")
    print(f"[+] Unit Hardware BOM   : INR {summary['bom_unit_hardware_cost']:,.2f}")
    print(f"[+] Total Project Cost  : INR {summary['total_estimated_cost']:,.2f} (Includes 5% warranty, inspection & contingency)")
    print(f"[+] Recommended Bid Price: INR {summary['suggested_bid_before_gst']:,.2f} (Excl. GST)")
    print(f"[+] Final Quote on GeM  : INR {summary['suggested_bid_with_gst']:,.2f} (Incl. 18% GST)")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
