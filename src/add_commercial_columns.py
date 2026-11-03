import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add Warranty, AMC, and Training Configuration Inputs in Tab 2
old_adders_box = """                    <!-- Defense Field Services & Trial Cost Adders -->
                    <div style="padding:10px 16px 14px 16px; border-top:1px dashed #e2e8f0; background:#f8fafc; border-radius:0 0 6px 6px;">
                        <div style="font-size:11px; font-weight:700; color:#334155; margin-bottom:8px; display:flex; align-items:center; gap:6px;">
                            <i class="fas fa-shield-halved" style="color:#0284c7;"></i> MANDATORY DEFENSE FIELD SERVICES & TRIAL ADDERS:
                        </div>
                        <div style="display:flex; gap:20px; flex-wrap:wrap;">
                            <label style="display:flex; align-items:center; gap:6px; font-size:11px; font-weight:600; color:#1e293b; cursor:pointer;">
                                <input type="checkbox" id="chkTrials" onchange="recalculateBOM()">
                                <span>High-Altitude Field Trials (Leh/Ladakh) <strong style="color:#0369a1;">(+₹2,50,000)</strong></span>
                            </label>
                            <label style="display:flex; align-items:center; gap:6px; font-size:11px; font-weight:600; color:#1e293b; cursor:pointer;">
                                <input type="checkbox" id="chkTraining" onchange="recalculateBOM()">
                                <span>Army / DGQA On-Site Training Package <strong style="color:#0369a1;">(+₹1,20,000)</strong></span>
                            </label>
                            <label style="display:flex; align-items:center; gap:6px; font-size:11px; font-weight:600; color:#1e293b; cursor:pointer;">
                                <input type="checkbox" id="chkCrating" onchange="recalculateBOM()">
                                <span>Military IP67 Crating & Hazmat Logistics <strong style="color:#0369a1;">(+₹85,000)</strong></span>
                            </label>
                        </div>
                    </div>
                </div>"""

