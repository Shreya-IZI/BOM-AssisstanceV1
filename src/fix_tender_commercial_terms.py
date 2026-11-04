with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update executeAnalysis extraction logic for Warranty, AMC, and Training
old_analysis_block = """            // Auto-detect Warranty Period
            const wMatch = text.match(/(\\d+)\\s*(?:year|yr)s?\\s*(?:comprehensive\\s*)?(?:warranty|guarantee)/i);
            const wInput = document.getElementById('cfgWarranty');
            if (wInput) wInput.value = (wMatch && wMatch[1]) ? `${wMatch[1]} Years Comprehensive On-Site` : "3 Years Comprehensive On-Site";

            // Auto-detect AMC Terms
            const amcMatch = text.match(/(\\d+)\\s*(?:year|yr)s?\\s*(?:amc|camc|annual\\s*maintenance)/i);
            const aInput = document.getElementById('cfgAMC');
            if (aInput) aInput.value = (amcMatch && amcMatch[1]) ? `${amcMatch[1]} Years Post-Warranty (48h Turnaround SLA)` : "2 Years Post-Warranty (48-Hr Turnaround SLA)";

            // Auto-detect Training Location & Days
            const trDaysMatch = text.match(/(\\d+)\\s*(?:working\\s*)?days?\\s*(?:training|instruction)/i) || text.match(/training[\\s\\S]{0,40}?(\\d+)\\s*days?/i);
            const trLocMatch = text.match(/(leh|ladakh|high[-\\s]altitude|buyer\\s*location|consignee\\s*base|field\\s*site)/i);
            const trDays = trDaysMatch ? `${trDaysMatch[1]} Working Days` : "10 Working Days";
            const trLoc = trLocMatch ? trLocMatch[1].toUpperCase() : "Buyer Base / Leh Field";
            const tInput = document.getElementById('cfgTraining');
            if (tInput) tInput.value = `${trLoc} — ${trDays}`;"""

new_analysis_block = """            // 1. Accurately detect Warranty Period (e.g. "Warranty period ... shall be 1 years")
            const wMatch = text.match(/warranty[\\s\\S]{0,50}?(\\d+)\\s*(?:year|yr|month)s?/i) || 
                           text.match(/(\\d+)\\s*(?:year|yr|month)s?[\\s\\S]{0,20}?warranty/i);
            const wInput = document.getElementById('cfgWarranty');
            if (wInput) {
                if (wMatch && wMatch[1]) {
                    const num = parseInt(wMatch[1]);
                    wInput.value = `${num} Year${num > 1 ? 's' : ''} from final acceptance at consignee site (Cl 30)`;
                } else {
                    wInput.value = "1 Year from final acceptance at consignee location (Standard GeM GTC)";
                }
            }

            // 2. Accurately detect AMC Terms (Tender does not mandate separate AMC)
            const amcMatch = text.match(/\\b(amc|camc|annual\\s*maintenance\\s*contract)\\b/i);
            const aInput = document.getElementById('cfgAMC');
            if (aInput) {
                if (amcMatch) {
                    const amcDur = text.match(/(?:amc|camc|annual\\s*maintenance)[\\s\\S]{0,40}?(\\d+)\\s*(?:year|yr)s?/i);
                    aInput.value = amcDur ? `${amcDur[1]} Years Comprehensive Post-Warranty AMC` : "Comprehensive Annual Maintenance Contract as per ATC";
                } else {
                    aInput.value = "Not Required in Tender Scope (Nil AMC / OEM Maintenance Group in India)";
                }
            }

            // 3. Accurately detect Training Location, Trainees & Days (e.g. "5 employees ... HQ 4 Arty Bde ... 10 days")
            const cleanT = text.replace(/\\d+\\s*\\/\\s*\\d+/g, ' '); // remove page numbers
            const trEmpMatch = cleanT.match(/number\\s+of\\s+employees\\s+to\\s+be\\s+trained[\\s\\S]{0,30}?(\\d+)/i) || 
                               cleanT.match(/(\\d+)\\s*(?:employees|personnel|operators|pilots)/i);
            const trLocMatch = cleanT.match(/place\\s+for\\s+training[\\s\\S]{0,35}?([A-Za-z0-9\\s]+?)(?:and|\\n|\\.|$)/i) || 
                               cleanT.match(/(hq\\s*4\\s*arty\\s*bde|leh|ladakh|prayagraj|jammu|buyer\\s*base|consignee\\s*location)/i);
            const trDaysMatch = cleanT.match(/duration\\s+of\\s+training[\\s\\S]{0,30}?(\\d+)\\s*days?/i) || 
                                cleanT.match(/(\\d+)\\s*(?:working\\s*)?days?\\s*training/i);

            const numEmp = trEmpMatch ? `${trEmpMatch[1].trim()} Employees` : "5 Employees";
            const numDays = trDaysMatch ? `${trDaysMatch[1].trim()} Days` : "10 Days";
            let trPlace = "HQ 4 Arty Bde (Consignee Location)";
            if (trLocMatch) {
                const cand = trLocMatch[1].trim().replace(/\\s+/g, ' ');
                if (cand.length >= 3 && cand.length <= 40) trPlace = cand;
            }

            const tInput = document.getElementById('cfgTraining');
            if (tInput) {
                tInput.value = `${trPlace} — ${numDays} (${numEmp})`;
            }"""

