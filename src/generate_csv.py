import csv
from tender_engine import TenderRuleEngine

def generate_excel_compatible_csv():
    engine = TenderRuleEngine()
    
    # 1. Evaluate Ordnance Dropping Tender (48 units)
    res_ord = engine.evaluate_tender({
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

    file_path = "/home/izi-system/Documents/Vana_BOMAutomation/data/VANA_Tender_Compliance_Checklist_Template.csv"
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["VANA DEFENCE & AEROSPACE — TENDER & BID COMPLIANCE MATRIX"])
        writer.writerow(["Generated for Indian Army / GeM Tenders (MoD Standard)"])
        writer.writerow([])
        
        # Section A: Tender Metadata
        writer.writerow(["SECTION A: TENDER IDENTIFICATION & COMMERCIAL SUMMARY"])
        writer.writerow(["Field", "Value", "Sales Team Action Required"])
        writer.writerow(["Tender BOQ Title", "10-inch Ordnance Dropping Drone", "Match exact BoQ title on GeM"])
        writer.writerow(["Quantity", 48, "Total delivery in 15 days to Jammu"])
        writer.writerow(["Total Unit Hardware BOM Cost", f"INR {res_ord['tender_summary']['bom_unit_hardware_cost']:,.2f}", "Internal benchmark"])
        writer.writerow(["Total Estimated Project Cost", f"INR {res_ord['tender_summary']['total_estimated_cost']:,.2f}", "Includes 5% warranty, inspection & contingency"])
        writer.writerow(["Recommended Initial Bid (Excl GST)", f"INR {res_ord['tender_summary']['suggested_bid_before_gst']:,.2f}", "25% Gross margin buffer for Reverse Auction"])
        writer.writerow(["Recommended Initial Bid (Incl 18% GST)", f"INR {res_ord['tender_summary']['suggested_bid_with_gst']:,.2f}", "Final quote on GeM financial portal"])
        writer.writerow([])

        # Section B: Critical Gatekeepers
        writer.writerow(["SECTION B: CRITICAL COMPLIANCE GATES (REJECTION RISKS)"])
        writer.writerow(["Gate #", "Risk Area", "Tender Requirement", "Sales Action / Rule Enforced", "Status"])
        writer.writerow([
            "GATE-01", 
            "Non-Chinese Origin", 
            "Zero Chinese components / parts / sub-assemblies (ATC Cl 17)", 
            "Mandatory signed undertaking certificate. All parts sourced from India/Europe/US.", 
            "MANDATORY"
        ])
        writer.writerow([
            "GATE-02", 
            "Advance Samples", 
            "3 Advance Samples to be delivered within 5 days of award (ATC Cl 3)", 
            "Ensure 3 units are ready in inventory; cost amortized into quote.", 
            "CRITICAL"
        ])
        writer.writerow([
            "GATE-03", 
            "Reverse Auction (RA)", 
            "RA between lowest 50% technically qualified bidders", 
            "Do NOT quote rock-bottom in round 1; retain 10-15% margin for live bidding.", 
            "COMMERCIAL"
        ])
        writer.writerow([
            "GATE-04", 
            "Option Clause", 
            "Buyer right to increase quantity up to +25% at contracted rate", 
            "Lock vendor component pricing for at least 180 days.", 
            "SUPPLY CHAIN"
        ])
        writer.writerow([
            "GATE-05", 
            "Make in India (MII)", 
            "Class 1 Local Supplier (Min 50% Local Content)", 
            "Upload OEM local content self-declaration with location of value addition.", 
            "ELIGIBILITY"
        ])
        writer.writerow([])

        # Section C: Compliant BOM Explosion
        writer.writerow(["SECTION C: EXPLODED NON-CHINESE COMPLIANT BOM (PER DRONE)"])
        writer.writerow(["Item #", "Subsystem / Category", "Component / Description", "Origin", "Qty/Drone", "Unit Cost (INR)", "Total Hardware (48 Units)"])
        for idx, line in enumerate(res_ord['calculated_bom'], 1):
            tot = line['unit_cost'] * line['qty_per_unit'] * 48
            writer.writerow([
                idx, 
                line['category'], 
                line['part'], 
                line['origin'], 
                line['qty_per_unit'], 
                f"INR {line['unit_cost']:,.2f}", 
                f"INR {tot:,.2f}"
            ])
        writer.writerow([])

        # Section D: Mandatory Documentation Checklist
        writer.writerow(["SECTION D: MANDATORY DOCUMENT UPLOAD CHECKLIST"])
        writer.writerow(["Doc #", "Document Name / Certificate", "Signed & Stamped?", "Ready for Upload?"])
        for idx, doc in enumerate(res_ord['mandatory_documents'], 1):
            writer.writerow([idx, doc, "[ ] YES", "[ ] READY"])

    print(f"Excel-compatible CSV template written to: {file_path}")

if __name__ == "__main__":
    generate_excel_compatible_csv()