new_adders_box = """                    <!-- Defense Field Services & Trial Cost Adders -->
                    <div style="padding:10px 16px 14px 16px; border-top:1px dashed #e2e8f0; background:#f8fafc;">
                        <div style="font-size:11px; font-weight:700; color:#334155; margin-bottom:8px; display:flex; align-items:center; gap:6px;">
                            <i class="fas fa-shield-halved" style="color:#0284c7;"></i> MANDATORY DEFENSE FIELD SERVICES & TRIAL ADDERS:
                        </div>
                        <div style="display:flex; gap:20px; flex-wrap:wrap;">
                            <label style="display:flex; align-items:center; gap:6px; font-size:11px; font-weight:600; color:#1e293b; cursor:pointer;">
                                <input type="checkbox" id="chkTrials" onchange="recalculateBOM()">
                                <span>High-Altitude Field Trials (Leh/Ladakh) <strong style="color:#0369a1;">(+₹2,50,000)</strong></span>
                            </label>
                            <label style="display:flex; align-items:center; gap:6px; font-size:11px; font-weight:600; color:#1e293b; cursor:pointer;">
                                <input type="checkbox" id="chkTraining" onchange="recalculateBOM()">
                                <span>Army / DGQA On-Site Training Package <strong style="color:#0369a1;">(+₹1,20,000)</strong></span>
                            </label>
                            <label style="display:flex; align-items:center; gap:6px; font-size:11px; font-weight:600; color:#1e293b; cursor:pointer;">
                                <input type="checkbox" id="chkCrating" onchange="recalculateBOM()">
                                <span>Military IP67 Crating & Hazmat Logistics <strong style="color:#0369a1;">(+₹85,000)</strong></span>
                            </label>
                        </div>
                    </div>

                    <!-- Dedicated Separate Fields for Warranty, AMC & Training -->
                    <div style="padding:14px 16px; border-top:1px solid #e2e8f0; background:#f0f9ff; border-radius:0 0 6px 6px;">
                        <div style="font-size:11px; font-weight:800; color:#0369a1; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:10px; display:flex; align-items:center; gap:6px;">
                            <i class="fas fa-clipboard-check"></i> Contractual Specifications (Separate Evaluation Parameters):
                        </div>
                        <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:16px;">
                            <div>
                                <label style="font-size:11px; font-weight:700; color:#0f172a; display:block; margin-bottom:4px;">
                                    1. WARRANTY PERIOD:
                                </label>
                                <input type="text" id="cfgWarranty" value="3 Years Comprehensive On-Site" oninput="updateCommercialTermsTable()" style="width:100%; border:1px solid #7dd3fc; border-radius:4px; padding:6px 10px; font-size:12px; font-weight:600; background:#ffffff;">
                                <span style="font-size:10px; color:#64748b; margin-top:2px; display:block;">Defect liability & full replacement of all spares</span>
                            </div>
                            <div>
                                <label style="font-size:11px; font-weight:700; color:#0f172a; display:block; margin-bottom:4px;">
                                    2. AMC DURATION & TERMS:
                                </label>
                                <input type="text" id="cfgAMC" value="2 Years Post-Warranty (48-Hr Turnaround SLA)" oninput="updateCommercialTermsTable()" style="width:100%; border:1px solid #7dd3fc; border-radius:4px; padding:6px 10px; font-size:12px; font-weight:600; background:#ffffff;">
                                <span style="font-size:10px; color:#64748b; margin-top:2px; display:block;">Annual maintenance, scheduled servicing & depot support</span>
                            </div>
                            <div>
                                <label style="font-size:11px; font-weight:700; color:#0f172a; display:block; margin-bottom:4px;">
                                    3. TRAINING LOCATION(S) & DAYS:
                                </label>
                                <input type="text" id="cfgTraining" value="Buyer Base / High-Altitude (Leh) — 10 Working Days" oninput="updateCommercialTermsTable()" style="width:100%; border:1px solid #7dd3fc; border-radius:4px; padding:6px 10px; font-size:12px; font-weight:600; background:#ffffff;">
                                <span style="font-size:10px; color:#64748b; margin-top:2px; display:block;">5 Days Flight Navigation + 5 Days 1st-Line Maintenance</span>
                            </div>
                        </div>
                    </div>
                </div>"""

if old_adders_box in html:
    html = html.replace(old_adders_box, new_adders_box)
    print("[1/5] Dedicated configuration fields for Warranty, AMC & Training added")
else:
    print("Warning: old_adders_box not found")

# 2. Add Dedicated Commercial & SLA Terms Table into Tab 2 (right under BOM table)
old_bom_panel_end = """                <!-- Quick Step Navigation for Sales -->
                <div class="step-nav-footer">
                    <button type="button" class="btn-secondary" onclick="switchTab('tab-extract', document.getElementById('nav-step-1'))">
                        &larr; Back to Step 1: Tender Details
                    </button>
                    <button type="button" class="btn-primary" style="padding:8px 18px; font-weight:700;" onclick="switchTab('tab-gaps', document.getElementById('nav-step-3'))">
                        Next: Step 3 — Handle Missing Items &rarr;
                    </button>
                </div>
            </div>"""