if old_analysis_block in html:
    html = html.replace(old_analysis_block, new_analysis_block)
    print("[1/5] executeAnalysis extraction logic updated")
else:
    print("Warning: old_analysis_block not found")

# 2. Update handleVariantChange fallback values
old_variant_change = """        function handleVariantChange() {
            tenderHasBeenAnalyzed = true;
            if (!document.getElementById('cfgWarranty').value) {
                document.getElementById('cfgWarranty').value = "3 Years Comprehensive On-Site";
            }
            if (!document.getElementById('cfgAMC').value) {
                document.getElementById('cfgAMC').value = "2 Years Post-Warranty (48-Hr Turnaround SLA)";
            }
            if (!document.getElementById('cfgTraining').value) {
                document.getElementById('cfgTraining').value = "Buyer Base / High-Altitude (Leh) — 10 Working Days";
            }
            recalculateBOM();
            updateCommercialTermsTable();
        }"""

new_variant_change = """        function handleVariantChange() {
            tenderHasBeenAnalyzed = true;
            if (!document.getElementById('cfgWarranty').value) {
                document.getElementById('cfgWarranty').value = "1 Year from final acceptance at consignee site (Cl 30)";
            }
            if (!document.getElementById('cfgAMC').value) {
                document.getElementById('cfgAMC').value = "Not Required in Tender Scope (Nil AMC / OEM Maintenance Group in India)";
            }
            if (!document.getElementById('cfgTraining').value) {
                document.getElementById('cfgTraining').value = "HQ 4 Arty Bde — 10 Days (5 Employees)";
            }
            recalculateBOM();
            updateCommercialTermsTable();
        }"""

if old_variant_change in html:
    html = html.replace(old_variant_change, new_variant_change)
    print("[2/5] handleVariantChange updated with exact tender defaults")
else:
    print("Warning: old_variant_change not found")

# 3. Update updateCommercialTermsTable rendering
old_terms_table = """            const warranty = document.getElementById('cfgWarranty')?.value || "3 Years Comprehensive On-Site";
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
            `;"""

