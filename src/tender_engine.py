import json
import sqlite3
from typing import Dict, List, Any

DB_PATH = "/home/izi-system/Documents/Vana_BOMAutomation/data/vana_catalog.db"

class TenderRuleEngine:
    """
    Evaluates tender parameters, checks Indian Army & MoD GeM compliances,
    enforces non-Chinese origin rules, auto-generates BOM, and identifies all cost/clause risks.
    """

    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def get_items_by_category(self, category: str, exclude_china: bool = True, prefer_mii: bool = True):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        query = "SELECT id, category, manufacturer, model, country, specs, price_inr, is_mii FROM items WHERE category = ?"
        params = [category]
        if exclude_china:
            query += " AND LOWER(country) NOT IN ('china', 'chinese')"
        if prefer_mii:
            query += " ORDER BY is_mii DESC, price_inr ASC"
        else:
            query += " ORDER BY price_inr ASC"
        cur.execute(query, params)
        rows = cur.fetchall()
        conn.close()
        return [
            {
                "id": r[0], "category": r[1], "manufacturer": r[2], "model": r[3],
                "country": r[4], "specs": r[5], "price_inr": r[6], "is_mii": bool(r[7])
            }
            for r in rows
        ]

    def evaluate_tender(self, tender_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Input keys:
        - tender_type: "ORDNANCE_DROPPING" | "SURVEILLANCE_DAY" | "SURVEILLANCE_DAY_NIGHT" | "EW_CONTESTED"
        - quantity: int
        - is_gem_tender: bool (default True)
        - client: "INDIAN_ARMY" | "CIVILIAN" | etc.
        - delivery_days: int
        - advance_sample_required: bool
        - advance_sample_qty: int
        - option_clause_pct: int (e.g. 25 or 50)
        - training_required: bool
        - training_personnel: int
        - training_days: int
        - site_visit_mandatory: bool
        - reverse_auction_enabled: bool
        - local_content_threshold: int (e.g. 50%)
        """
        warnings = []
        critical_alerts = []
        action_items = []
        mandatory_documents = []
        calculated_bom = []

        qty = tender_input.get("quantity", 1)
        ttype = tender_input.get("tender_type", "SURVEILLANCE_DAY_NIGHT")
        client = tender_input.get("client", "INDIAN_ARMY")
        delivery_days = tender_input.get("delivery_days", 15)

        # -------------------------------------------------------------
        # 1. CHINA CLAUSE & LAND-BORDER RESTRICTION
        # -------------------------------------------------------------
        is_mod = (client == "INDIAN_ARMY")
        exclude_china = is_mod or tender_input.get("no_chinese_components", True)
        if exclude_china:
            critical_alerts.append({
                "type": "STRICT_COMPLIANCE",
                "title": "NON-CHINESE ORIGIN UNDERTAKING REQUIRED",
                "detail": "MoD/Army ATC mandates a signed declaration that ZERO components are sourced from China. Any Chinese sub-assembly found during TEC/Inspection will forfeit payments and black-list the firm."
            })
            mandatory_documents.append("MoD Non-Chinese Origin Undertaking Certificate (Signed & Stamped)")

        # -------------------------------------------------------------
        # 2. LOCAL CONTENT (MAKE IN INDIA - MII)
        # -------------------------------------------------------------
        local_content_req = tender_input.get("local_content_threshold", 50)
        if local_content_req >= 50:
            action_items.append({
                "category": "ELIGIBILITY",
                "title": f"Class-1 Local Supplier Certification (Min {local_content_req}% Local Content)",
                "detail": "Provide OEM Local Content calculation certificate detailing location of local value addition in India. Must be certified by CA/Cost Accountant if value > 10 Cr."
            })
            mandatory_documents.append("OEM Class-1 Local Content Self-Declaration / CA Certificate")

        # -------------------------------------------------------------
        # 3. REVERSE AUCTION (RA) STRATEGY
        # -------------------------------------------------------------
        if tender_input.get("reverse_auction_enabled", True):
            ra_rule = tender_input.get("ra_rule", "50% Lowest Priced Technically Qualified")
            warnings.append({
                "type": "PRICING_RISK",
                "title": "Reverse Auction (RA) Enabled",
                "detail": f"Evaluation rule: '{ra_rule}'. Do not quote your bottom break-even price in the initial technical bid. Leave 8-15% margin headroom to compete in the live reverse auction without dropping into negative margin."
            })

        # -------------------------------------------------------------
        # 4. OPTION CLAUSE (25% to 50% Quantity Increase at same rate)
        # -------------------------------------------------------------
        option_pct = tender_input.get("option_clause_pct", 25)
        if option_pct > 0:
            warnings.append({
                "type": "SUPPLY_CHAIN_RISK",
                "title": f"Buyer Option Clause ({option_pct}% Repeat Order at Contracted Rate)",
                "detail": f"Buyer can demand up to {option_pct}% extra quantity at the exact same unit price during the contract period. Verify long-term price validity with motor, battery, and sensor vendors."
            })

        # -------------------------------------------------------------
        # 5. ADVANCE SAMPLES & FIELD ACCEPTANCE TESTING
        # -------------------------------------------------------------
        if tender_input.get("advance_sample_required", False):
            sample_qty = tender_input.get("advance_sample_qty", 3)
            sample_days = tender_input.get("advance_sample_days", 5)
            critical_alerts.append({
                "type": "DELIVERY_RISK",
                "title": f"Advance Sample Clause: {sample_qty} Units within {sample_days} Days!",
                "detail": f"Successful bidder MUST deliver {sample_qty} physical test units to the buyer within {sample_days} days of contract award free of cost for destructive/field testing. Cost of {sample_qty} test units MUST be amortized across the project quote."
            })

        # -------------------------------------------------------------
        # 6. TRAINING & COMMISSIONING
        # -------------------------------------------------------------
        training_cost = 0
        if tender_input.get("training_required", False):
            trainees = tender_input.get("training_personnel", 5)
            t_days = tender_input.get("training_days", 10)
            t_loc = tender_input.get("training_location", "Consignee Site (e.g. Prayagraj / Nowshera)")
            # Estimated engineering instructor cost per day + travel
            training_cost = t_days * 12000 + 40000 # 1.6 Lakhs estimate
            action_items.append({
                "category": "COMMERCIAL_COST",
                "title": f"On-Site Training: {trainees} Personnel for {t_days} Days at {t_loc}",
                "detail": f"Budgeted approx INR {training_cost:,.0f} for trainer travel, lodging, syllabus, and flight certificates."
            })

        # -------------------------------------------------------------
        # 7. MANDATORY DOCUMENT CHECKLIST
        # -------------------------------------------------------------
        mandatory_documents.extend([
            "PAN Card & GSTIN Registration Copy",
            "Cancelled Cheque & Certified Bank EFT Mandate",
            "Bidder Financial Standing Declaration (Not bankrupt / in receivership)",
            "3-Year Residual Market Life Certificate (Equipment not obsolete / EOL)",
            "IPv6 Ready Compliance Certificate (For all IT/IP network components)",
            "Malicious Code Certificate (Firmware & Hardware free from spyware/backdoors)",
            "Non-Disclosure Declaration Certificate (On Company Letterhead)",
            "OEM Authorization Certificate (MAF) with contact details",
            "ISO 9001:2015 Quality Certificate",
            "3 Years Past Performance Proof (CRAC / Supply orders to Govt/PSU for >= 30%)",
            "Audited Balance Sheets (Last 3 Financial Years certified by CA)",
            "Compliance Sheet against Buyer Technical Specifications (BoQ line by line)"
        ])

        # -------------------------------------------------------------
        # 8. AUTOMATIC BOM DERIVATION ACCORDING TO TENDER TYPE
        # -------------------------------------------------------------
        # Helper to pick best compliant part
        def pick(cat, pref_kw=""):
            items = self.get_items_by_category(cat, exclude_china=exclude_china, prefer_mii=True)
            if pref_kw:
                matches = [i for i in items if pref_kw.lower() in i['model'].lower() or pref_kw.lower() in i['manufacturer'].lower()]
                if matches:
                    return matches[0]
            return items[0] if items else None

        if ttype == "ORDNANCE_DROPPING":
            # 10 Inch Ordnance Dropping Drone (as per Bid GEM/2026/B/7922599)
            # Motor: 4 per drone
            m = pick("Motor", "3115") or pick("Motor", "4006")
            e = pick("ESC", "Flameback") or pick("ESC", "Vector")
            p = pick("Propeller", "Reflex") or pick("Propeller", "17")
            b = pick("Battery", "M power")
            fc = pick("Flight Controller", "Agam") or pick("Flight Controller", "BotLab")
            gps = pick("GPS / GNSS", "Orbit Nano")
            rc = pick("Transmitter / RC", "Axle Drone")
            chg = pick("Battery Charger", "ToolkitRC") or pick("Battery Charger", "SkyRC")
            acc_release = pick("Accessories", "Release")
            acc_case = pick("Accessories", "Hard Case")
            acc_tools = pick("Accessories", "Tool Set")
            acc_log = pick("Accessories", "Manual")
            nav_light = pick("Navigation Lights", "Vector")

            calculated_bom = [
                {"category": "Frame & Mechanicals", "part": "10-inch Carbon Fiber Drone Frame", "qty_per_unit": 1, "unit_cost": 28000, "origin": "India"},
                {"category": "Motor", "part": f"{m['manufacturer']} {m['model']}", "qty_per_unit": 4, "unit_cost": m['price_inr'], "origin": m['country']},
                {"category": "ESC", "part": f"{e['manufacturer']} {e['model']}", "qty_per_unit": 4, "unit_cost": e['price_inr'], "origin": e['country']},
                {"category": "Propeller", "part": f"{p['manufacturer']} {p['model']} (Pair)", "qty_per_unit": 2, "unit_cost": p['price_inr'], "origin": p['country']},
                {"category": "Flight Controller", "part": f"{fc['manufacturer']} {fc['model']}", "qty_per_unit": 1, "unit_cost": fc['price_inr'], "origin": fc['country']},
                {"category": "GPS/GNSS", "part": f"{gps['manufacturer']} {gps['model']}", "qty_per_unit": 1, "unit_cost": gps['price_inr'], "origin": gps['country']},
                {"category": "Battery", "part": f"{b['manufacturer']} {b['model']}", "qty_per_unit": 2, "unit_cost": b['price_inr'], "origin": b['country']},
                {"category": "Radio Controller / GCS", "part": f"{rc['manufacturer']} {rc['model']}", "qty_per_unit": 1, "unit_cost": rc['price_inr'], "origin": rc['country']},
                {"category": "Ordnance Release", "part": f"{acc_release['model']}", "qty_per_unit": 1, "unit_cost": acc_release['price_inr'], "origin": "India"},
                {"category": "Charger", "part": f"{chg['manufacturer']} {chg['model']}", "qty_per_unit": 1, "unit_cost": chg['price_inr'], "origin": chg['country']},
                {"category": "Hard Transport Case", "part": f"{acc_case['model']}", "qty_per_unit": 1, "unit_cost": acc_case['price_inr'], "origin": "India"},
                {"category": "Tool Kit & Spares", "part": f"{acc_tools['model']}", "qty_per_unit": 1, "unit_cost": acc_tools['price_inr'], "origin": "India"},
                {"category": "Logbook & Technical Manual", "part": f"{acc_log['model']}", "qty_per_unit": 1, "unit_cost": acc_log['price_inr'], "origin": "India"},
                {"category": "Nav Lights / Strobes", "part": f"{nav_light['model']}", "qty_per_unit": 1, "unit_cost": nav_light['price_inr'], "origin": nav_light['country']}
            ]

        elif ttype in ("SURVEILLANCE_DAY_NIGHT", "TACTICAL_DRONE"):
            # Multi-Mission Tactical Drone / Surveillance System (Bids 7949747 & 7779287)
            m = pick("Motor", "Vector") or pick("Motor", "Flameback")
            e = pick("ESC", "Vector") or pick("ESC", "Flameback")
            p = pick("Propeller", "Reflex") or pick("Propeller", "Mejzlik")
            b = pick("Battery", "GenX Power") or pick("Battery", "M power")
            cam = pick("Camera / Payload", "MotionMatics") or pick("Camera / Payload", "Delopt")
            fc = pick("Flight Controller", "Orange cube") or pick("Flight Controller", "Agam")
            gps = pick("GPS / GNSS", "Orbit Nano") or pick("GPS / GNSS", "Here")
            rc = pick("Transmitter / RC", "Apex") or pick("Transmitter / RC", "Axle")
            chg = pick("Battery Charger", "Tattu") or pick("Battery Charger", "SkyRC")
            gcs_laptop = pick("Rugged Laptop / Tablet", "Zebra") or pick("Rugged Laptop / Tablet", "Getac")
            acc_case = pick("Accessories", "Hard Case")
            acc_tools = pick("Accessories", "Tool Set")
            acc_log = pick("Accessories", "Manual")

            calculated_bom = [
                {"category": "Airframe", "part": "VANA Tactical Carbon Quad/Hex Airframe (IP54)", "qty_per_unit": 1, "unit_cost": 85000, "origin": "India"},
                {"category": "Motor", "part": f"{m['manufacturer']} {m['model']}", "qty_per_unit": 4, "unit_cost": m['price_inr'], "origin": m['country']},
                {"category": "ESC", "part": f"{e['manufacturer']} {e['model']}", "qty_per_unit": 4, "unit_cost": e['price_inr'], "origin": e['country']},
                {"category": "Propeller", "part": f"{p['manufacturer']} {p['model']} (Pair)", "qty_per_unit": 2, "unit_cost": p['price_inr'], "origin": p['country']},
                {"category": "Payload Gimbal (Day+Night)", "part": f"{cam['manufacturer']} {cam['model']}", "qty_per_unit": 1, "unit_cost": cam['price_inr'], "origin": cam['country']},
                {"category": "Flight Controller", "part": f"{fc['manufacturer']} {fc['model']}", "qty_per_unit": 1, "unit_cost": fc['price_inr'], "origin": fc['country']},
                {"category": "GPS/GNSS RTK", "part": f"{gps['manufacturer']} {gps['model']}", "qty_per_unit": 1, "unit_cost": gps['price_inr'], "origin": gps['country']},
                {"category": "Tactical Battery Pack (1 Op + 1 Spare)", "part": f"{b['manufacturer']} {b['model']}", "qty_per_unit": 2, "unit_cost": b['price_inr'], "origin": b['country']},
                {"category": "GCS & Datalink (10-20km)", "part": f"{rc['manufacturer']} {rc['model']}", "qty_per_unit": 1, "unit_cost": rc['price_inr'], "origin": rc['country']},
                {"category": "Rugged GCS Laptop/Tablet", "part": f"{gcs_laptop['manufacturer']} {gcs_laptop['model']}", "qty_per_unit": 1, "unit_cost": gcs_laptop['price_inr'], "origin": gcs_laptop['country']},
                {"category": "Heavy-Duty Dual Charger", "part": f"{chg['manufacturer']} {chg['model']}", "qty_per_unit": 1, "unit_cost": chg['price_inr'], "origin": chg['country']},
                {"category": "Military Hard Case IP67", "part": f"{acc_case['model']}", "qty_per_unit": 2, "unit_cost": acc_case['price_inr'], "origin": "India"},
                {"category": "Maintenance Tool Kit", "part": f"{acc_tools['model']}", "qty_per_unit": 1, "unit_cost": acc_tools['price_inr'], "origin": "India"},
                {"category": "User Manual & Logbook", "part": f"{acc_log['model']}", "qty_per_unit": 1, "unit_cost": acc_log['price_inr'], "origin": "India"}
            ]

        # Calculate unit and total costs
        bom_unit_cost = sum(line["unit_cost"] * line["qty_per_unit"] for line in calculated_bom)
        bom_total_hardware = bom_unit_cost * qty

        # Mandatory services & risk buffers
        inspection_buffer = 35000  # Board of officers stage-wise inspection cost buffer
        warranty_buffer = bom_total_hardware * 0.05  # 5% warranty reserve for 1-year on-site support
        gst_pct = 18.0
        contingency = bom_total_hardware * 0.04 # 4% contingency for Option clause / currency variation

        total_project_cost = bom_total_hardware + training_cost + inspection_buffer + warranty_buffer + contingency
        suggested_quote_before_gst = total_project_cost * 1.25 # 25% gross margin baseline before RA
        suggested_quote_with_gst = suggested_quote_before_gst * 1.18

        return {
            "tender_summary": {
                "tender_type": ttype,
                "quantity": qty,
                "delivery_days": delivery_days,
                "client": client,
                "bom_unit_hardware_cost": bom_unit_cost,
                "total_hardware_cost": bom_total_hardware,
                "training_cost": training_cost,
                "inspection_buffer": inspection_buffer,
                "warranty_buffer": warranty_buffer,
                "contingency_buffer": contingency,
                "total_estimated_cost": total_project_cost,
                "suggested_bid_before_gst": suggested_quote_before_gst,
                "suggested_bid_with_gst": suggested_quote_with_gst
            },
            "critical_alerts": critical_alerts,
            "warnings": warnings,
            "action_items": action_items,
            "mandatory_documents": mandatory_documents,
            "calculated_bom": calculated_bom
        }

if __name__ == "__main__":
    engine = TenderRuleEngine()
    # Test with Ordnance Dropping Drone Tender (48 units)
    res = engine.evaluate_tender({
        "tender_type": "ORDNANCE_DROPPING",
        "quantity": 48,
        "client": "INDIAN_ARMY",
        "delivery_days": 15,
        "advance_sample_required": True,
        "advance_sample_qty": 3,
        "advance_sample_days": 5,
        "option_clause_pct": 25,
        "reverse_auction_enabled": True
    })
    print(json.dumps(res, indent=2))