new_bom_panel_end = """                <!-- Dedicated Evaluation Table: Warranty, AMC & Training (Separate Columns) -->
                <div class="data-panel" style="margin-top:20px;">
                    <div class="panel-heading" style="background:#f8fafc; border-bottom:1px solid #e2e8f0;">
                        <span class="panel-title" style="color:#0f172a;">
                            <i class="fas fa-handshake" style="color:#0284c7;"></i> Commercial & SLA Terms Matrix (Separate Evaluation Columns)
                        </span>
                        <span class="badge badge-green">Clearly Separated</span>
                    </div>
                    <div class="panel-body" style="padding:0; overflow-x:auto;">
                        <table class="enterprise-table" style="font-size:12px;">
                            <thead>
                                <tr>
                                    <th style="width:120px;">Parameter</th>
                                    <th style="width:200px;">Scope of Obligation</th>
                                    <th style="width:180px; color:#0369a1; background:#f0f9ff;">Warranty Period</th>
                                    <th style="width:220px; color:#0369a1; background:#f0f9ff;">AMC Duration & Terms</th>
                                    <th style="width:250px; color:#0369a1; background:#f0f9ff;">Training Location(s) & Days</th>
                                    <th style="text-align:right; width:130px;">Pricing Status</th>
                                </tr>
                            </thead>
                            <tbody id="commercialTermsTableBody">
                                <!-- Populated dynamically -->
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Quick Step Navigation for Sales -->
                <div class="step-nav-footer">
                    <button type="button" class="btn-secondary" onclick="switchTab('tab-extract', document.getElementById('nav-step-1'))">
                        &larr; Back to Step 1: Tender Details
                    </button>
                    <button type="button" class="btn-primary" style="padding:8px 18px; font-weight:700;" onclick="switchTab('tab-gaps', document.getElementById('nav-step-3'))">
                        Next: Step 3 — Handle Missing Items &rarr;
                    </button>
                </div>
            </div>"""

if old_bom_panel_end in html:
    html = html.replace(old_bom_panel_end, new_bom_panel_end)
    print("[2/5] Dedicated Commercial Terms Table added to Tab 2")
else:
    print("Warning: old_bom_panel_end not found")

# 3. Add JS function to render Commercial Terms Table
commercial_js = """
        // Update the dedicated separate columns table for Warranty, AMC & Training
        function updateCommercialTermsTable() {
            const tbody = document.getElementById('commercialTermsTableBody');
            if (!tbody) return;

            const warranty = document.getElementById('cfgWarranty')?.value || "3 Years Comprehensive On-Site";
            const amc = document.getElementById('cfgAMC')?.value || "2 Years Post-Warranty (48h Turnaround SLA)";
            const training = document.getElementById('cfgTraining')?.value || "Buyer Base / Leh Field — 10 Working Days";

            tbody.innerHTML = `
                <tr>
                    <td style="font-weight:700; color:#0f172a;"><i class="fas fa-shield" style="color:#0284c7; margin-right:4px;"></i> Warranty</td>
                    <td>Comprehensive on-site replacement & defect liability covering all mechanical, electrical, avionics & payload parts</td>
                    <td style="font-weight:800; color:#15803d; background:#f0fdf4;">${warranty}</td>
                    <td style="color:#94a3b8; font-style:italic;">Included in Warranty Period</td>
                    <td style="color:#94a3b8; font-style:italic;">Consignee Bases (Pan-India)</td>
                    <td style="text-align:right;"><span class="badge badge-green">Included in Bid</span></td>
                </tr>
                <tr>
                    <td style="font-weight:700; color:#0f172a;"><i class="fas fa-screwdriver-wrench" style="color:#0284c7; margin-right:4px;"></i> AMC</td>
                    <td>Post-warranty annual maintenance contract, preventive health-checks, scheduled calibration & spares buffer</td>
                    <td style="color:#94a3b8; font-style:italic;">Commences post-warranty</td>
                    <td style="font-weight:800; color:#0369a1; background:#f0f9ff;">${amc}</td>
                    <td style="color:#94a3b8; font-style:italic;">Regional Depot & On-Site</td>
                    <td style="text-align:right;"><span class="badge badge-green">Covered in Reserves</span></td>
                </tr>
                <tr>
                    <td style="font-weight:700; color:#0f172a;"><i class="fas fa-graduation-cap" style="color:#0284c7; margin-right:4px;"></i> Training</td>
                    <td>Operational training for pilots (5 days simulation & flight) + First-line maintenance & payload handling (5 days)</td>
                    <td style="color:#94a3b8; font-style:italic;">Conducted prior to hand-over</td>
                    <td style="color:#94a3b8; font-style:italic;">Covers 10 personnel per batch</td>
                    <td style="font-weight:800; color:#b45309; background:#fffbeb;">${training}</td>
                    <td style="text-align:right;"><span class="badge badge-green">Included in Bid</span></td>
                </tr>
            `;
        }
"""