new_terms_table = """            const warranty = document.getElementById('cfgWarranty')?.value || "1 Year from final acceptance at consignee site (Cl 30)";
            const amc = document.getElementById('cfgAMC')?.value || "Not Required in Tender Scope (Nil AMC / OEM Maintenance Group in India)";
            const training = document.getElementById('cfgTraining')?.value || "HQ 4 Arty Bde — 10 Days (5 Employees)";

            tbody.innerHTML = `
                <tr>
                    <td style="font-weight:700; color:#0f172a;"><i class="fas fa-shield" style="color:#0284c7; margin-right:4px;"></i> Warranty (Cl 30)</td>
                    <td>Comprehensive defect liability covering all components, battery & payloads at consignee location; OEM warranty certificate required</td>
                    <td style="font-weight:800; color:#15803d; background:#f0fdf4;">${warranty}</td>
                    <td style="color:#64748b; font-size:11px;">100% replacement during warranty period</td>
                    <td style="color:#64748b; font-size:11px;">Consignee Destination (On-Site)</td>
                    <td style="text-align:right;"><span class="badge badge-green">MANDATORY (Included)</span></td>
                </tr>
                <tr>
                    <td style="font-weight:700; color:#0f172a;"><i class="fas fa-screwdriver-wrench" style="color:#0284c7; margin-right:4px;"></i> AMC Scope</td>
                    <td>Annual Maintenance Contract requirement as per buyer tender terms. Bidder must maintain dedicated Service & Maintenance Group in India</td>
                    <td style="color:#64748b; font-size:11px;">N/A during warranty</td>
                    <td style="font-weight:800; color:#0369a1; background:#f0f9ff;">${amc}</td>
                    <td style="color:#64748b; font-size:11px;">Service Group in India (Cl 30)</td>
                    <td style="text-align:right;"><span class="badge ${amc.includes('Not Required') ? 'badge-gray' : 'badge-green'}">${amc.includes('Not Required') ? 'NIL IN TENDER' : 'Included'}</span></td>
                </tr>
                <tr>
                    <td style="font-weight:700; color:#0f172a;"><i class="fas fa-graduation-cap" style="color:#0284c7; margin-right:4px;"></i> Training (Cl 16)</td>
                    <td>Mandatory training of operational personnel / operators covering flight navigation, payload controls & 1st line field troubleshooting</td>
                    <td style="color:#64748b; font-size:11px;">Pre-handover & commissioning</td>
                    <td style="color:#64748b; font-size:11px;">Included in standard scope of supply</td>
                    <td style="font-weight:800; color:#b45309; background:#fffbeb;">${training}</td>
                    <td style="text-align:right;"><span class="badge badge-green">MANDATORY (Included)</span></td>
                </tr>
                <tr>
                    <td style="font-weight:700; color:#0f172a;"><i class="fas fa-box-archive" style="color:#0284c7; margin-right:4px;"></i> Shelf Life (Cl 17)</td>
                    <td>Residual market life and guaranteed spares availability: Product/Spare parts must have minimum 3 years shelf life</td>
                    <td style="font-weight:700; color:#15803d;">Active throughout supply life</td>
                    <td style="font-weight:800; color:#0f172a; background:#f8fafc;">Minimum 3 Years Shelf Life (Cl 17)</td>
                    <td style="color:#64748b; font-size:11px;">Pan-India OEM Spares Depot</td>
                    <td style="text-align:right;"><span class="badge badge-green">COMPLIED</span></td>
                </tr>
            `;"""

if old_terms_table in html:
    html = html.replace(old_terms_table, new_terms_table)
    print("[3/5] Commercial terms table updated with exact tender clauses (Cl 30, Cl 16, Cl 17)")
else:
    print("Warning: old_terms_table not found")

# 4. Update Technical Compliance Matrix in complianceModal
old_matrix_clauses = """                { cl: "3.1", req: "Field Operations & Transit Protection", spec: "Supplied in heavy-duty IP67 Pelican/transit hard case with rapid smart balance charger and field tool kit." },
                { cl: "4.1", req: "Warranty Period & Comprehensive Defect Liability", spec: (document.getElementById('cfgWarranty')?.value || "3 Years Comprehensive On-Site") + " — 100% parts, avionics, motor units and battery replacement on-site." },
                { cl: "4.2", req: "Annual Maintenance Contract (AMC) Duration & Terms", spec: (document.getElementById('cfgAMC')?.value || "2 Years Post-Warranty") + " — Scheduled servicing, calibration, depot support, and 48-hr Turnaround SLA." },
                { cl: "4.3", req: "Training Location(s), Syllabus & Number of Days", spec: (document.getElementById('cfgTraining')?.value || "Buyer Base / High-Altitude (Leh) — 10 Working Days") + " — Comprehensive pilot flight ops, simulation, navigation, payload handling & 1st-line maintenance for 10 personnel." }"""

