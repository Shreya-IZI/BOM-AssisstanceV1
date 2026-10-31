# VANA Defence & Aerospace — Tender & BOM Intelligence Workspace

An enterprise-grade system for tender requirement extraction, statutory compliance categorization, and automated Bill of Materials (BOM) explosion tailored for Indian Ministry of Defence (MoD) and GeM (Government e-Marketplace) operations.

---

## Key Features

1. **Document Ingestion & Parsing:**
   * Direct drag-and-drop support for GeM tender PDFs and specification sheets.
   * Cleans bilingual text, strips corrupt font encodings, and parses technical clauses.

2. **Statutory Risk & Compliance Gates:**
   * Detects and enforces **Strict Non-Chinese Origin (ATC Cl 17)**.
   * Identifies **5-Day Advance Sample SLAs**, **Option Clauses (+25% to +50%)**, and **Reverse Auction (RA)** rules.

3. **Compliant BOM Explosion & Costing:**
   * Selects 100% Non-Chinese components from the verified 140-item catalog.
   * Computes Hardware Total, 5% Warranty Reserve, 4% Contingency, and 18% GST.
   * Displays both **Base Revenue (Excl. GST)** and the **Official GeM Bid (Incl. GST)**.

4. **Sourcing Gaps & Provisional Costing:**
   * Manage items requested in tenders that aren't yet in the catalog.
   * Add provisional quotes to prevent bidding delays, which automatically inject into the active BOM.

5. **Exports:**
   * One-click download of the complete BOM to Excel-compatible CSV.
   * Print/Save to official PDF.

---

## Live Deployment on Vercel

This repository is optimized for immediate deployment on **Vercel**:
* `index.html` is configured at the root as a static enterprise web application.
* No complex backend server setup is required.