if 'function updateCommercialTermsTable()' not in html:
    html = html.replace('// 1. MAKE IN INDIA (MII) LOCAL CONTENT & CERTIFICATE', commercial_js + '\n        // 1. MAKE IN INDIA (MII) LOCAL CONTENT & CERTIFICATE')
    print("[3/5] JS logic for updating commercial table injected")
else:
    print("Warning: updateCommercialTermsTable already present")

# Call updateCommercialTermsTable on window.onload and handleVariantChange
if 'updateCommercialTermsTable();' not in html:
    html = html.replace('recalculateBOM();\n            renderGaps();', 'recalculateBOM();\n            updateCommercialTermsTable();\n            renderGaps();')
    print("[4/5] updateCommercialTermsTable hooked into onload")

# 4. Update CSV Export to include separate Warranty, AMC, and Training columns
old_csv_end = """            csv += `Total Project Cost (Cost Floor),,${Math.round(totalProjectCost)}\\n`;
            csv += `Recommended Base Bid (Excl GST),,${Math.round(bidExGST)}\\n`;
            csv += `Official GeM Bid (Incl 18% GST),,${Math.round(bidIncGST)}\\n\\n`;
            csv += `MAKE IN INDIA COMPLIANCE\\n`;
            csv += `Local Content Percentage,,${mii.pct.toFixed(1)}%\\n`;
            csv += `Supplier Classification,,${mii.supplierClass}\\n`;
            csv += `Zero Chinese Origin Verified,,100% Compliant (MoD Cl 17)\\n`;"""

new_csv_end = """            csv += `Total Project Cost (Cost Floor),,${Math.round(totalProjectCost)}\\n`;
            csv += `Recommended Base Bid (Excl GST),,${Math.round(bidExGST)}\\n`;
            csv += `Official GeM Bid (Incl 18% GST),,${Math.round(bidIncGST)}\\n\\n`;

            const warrantyVal = document.getElementById('cfgWarranty')?.value || "3 Years Comprehensive On-Site";
            const amcVal = document.getElementById('cfgAMC')?.value || "2 Years Post-Warranty (48h Turnaround SLA)";
            const trainingVal = document.getElementById('cfgTraining')?.value || "Buyer Base / High-Altitude (Leh) — 10 Working Days";

            csv += `CONTRACTUAL & SERVICE TERMS (SEPARATE EVALUATION COLUMNS)\\n`;
            csv += `Parameter,Scope of Obligation,Warranty Period,AMC Duration & Terms,Training Location & Days,Pricing Status\\n`;
            csv += `"Warranty","Comprehensive On-Site Defect Liability & Spares","${warrantyVal}","Included in Warranty Period","Consignee Bases (Pan-India)","Included in Bid"\\n`;
            csv += `"AMC","Post-Warranty Maintenance & Scheduled Calibration","Commences Post-Warranty","${amcVal}","Regional Depot & On-Site","Included in Reserves"\\n`;
            csv += `"Training","Pilot Flight Navigation & 1st Line Maintenance","Pre-Delivery / Handover","Covers 10 Pilots & Techs","${trainingVal}","Included in Package"\\n\\n`;

            csv += `MAKE IN INDIA COMPLIANCE\\n`;
            csv += `Local Content Percentage,,${mii.pct.toFixed(1)}%\\n`;
            csv += `Supplier Classification,,${mii.supplierClass}\\n`;
            csv += `Zero Chinese Origin Verified,,100% Compliant (MoD Cl 17)\\n`;"""

if old_csv_end in html:
    html = html.replace(old_csv_end, new_csv_end)
    print("[5/5] CSV export updated with separate Warranty, AMC, and Training columns")
else:
    print("Warning: old_csv_end not found")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Commercial columns integration script finished!")