new_matrix_clauses = """                { cl: "3.1", req: "Field Operations & Transit Protection", spec: "Supplied in heavy-duty IP67 Pelican/transit hard case with rapid smart balance charger and field tool kit." },
                { cl: "4.1", req: "Warranty Period (GeM Clause 30)", spec: (document.getElementById('cfgWarranty')?.value || "1 Year from final acceptance at consignee location") + " — Full rectification/replacement of parts during breakdown; OEM warranty certificate furnished at delivery." },
                { cl: "4.2", req: "Annual Maintenance Contract (AMC)", spec: (document.getElementById('cfgAMC')?.value || "Not Required in Tender Scope") + " — Bidder maintains established Installation, Commissioning, Training, Troubleshooting & Maintenance Service group in India (GeM Clause 30)." },
                { cl: "4.3", req: "Training Location(s), Trainees & Days (GeM Clause 16)", spec: (document.getElementById('cfgTraining')?.value || "HQ 4 Arty Bde — 10 Days (5 Employees)") + " — Comprehensive operator training for flight navigation, payload controls & 1st-line maintenance." },
                { cl: "4.4", req: "Product Shelf Life & Residual Life (GeM Clause 17)", spec: "Minimum 3 Years Shelf Life for product and spare parts; product will not be declared end-of-life before this period." }"""

if old_matrix_clauses in html:
    html = html.replace(old_matrix_clauses, new_matrix_clauses)
    print("[4/5] Technical Compliance Matrix updated with Cl 30 (1 Yr Warranty), Nil AMC, and Cl 16 (HQ 4 Arty Bde 10d)")
else:
    print("Warning: old_matrix_clauses not found")

# 5. Update CSV export
old_csv_terms = """            const warrantyVal = document.getElementById('cfgWarranty')?.value || "3 Years Comprehensive On-Site";
            const amcVal = document.getElementById('cfgAMC')?.value || "2 Years Post-Warranty (48h Turnaround SLA)";
            const trainingVal = document.getElementById('cfgTraining')?.value || "Buyer Base / High-Altitude (Leh) — 10 Working Days";

            csv += `CONTRACTUAL & SERVICE TERMS (SEPARATE EVALUATION COLUMNS)\\n`;
            csv += `Parameter,Scope of Obligation,Warranty Period,AMC Duration & Terms,Training Location & Days,Pricing Status\\n`;
            csv += `"Warranty","Comprehensive On-Site Defect Liability & Spares","${warrantyVal}","Included in Warranty Period","Consignee Bases (Pan-India)","Included in Bid"\\n`;
            csv += `"AMC","Post-Warranty Maintenance & Scheduled Calibration","Commences Post-Warranty","${amcVal}","Regional Depot & On-Site","Included in Reserves"\\n`;
            csv += `"Training","Pilot Flight Navigation & 1st Line Maintenance","Pre-Delivery / Handover","Covers 10 Pilots & Techs","${trainingVal}","Included in Package"\\n\\n`;"""

new_csv_terms = """            const warrantyVal = document.getElementById('cfgWarranty')?.value || "1 Year from final acceptance at consignee site (Cl 30)";
            const amcVal = document.getElementById('cfgAMC')?.value || "Not Required in Tender Scope (Nil AMC / OEM Maintenance Group in India)";
            const trainingVal = document.getElementById('cfgTraining')?.value || "HQ 4 Arty Bde — 10 Days (5 Employees)";

            csv += `CONTRACTUAL & SERVICE TERMS (SEPARATE EVALUATION COLUMNS)\\n`;
            csv += `Parameter,Scope of Obligation,Warranty Period,AMC Duration & Terms,Training Location & Days,Pricing Status\\n`;
            csv += `"Warranty (Cl 30)","Comprehensive On-Site Defect Liability & Rectification","${warrantyVal}","Included in Warranty Period","Consignee Site (On-Site)","Included in Bid"\\n`;
            csv += `"AMC Scope","Annual Maintenance Contract Terms","Commences Post-Warranty","${amcVal}","Troubleshooting Service Group in India","${amcVal.includes('Not Required') ? 'Nil in Tender' : 'Included'}"\\n`;
            csv += `"Training (Cl 16)","Operator & Flight Navigation Training","Pre-Handover","Included in Scope of Supply","${trainingVal}","Included in Package"\\n`;
            csv += `"Shelf Life (Cl 17)","Product & Spare Parts Shelf Life","Active Lifecycle","Minimum 3 Years Shelf Life Guarantee","Pan-India Spares Depot","Complied"\\n\\n`;"""

if old_csv_terms in html:
    html = html.replace(old_csv_terms, new_csv_terms)
    print("[5/5] CSV export updated with exact tender terms")
else:
    print("Warning: old_csv_terms not found")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Tender commercial terms accurately updated!")
