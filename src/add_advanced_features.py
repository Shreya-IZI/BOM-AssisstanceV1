import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Header Indicators
old_header = """        <div class="status-indicators">
            <div class="system-pill" style="cursor:pointer;" onclick="openGuideModal()">
                <i class="fas fa-circle-question" style="color:#0284c7;"></i>
                <span style="font-weight:700; color:#0369a1;">User Guide & Help</span>
            </div>
            <div class="system-pill">
                <span class="pill-dot"></span>
                <span>MoD Procurement Standard</span>
            </div>
            <div class="system-pill">
                <span class="pill-dot" style="background:#0284c7;"></span>
                <span>100% Non-Chinese Verified</span>
            </div>
        </div>"""

new_header = """        <div class="status-indicators">
            <div class="system-pill" style="cursor:pointer;" onclick="openGuideModal()">
                <i class="fas fa-circle-question" style="color:#0284c7;"></i>
                <span style="font-weight:700; color:#0369a1;">User Guide</span>
            </div>
            <div class="system-pill" style="cursor:pointer;" onclick="openDraftsModal()">
                <i class="fas fa-folder-open" style="color:#0284c7;"></i>
                <span id="draftsBadgeText" style="font-weight:700; color:#0369a1;">Drafts (0)</span>
            </div>
            <div class="system-pill" style="cursor:pointer; background:#f0fdf4; border-color:#86efac;" onclick="saveTenderDraft()">
                <i class="fas fa-bookmark" style="color:#16a34a;"></i>
                <span style="font-weight:700; color:#15803d;">Save Draft</span>
            </div>
            <div class="system-pill">
                <span class="pill-dot"></span>
                <span>MoD / GeM Compliant</span>
            </div>
            <div class="system-pill">
                <span class="pill-dot" style="background:#0284c7;"></span>
                <span>100% Non-Chinese</span>
            </div>
        </div>"""

if old_header in html:
    html = html.replace(old_header, new_header)
    print("[1/7] Header indicators updated")
else:
    print("Warning: old_header not found")

# 2. Add Commercial Service Adders into TAB 2
old_config = """                        <div style="display:flex; align-items:center; gap:12px; padding-bottom:6px;">
                            <label style="font-size:11px; font-weight:600; display:flex; align-items:center; gap:6px; cursor:pointer;">
                                <input type="checkbox" id="bomNoChina" checked onchange="recalculateBOM()">
                                <span>Zero Chinese Origin (MoD Cl 17)</span>
                            </label>
                            <label style="font-size:11px; font-weight:600; display:flex; align-items:center; gap:6px; cursor:pointer;">
                                <input type="checkbox" id="bomMII" checked onchange="recalculateBOM()">
                                <span>Class 1 Local Supplier (50%+ MII)</span>
                            </label>
                        </div>
                    </div>
                </div>"""

new_config = """                        <div style="display:flex; align-items:center; gap:12px; padding-bottom:6px;">
                            <label style="font-size:11px; font-weight:600; display:flex; align-items:center; gap:6px; cursor:pointer;">
                                <input type="checkbox" id="bomNoChina" checked onchange="recalculateBOM()">
                                <span>Zero Chinese Origin (MoD Cl 17)</span>
                            </label>
                            <label style="font-size:11px; font-weight:600; display:flex; align-items:center; gap:6px; cursor:pointer;">
                                <input type="checkbox" id="bomMII" checked onchange="recalculateBOM()">
                                <span>Class 1 Local Supplier (50%+ MII)</span>
                            </label>
                        </div>
                    </div>

                    <!-- Defense Field Services & Trial Cost Adders -->
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

if old_config in html:
    html = html.replace(old_config, new_config)
    print("[2/7] Service & Field Trial Cost Adders injected")
else:
    print("Warning: old_config not found")

# 3. Add Feature Action Buttons Above BOM Table
old_bom_heading = """                <!-- BOM Table -->
                <div class="data-panel">
                    <div class="panel-heading">
                        <span class="panel-title">Exploded Assembly Hierarchy (Per Drone)</span>
                        <div style="display:flex; gap:8px;">
                            <button type="button" class="btn-secondary" onclick="exportBOMCSV()">Download CSV</button>
                            <button type="button" class="btn-primary" onclick="printOrSavePDF()">Export PDF</button>
                        </div>
                    </div>"""

new_bom_heading = """                <!-- BOM Table -->
                <div class="data-panel">
                    <div class="panel-heading" style="flex-wrap:wrap; gap:10px;">
                        <div>
                            <span class="panel-title">Exploded Assembly Hierarchy (Per Drone)</span>
                            <span id="miiSummaryBadge" class="badge badge-green" style="margin-left:8px; cursor:pointer;" onclick="openMIIModal()">
                                <i class="fas fa-certificate"></i> MII: Calculating...
                            </span>
                        </div>
                        <div style="display:flex; gap:8px; flex-wrap:wrap;">
                            <button type="button" class="btn-secondary" style="background:#f0fdf4; border-color:#86efac; color:#15803d; font-weight:700;" onclick="openMIIModal()">
                                <i class="fas fa-stamp"></i> MII Certificate
                            </button>
                            <button type="button" class="btn-secondary" style="background:#eff6ff; border-color:#93c5fd; color:#1d4ed8; font-weight:700;" onclick="openRAModal()">
                                <i class="fas fa-gavel"></i> Reverse Auction (RA) Simulator
                            </button>
                            <button type="button" class="btn-secondary" style="background:#fefce8; border-color:#fde047; color:#854d0e; font-weight:700;" onclick="openComplianceModal()">
                                <i class="fas fa-list-check"></i> Compliance Matrix
                            </button>
                            <button type="button" class="btn-secondary" onclick="exportBOMCSV()"><i class="fas fa-file-excel"></i> Download CSV</button>
                            <button type="button" class="btn-primary" onclick="printOrSavePDF()"><i class="fas fa-file-pdf"></i> Export PDF</button>
                        </div>
                    </div>"""

if old_bom_heading in html:
    html = html.replace(old_bom_heading, new_bom_heading)
    print("[3/7] Action buttons above BOM table injected")
else:
    print("Warning: old_bom_heading not found")

# 4. Add Compliance Matrix button into TAB 1 footer
old_t1_footer = """                <!-- Quick Step Navigation for Sales -->
                <div class="step-nav-footer">
                    <div style="font-size:12px; color:#64748b;">
                        <i class="fas fa-info-circle" style="color:#0284c7;"></i> Completed scanning tender requirements? Move to Step 2 to calculate the bid price.
                    </div>
                    <button type="button" class="btn-primary" style="padding:8px 18px; font-weight:700;" onclick="switchTab('tab-bom', document.getElementById('nav-step-2'))">
                        Next: Step 2 — Review Price & BOM &rarr;
                    </button>
                </div>"""

new_t1_footer = """                <!-- Quick Step Navigation for Sales -->
                <div class="step-nav-footer">
                    <div style="display:flex; align-items:center; gap:10px;">
                        <button type="button" class="btn-secondary" onclick="openComplianceModal()" style="font-weight:600;">
                            <i class="fas fa-list-check" style="color:#0284c7;"></i> View Compliance Matrix
                        </button>
                        <span style="font-size:12px; color:#64748b;">
                            Ready to price? Move to Step 2 to generate the compliant BOM.
                        </span>
                    </div>
                    <button type="button" class="btn-primary" style="padding:8px 18px; font-weight:700;" onclick="switchTab('tab-bom', document.getElementById('nav-step-2'))">
                        Next: Step 2 — Review Price & BOM &rarr;
                    </button>
                </div>"""

if old_t1_footer in html:
    html = html.replace(old_t1_footer, new_t1_footer)
    print("[4/7] TAB 1 footer updated")
else:
    print("Warning: old_t1_footer not found")

# 5. Inject 4 New Modals before </body>
modals_html = """
    <!-- ================= 1. MAKE IN INDIA (MII) CERTIFICATE MODAL ================= -->
    <div id="miiModal" class="modal-overlay">
        <div class="modal-content" style="max-width: 720px;">
            <div class="modal-header" style="background:#f0fdf4; border-bottom:1px solid #bbf7d0;">
                <span style="display:flex; align-items:center; gap:8px; color:#166534; font-weight:700;">
                    <i class="fas fa-certificate" style="color:#16a34a;"></i> Make in India (MII) Local Content Certificate
                </span>
                <span style="cursor:pointer; font-size:18px; color:#64748b;" onclick="closeMIIModal()">&times;</span>
            </div>
            <div class="modal-body" id="miiCertificateContent" style="padding:20px; font-size:12px; line-height:1.6; max-height:500px; overflow-y:auto;">
                <!-- Populated dynamically -->
            </div>
            <div class="modal-footer" style="display:flex; justify-content:space-between;">
                <button type="button" class="btn-secondary" onclick="copyMIIText()">
                    <i class="fas fa-copy"></i> Copy Undertaking Text
                </button>
                <div style="display:flex; gap:8px;">
                    <button type="button" class="btn-primary" onclick="printMIICertificate()">
                        <i class="fas fa-print"></i> Print Official Certificate
                    </button>
                    <button type="button" class="btn-secondary" onclick="closeMIIModal()">Close</button>
                </div>
            </div>
        </div>
    </div>

    <!-- ================= 2. REVERSE AUCTION (RA) SIMULATOR MODAL ================= -->
    <div id="raModal" class="modal-overlay">
        <div class="modal-content" style="max-width: 680px;">
            <div class="modal-header" style="background:#eff6ff; border-bottom:1px solid #bfdbfe;">
                <span style="display:flex; align-items:center; gap:8px; color:#1e40af; font-weight:700;">
                    <i class="fas fa-gavel" style="color:#2563eb;"></i> Live GeM Reverse Auction (RA) Simulator & Price Floor
                </span>
                <span style="cursor:pointer; font-size:18px; color:#64748b;" onclick="closeRAModal()">&times;</span>
            </div>
            <div class="modal-body" style="padding:18px; font-size:12px; max-height:520px; overflow-y:auto;">
                <!-- Key Price Thresholds Grid -->
                <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:12px; margin-bottom:16px;">
                    <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:6px; padding:10px;">
                        <div style="font-size:10px; font-weight:700; color:#64748b; text-transform:uppercase;">Official GeM Bid (L1 Start)</div>
                        <div id="raStartBid" style="font-size:16px; font-weight:800; color:#0f172a; margin-top:4px;">₹0</div>
                        <div style="font-size:10px; color:#64748b;">Full target margin (incl. GST)</div>
                    </div>
                    <div style="background:#fefce8; border:1px solid #fef08a; border-radius:6px; padding:10px;">
                        <div style="font-size:10px; font-weight:700; color:#854d0e; text-transform:uppercase;">Safe RA Floor (5% Margin)</div>
                        <div id="raSafeFloor" style="font-size:16px; font-weight:800; color:#b45309; margin-top:4px;">₹0</div>
                        <div style="font-size:10px; color:#854d0e;">Minimum recommended stop</div>
                    </div>
                    <div style="background:#fef2f2; border:1px solid #fecaca; border-radius:6px; padding:10px;">
                        <div style="font-size:10px; font-weight:700; color:#991b1b; text-transform:uppercase;">Hard Cost Floor (Break-Even)</div>
                        <div id="raHardFloor" style="font-size:16px; font-weight:800; color:#dc2626; margin-top:4px;">₹0</div>
                        <div style="font-size:10px; color:#991b1b;">WALK-AWAY RED LINE (0% profit)</div>
                    </div>
                </div>

                <!-- Live Competitor Simulator Input -->
                <div style="background:#f1f5f9; border:1px solid #cbd5e1; border-radius:6px; padding:12px; margin-bottom:16px;">
                    <div style="font-weight:700; color:#0f172a; margin-bottom:8px;">Live Auction Interactive Check:</div>
                    <div style="display:flex; gap:12px; align-items:flex-end;">
                        <div style="flex:1;">
                            <label style="font-size:11px; font-weight:600; color:#475569; display:block; margin-bottom:4px;">Current Lowest Competitor Bid on GeM (₹):</label>
                            <input type="number" id="raCompetitorBid" placeholder="e.g. 25000000" oninput="calculateRADecision()" style="width:100%; padding:6px 10px; border:1px solid #94a3b8; border-radius:4px; font-size:13px; font-weight:700;">
                        </div>
                        <div style="width:140px;">
                            <label style="font-size:11px; font-weight:600; color:#475569; display:block; margin-bottom:4px;">Min Decrement %:</label>
                            <input type="number" id="raDecrementPct" value="0.5" step="0.1" min="0.1" max="5" oninput="calculateRADecision()" style="width:100%; padding:6px 10px; border:1px solid #94a3b8; border-radius:4px; font-size:12px; font-weight:600;">
                        </div>
                    </div>
                    <div id="raDecisionBox" style="margin-top:10px; padding:10px; border-radius:4px; font-weight:600; display:none;"></div>
                </div>

                <!-- Next Strategic Decrement Bids Table -->
                <div style="font-weight:700; color:#0f172a; margin-bottom:6px;">Next Strategic Bid Decrement Options:</div>
                <table class="enterprise-table" style="font-size:11px;">
                    <thead>
                        <tr>
                            <th>Step</th>
                            <th>Bid Amount (₹ Incl. GST)</th>
                            <th>Drop from Start</th>
                            <th>Effective Margin</th>
                            <th style="text-align:center;">Action</th>
                        </tr>
                    </thead>
                    <tbody id="raDecrementTableBody"></tbody>
                </table>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn-primary" onclick="closeRAModal()">Done</button>
            </div>
        </div>
    </div>

    <!-- ================= 3. SAVE / LOAD TENDER DRAFTS MODAL ================= -->
    <div id="draftsModal" class="modal-overlay">
        <div class="modal-content" style="max-width: 720px;">
            <div class="modal-header">
                <span style="display:flex; align-items:center; gap:8px;">
                    <i class="fas fa-folder-open" style="color:#0284c7;"></i> Saved Tender Drafts & Versions
                </span>
                <span style="cursor:pointer; font-size:18px;" onclick="closeDraftsModal()">&times;</span>
            </div>
            <div class="modal-body" style="padding:16px; font-size:12px; max-height:480px; overflow-y:auto;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                    <div style="color:#64748b;">Manage your saved tender proposals stored in your browser or import from teammates.</div>
                    <div style="display:flex; gap:8px;">
                        <label class="btn-secondary" style="padding:4px 10px; cursor:pointer; font-size:11px;">
                            <i class="fas fa-file-import"></i> Import JSON
                            <input type="file" id="importDraftInput" accept=".json" onchange="importTenderDraft(event)" style="display:none;">
                        </label>
                        <button type="button" class="btn-primary" style="padding:4px 10px; font-size:11px;" onclick="saveTenderDraft()">
                            <i class="fas fa-plus"></i> Save Current as New
                        </button>
                    </div>
                </div>

                <table class="enterprise-table">
                    <thead>
                        <tr>
                            <th>Tender / Draft Name</th>
                            <th>Date</th>
                            <th>Platform & Qty</th>
                            <th style="text-align:right;">Official Bid (₹)</th>
                            <th style="text-align:center;">Actions</th>
                        </tr>
                    </thead>
                    <tbody id="draftsTableBody"></tbody>
                </table>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn-secondary" onclick="closeDraftsModal()">Close</button>
            </div>
        </div>
    </div>

    <!-- ================= 4. TECHNICAL COMPLIANCE MATRIX MODAL ================= -->
    <div id="complianceModal" class="modal-overlay">
        <div class="modal-content" style="max-width: 860px;">
            <div class="modal-header" style="background:#f8fafc;">
                <span style="display:flex; align-items:center; gap:8px; font-weight:700;">
                    <i class="fas fa-list-check" style="color:#0284c7;"></i> Technical Compliance Matrix (Ministry of Defence / GeM RFP Standard)
                </span>
                <span style="cursor:pointer; font-size:18px;" onclick="closeComplianceModal()">&times;</span>
            </div>
            <div class="modal-body" style="padding:16px; font-size:12px; max-height:500px; overflow-y:auto;">
                <div style="background:#eff6ff; border:1px solid #bfdbfe; border-radius:6px; padding:10px 14px; margin-bottom:12px; color:#1e40af; font-size:11px;">
                    <i class="fas fa-info-circle"></i> This matrix maps tender technical specifications against our 100% non-Chinese compliant drone configuration. You can download as Excel CSV or copy directly into your GeM technical bid envelope.
                </div>
                <table class="enterprise-table" id="complianceTable">
                    <thead>
                        <tr>
                            <th style="width:50px;">Cl #</th>
                            <th style="width:220px;">Tender Specification / Requirement</th>
                            <th style="width:100px; text-align:center;">Compliance</th>
                            <th>Offered Specification & Supporting Proof</th>
                        </tr>
                    </thead>
                    <tbody id="complianceTableBody"></tbody>
                </table>
            </div>
            <div class="modal-footer" style="display:flex; justify-content:space-between;">
                <button type="button" class="btn-secondary" onclick="copyComplianceTable()">
                    <i class="fas fa-copy"></i> Copy to Clipboard (Word/Excel)
                </button>
                <div style="display:flex; gap:8px;">
                    <button type="button" class="btn-secondary" onclick="downloadComplianceCSV()">
                        <i class="fas fa-file-excel"></i> Download CSV
                    </button>
                    <button type="button" class="btn-primary" onclick="printComplianceSheet()">
                        <i class="fas fa-print"></i> Print Compliance Sheet
                    </button>
                    <button type="button" class="btn-secondary" onclick="closeComplianceModal()">Close</button>
                </div>
            </div>
        </div>
    </div>
"""

if '<!-- ================= 1. MAKE IN INDIA (MII) CERTIFICATE MODAL ================= -->' not in html:
    html = html.replace('</body>', modals_html + '\n</body>')
    print("[5/7] 4 New Modals injected")
else:
    print("Warning: Modals already present")

# 6. Update recalculateBOM
old_recalc = """            const totalHW = unitBOM * qty;
            const warranty = totalHW * 0.05;
            const contingency = totalHW * 0.04;
            const inspection = 35000;
            const totalProjectCost = totalHW + warranty + contingency + inspection;

            const bidExGST = totalProjectCost * (1 + margin / 100);
            const gst = bidExGST * 0.18;
            const bidIncGST = bidExGST + gst;

            document.getElementById('priceUnitBOM').innerText = "₹" + Math.round(unitBOM).toLocaleString('en-IN');
            document.getElementById('priceTotalCost').innerText = "₹" + Math.round(totalProjectCost).toLocaleString('en-IN');
            document.getElementById('priceBidEx').innerText = "₹" + Math.round(bidExGST).toLocaleString('en-IN');
            document.getElementById('priceBidInc').innerText = "₹" + Math.round(bidIncGST).toLocaleString('en-IN');"""

new_recalc = """            // Defense Service Adders
            const trialAdder = document.getElementById('chkTrials')?.checked ? 250000 : 0;
            const trainingAdder = document.getElementById('chkTraining')?.checked ? 120000 : 0;
            const cratingAdder = document.getElementById('chkCrating')?.checked ? 85000 : 0;
            const serviceAdders = trialAdder + trainingAdder + cratingAdder;

            const totalHW = unitBOM * qty;
            const warranty = totalHW * 0.05;
            const contingency = totalHW * 0.04;
            const inspection = 35000;
            const totalProjectCost = totalHW + warranty + contingency + inspection + serviceAdders;

            const bidExGST = totalProjectCost * (1 + margin / 100);
            const gst = bidExGST * 0.18;
            const bidIncGST = bidExGST + gst;

            // Global cache for RA simulator & drafts
            window.currentProjectCost = totalProjectCost;
            window.currentOfficialBid = bidIncGST;

            document.getElementById('priceUnitBOM').innerText = "₹" + Math.round(unitBOM).toLocaleString('en-IN');
            document.getElementById('priceTotalCost').innerText = "₹" + Math.round(totalProjectCost).toLocaleString('en-IN');
            document.getElementById('priceBidEx').innerText = "₹" + Math.round(bidExGST).toLocaleString('en-IN');
            document.getElementById('priceBidInc').innerText = "₹" + Math.round(bidIncGST).toLocaleString('en-IN');

            // Update MII badge above BOM table
            const miiInfo = calculateLocalContent();
            const miiBadge = document.getElementById('miiSummaryBadge');
            if (miiBadge) {
                miiBadge.innerText = `MII: ${miiInfo.pct.toFixed(1)}% (${miiInfo.isClass1 ? 'Class-I' : 'Class-II'})`;
                miiBadge.className = `badge ${miiInfo.isClass1 ? 'badge-green' : 'badge-amber'}`;
            }"""

if old_recalc in html:
    html = html.replace(old_recalc, new_recalc)
    print("[6/7] recalculateBOM updated")
else:
    print("Warning: old_recalc not found")

# 7. Inject JS Logic right before window.onload = function() {
target_onload = """        window.onload = function() {
            recalculateBOM();"""

js_logic = """
        // ================= ADVANCED FEATURE LOGIC ================= //

        // 1. MAKE IN INDIA (MII) LOCAL CONTENT & CERTIFICATE
        function openMIIModal() {
            renderMIICertificate();
            document.getElementById('miiModal').classList.add('open');
        }
        function closeMIIModal() { document.getElementById('miiModal').classList.remove('open'); }

        function calculateLocalContent() {
            let totalBOM = 0;
            let localBOM = 0;
            if (currentBOM && currentBOM.length > 0) {
                currentBOM.forEach(it => {
                    const ext = (it.qty || 1) * (it.cost || 0);
                    totalBOM += ext;
                    if (it.origin === 'India') localBOM += ext;
                });
            }
            const pct = totalBOM > 0 ? (localBOM / totalBOM) * 100 : 0;
            const isClass1 = pct >= 50;
            const isClass2 = pct >= 20 && pct < 50;
            const supplierClass = isClass1 ? "Class-I Local Supplier (MII >= 50%)" : (isClass2 ? "Class-II Local Supplier (20% - 49%)" : "Non-Local Supplier (<20%)");
            return { totalBOM, localBOM, pct, isClass1, isClass2, supplierClass };
        }

        function renderMIICertificate() {
            const mii = calculateLocalContent();
            const variant = document.getElementById('bomVariant').value;
            const variantName = FLEET_VARIANTS[variant] ? FLEET_VARIANTS[variant].name : variant;
            const qty = parseInt(document.getElementById('bomQty').value) || 1;
            const today = new Date().toLocaleDateString('en-IN', { day:'numeric', month:'long', year:'numeric' });

            const container = document.getElementById('miiCertificateContent');
            if (!container) return;

            let rows = '';
            currentBOM.forEach((it, idx) => {
                const ext = it.qty * it.cost;
                rows += `
                    <tr>
                        <td>${idx + 1}</td>
                        <td style="font-weight:600;">${it.cat}</td>
                        <td>${it.name}</td>
                        <td style="text-align:center;"><span class="badge ${it.origin === 'India' ? 'badge-green' : 'badge-gray'}">${it.origin}</span></td>
                        <td style="text-align:right;">₹${ext.toLocaleString('en-IN')}</td>
                        <td style="text-align:center;">${it.origin === 'India' ? '<i class=\"fas fa-check\" style=\"color:#16a34a;\"></i> Local' : 'Imported'}</td>
                    </tr>
                `;
            });

            container.innerHTML = `
                <div style="border:2px solid #0f172a; padding:24px; background:#ffffff; border-radius:4px; font-family:serif;">
                    <div style="text-align:center; border-bottom:2px solid #0f172a; padding-bottom:12px; margin-bottom:16px;">
                        <h2 style="margin:0; font-size:18px; text-transform:uppercase; letter-spacing:1px; color:#0f172a;">FORMAL LOCAL CONTENT SELF-CERTIFICATION UNDER MAKE IN INDIA</h2>
                        <div style="font-size:11px; font-style:italic; color:#475569; margin-top:4px;">
                            In accordance with DPIIT Public Procurement Order P-45021/2/2017-PP (BE-II) & Ministry of Defence Directives
                        </div>
                    </div>

                    <div style="display:flex; justify-content:space-between; font-size:11px; margin-bottom:14px; font-family:sans-serif;">
                        <div><strong>Date:</strong> ${today}</div>
                        <div><strong>Tender Quantity:</strong> ${qty} Systems</div>
                        <div><strong>Target Platform:</strong> ${variantName}</div>
                    </div>

                    <div style="background:#f0fdf4; border:1px solid #86efac; border-radius:6px; padding:12px; margin-bottom:16px; font-family:sans-serif;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div>
                                <span style="font-size:11px; font-weight:700; color:#15803d; text-transform:uppercase;">Certified Local Content Percentage:</span>
                                <div style="font-size:24px; font-weight:900; color:#14532d;">${mii.pct.toFixed(1)}%</div>
                            </div>
                            <div style="text-align:right;">
                                <span class="badge ${mii.isClass1 ? 'badge-green' : 'badge-amber'}" style="font-size:12px; padding:6px 12px;">
                                    ${mii.supplierClass}
                                </span>
                                <div style="font-size:10px; color:#15803d; margin-top:4px;">100% Non-Chinese Verified (MoD Cl 17 Compliant)</div>
                            </div>
                        </div>
                    </div>

                    <p style="text-indent:24px; margin-bottom:12px;">
                        We hereby solemnly declare and certify that the offered <strong>${variantName}</strong> multirotor drone system meets the mandatory local content threshold prescribed for <strong>${mii.supplierClass}</strong> under the Public Procurement (Preference to Make in India) Order.
                    </p>

                    <p style="text-indent:24px; margin-bottom:14px;">
                        The total direct hardware cost is <strong>₹${Math.round(mii.totalBOM).toLocaleString('en-IN')}</strong> per drone, of which <strong>₹${Math.round(mii.localBOM).toLocaleString('en-IN')} (${mii.pct.toFixed(1)}%)</strong> constitutes indigenous domestic value addition. All local manufacturing, printed circuit board integration, airframe milling, proprietary flight software compilation, calibration, and environmental testing are executed at our facility in India.
                    </p>

                    <div style="margin-bottom:16px;">
                        <strong style="font-size:11px; font-family:sans-serif; text-transform:uppercase; color:#0f172a;">Subsystem Breakdown:</strong>
                        <table class="enterprise-table" style="font-size:10px; margin-top:6px; font-family:sans-serif;">
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Subsystem</th>
                                    <th>Specification / Part</th>
                                    <th style="text-align:center;">Country of Origin</th>
                                    <th style="text-align:right;">Total (₹)</th>
                                    <th style="text-align:center;">Local Qualifying</th>
                                </tr>
                            </thead>
                            <tbody>${rows}</tbody>
                        </table>
                    </div>

                    <div style="margin-top:36px; display:flex; justify-content:space-between; font-family:sans-serif; font-size:11px;">
                        <div>
                            <div>________________________________________</div>
                            <div style="font-weight:700; margin-top:4px;">Authorized Signatory</div>
                            <div style="color:#64748b;">Defence & Aerospace Bidding Division</div>
                        </div>
                        <div style="text-align:right;">
                            <div>[ OFFICIAL COMPANY SEAL ]</div>
                            <div style="color:#64748b; margin-top:4px;">Place: New Delhi / Bengaluru, India</div>
                        </div>
                    </div>
                </div>
            `;
        }

        function copyMIIText() {
            const mii = calculateLocalContent();
            const variant = document.getElementById('bomVariant').value;
            const variantName = FLEET_VARIANTS[variant] ? FLEET_VARIANTS[variant].name : variant;
            const text = "MAKE IN INDIA LOCAL CONTENT SELF-CERTIFICATION\\n\\nWe hereby confirm and declare that the product '" + variantName + "' offered against the GeM tender contains " + mii.pct.toFixed(1) + "% Local Content, qualifying us as a '" + mii.supplierClass + "' under DPIIT Order P-45021/2/2017-PP (BE-II). 100% of the assembly, firmware integration, and environmental testing is completed in India, with Zero Chinese Origin components.";
            navigator.clipboard.writeText(text).then(() => alert("MII Undertaking text copied to clipboard!"));
        }

        function printMIICertificate() {
            const printContent = document.getElementById('miiCertificateContent').innerHTML;
            const w = window.open('', '', 'width=800,height=900');
            w.document.write('<html><head><title>MII Local Content Certificate</title>');
            w.document.write('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">');
            w.document.write('<style>body{font-family:serif;padding:30px;color:#000;} table{width:100%;border-collapse:collapse;} th,td{border:1px solid #ccc;padding:6px;font-size:11px;} th{background:#eee;} .badge{border:1px solid #999;padding:2px 6px;border-radius:3px;font-size:10px;}</style>');
            w.document.write('</head><body>' + printContent + '</body></html>');
            w.document.close();
            w.print();
        }

        // 2. REVERSE AUCTION (RA) SIMULATOR
        function openRAModal() {
            const totalProjectCost = window.currentProjectCost || 0;
            const bidIncGST = window.currentOfficialBid || 0;

            const hardFloor = totalProjectCost * 1.18; // Cost + 18% GST (Break-Even)
            const safeFloor = (totalProjectCost * 1.05) * 1.18; // Cost + 5% reserve + 18% GST

            document.getElementById('raStartBid').innerText = "₹" + Math.round(bidIncGST).toLocaleString('en-IN');
            document.getElementById('raSafeFloor').innerText = "₹" + Math.round(safeFloor).toLocaleString('en-IN');
            document.getElementById('raHardFloor').innerText = "₹" + Math.round(hardFloor).toLocaleString('en-IN');

            const compInput = document.getElementById('raCompetitorBid');
            if (!compInput.value || parseFloat(compInput.value) <= 0) {
                compInput.value = Math.round(bidIncGST * 0.98); // prefill with 2% undercut
            }

            calculateRADecision();
            renderRADecrementTable(bidIncGST, hardFloor, safeFloor);
            document.getElementById('raModal').classList.add('open');
        }
        function closeRAModal() { document.getElementById('raModal').classList.remove('open'); }

        function calculateRADecision() {
            const competitor = parseFloat(document.getElementById('raCompetitorBid').value) || 0;
            const totalProjectCost = window.currentProjectCost || 0;
            const bidIncGST = window.currentOfficialBid || 0;
            const hardFloor = totalProjectCost * 1.18;
            const safeFloor = (totalProjectCost * 1.05) * 1.18;
            const decBox = document.getElementById('raDecisionBox');

            if (!decBox) return;
            decBox.style.display = 'block';

            if (competitor <= 0) {
                decBox.style.display = 'none';
                return;
            }

            if (competitor > bidIncGST) {
                decBox.style.background = '#dcfce7';
                decBox.style.color = '#15803d';
                decBox.style.border = '1px solid #86efac';
                decBox.innerHTML = `🟢 <strong>You are in L1 position!</strong> Competitor is bidding higher than your standard quotation. No need to drop price.`;
            } else if (competitor > safeFloor) {
                const nextBid = Math.round(competitor * 0.995);
                decBox.style.background = '#fefce8';
                decBox.style.color = '#854d0e';
                decBox.style.border = '1px solid #fde047';
                decBox.innerHTML = `🟡 <strong>Competitive Zone:</strong> You can safely match or undercut by 0.5%. Recommended Next Bid: <strong style="font-size:14px; color:#0f172a;">₹${nextBid.toLocaleString('en-IN')}</strong>. Plenty of healthy margin remaining!`;
            } else if (competitor > hardFloor) {
                const nextBid = Math.round(competitor * 0.995);
                decBox.style.background = '#fff7ed';
                decBox.style.color = '#c2410c';
                decBox.style.border = '1px solid #fdba74';
                decBox.innerHTML = `🟠 <strong>CAUTION — Thin Margin Zone:</strong> Competitor has pushed below safe 5% margin. If you must win, final bid: <strong style="font-size:14px; color:#c2410c;">₹${nextBid.toLocaleString('en-IN')}</strong>. Do not go further!`;
            } else {
                decBox.style.background = '#fef2f2';
                decBox.style.color = '#991b1b';
                decBox.style.border = '1px solid #fca5a5';
                decBox.innerHTML = `🔴 <strong>⛔ STOP BIDDING IMMEDIATELY:</strong> Competitor bid (₹${competitor.toLocaleString('en-IN')}) is below your absolute cost floor (₹${Math.round(hardFloor).toLocaleString('en-IN')}). If you match this, the company will lose cash. Let competitor take this contract at a loss!`;
            }
        }

        function renderRADecrementTable(startBid, hardFloor, safeFloor) {
            const tbody = document.getElementById('raDecrementTableBody');
            if (!tbody) return;
            tbody.innerHTML = '';

            const steps = [0.005, 0.01, 0.015, 0.02, 0.03, 0.05];
            steps.forEach((s, idx) => {
                const bidVal = Math.round(startBid * (1 - s));
                const diff = startBid - bidVal;
                let statusBadge = '';
                if (bidVal > safeFloor) {
                    statusBadge = '<span class="badge badge-green">Healthy</span>';
                } else if (bidVal > hardFloor) {
                    statusBadge = '<span class="badge badge-amber">Slim</span>';
                } else {
                    statusBadge = '<span class="badge" style="background:#fecaca; color:#991b1b;">Loss Maker</span>';
                }

                tbody.innerHTML += `
                    <tr>
                        <td style="font-weight:700;">-${(s * 100).toFixed(1)}%</td>
                        <td style="font-weight:700; font-size:12px;">₹${bidVal.toLocaleString('en-IN')}</td>
                        <td style="color:#64748b;">-₹${diff.toLocaleString('en-IN')}</td>
                        <td>${statusBadge}</td>
                        <td style="text-align:center;">
                            <button class="btn-secondary" style="padding:2px 8px; font-size:11px;" onclick="navigator.clipboard.writeText('${bidVal}').then(()=>alert('Bid ₹${bidVal.toLocaleString('en-IN')} copied to clipboard!'))">
                                <i class="fas fa-copy"></i> Copy
                            </button>
                        </td>
                    </tr>
                `;
            });
        }

        // 3. SAVE / LOAD TENDER DRAFTS
        const DRAFT_STORAGE_KEY = 'bom_assist_saved_drafts';

        function getSavedDrafts() {
            try {
                return JSON.parse(localStorage.getItem(DRAFT_STORAGE_KEY)) || [];
            } catch(e) {
                return [];
            }
        }

        function updateDraftCount() {
            const drafts = getSavedDrafts();
            const badge = document.getElementById('draftsBadgeText');
            if (badge) badge.innerText = `Drafts (${drafts.length})`;
        }

        function saveTenderDraft() {
            const variant = document.getElementById('bomVariant').value;
            const qty = parseInt(document.getElementById('bomQty').value) || 1;
            const margin = parseInt(document.getElementById('bomMargin').value) || 25;
            const specText = document.getElementById('specInput').value;
            const dateStr = new Date().toLocaleDateString('en-IN', { day:'2-digit', month:'short', year:'numeric', hour:'2-digit', minute:'2-digit' });

            const defaultTitle = `Tender_${variant}_${qty}u_${new Date().toISOString().slice(0,10)}`;
            const title = prompt("Enter a name for this tender draft:", defaultTitle);
            if (!title) return;

            const draft = {
                id: Date.now(),
                title: title.trim(),
                date: dateStr,
                variant: variant,
                qty: qty,
                margin: margin,
                specText: specText,
                trials: document.getElementById('chkTrials')?.checked || false,
                training: document.getElementById('chkTraining')?.checked || false,
                crating: document.getElementById('chkCrating')?.checked || false,
                sourcingGaps: sourcingGaps,
                officialBid: window.currentOfficialBid || 0
            };

            const drafts = getSavedDrafts();
            drafts.unshift(draft);
            localStorage.setItem(DRAFT_STORAGE_KEY, JSON.stringify(drafts));
            updateDraftCount();
            alert(`Draft "${draft.title}" saved successfully!`);
        }

        function openDraftsModal() {
            renderDraftsList();
            document.getElementById('draftsModal').classList.add('open');
        }
        function closeDraftsModal() { document.getElementById('draftsModal').classList.remove('open'); }

        function renderDraftsList() {
            const drafts = getSavedDrafts();
            const tbody = document.getElementById('draftsTableBody');
            if (!tbody) return;
            tbody.innerHTML = '';

            if (drafts.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="5" style="text-align:center; padding:32px 16px; color:#94a3b8; font-style:italic;">
                            No saved drafts found. Click "Save Current as New" to bookmark your active tender.
                        </td>
                    </tr>
                `;
                return;
            }

            drafts.forEach(d => {
                tbody.innerHTML += `
                    <tr>
                        <td style="font-weight:700; color:#0f172a;">${d.title}</td>
                        <td style="color:#64748b; font-size:11px;">${d.date}</td>
                        <td style="font-size:11px;">${d.variant} (${d.qty} Units)</td>
                        <td style="text-align:right; font-weight:700; color:#15803d;">₹${Math.round(d.officialBid || 0).toLocaleString('en-IN')}</td>
                        <td style="text-align:center;">
                            <div style="display:inline-flex; gap:6px;">
                                <button class="btn-primary" style="padding:2px 8px; font-size:11px;" onclick="loadDraftById(${d.id})">Load</button>
                                <button class="btn-secondary" style="padding:2px 8px; font-size:11px;" onclick="exportDraftJSON(${d.id})"><i class="fas fa-download"></i></button>
                                <button class="btn-secondary" style="padding:2px 8px; font-size:11px; color:#dc2626;" onclick="deleteDraftById(${d.id})"><i class="fas fa-trash"></i></button>
                            </div>
                        </td>
                    </tr>
                `;
            });
        }

        function loadDraftById(id) {
            const drafts = getSavedDrafts();
            const draft = drafts.find(d => d.id === id);
            if (!draft) return;

            if (draft.specText) {
                document.getElementById('specInput').value = draft.specText;
                updateCharCount();
            }
            if (draft.variant) document.getElementById('bomVariant').value = draft.variant;
            if (draft.qty) document.getElementById('bomQty').value = draft.qty;
            if (draft.margin) document.getElementById('bomMargin').value = draft.margin;

            if (document.getElementById('chkTrials')) document.getElementById('chkTrials').checked = !!draft.trials;
            if (document.getElementById('chkTraining')) document.getElementById('chkTraining').checked = !!draft.training;
            if (document.getElementById('chkCrating')) document.getElementById('chkCrating').checked = !!draft.crating;

            if (draft.sourcingGaps && Array.isArray(draft.sourcingGaps)) {
                sourcingGaps = draft.sourcingGaps;
                renderGaps();
            }

            tenderHasBeenAnalyzed = true;
            recalculateBOM();
            closeDraftsModal();
            switchTab('tab-bom', document.getElementById('nav-step-2'));
            alert(`Tender Draft "${draft.title}" loaded successfully!`);
        }

        function deleteDraftById(id) {
            if (!confirm("Are you sure you want to delete this draft?")) return;
            let drafts = getSavedDrafts();
            drafts = drafts.filter(d => d.id !== id);
            localStorage.setItem(DRAFT_STORAGE_KEY, JSON.stringify(drafts));
            renderDraftsList();
            updateDraftCount();
        }

        function exportDraftJSON(id) {
            const drafts = getSavedDrafts();
            const draft = drafts.find(d => d.id === id);
            if (!draft) return;
            const blob = new Blob([JSON.stringify(draft, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${draft.title.replace(/[^a-zA-Z0-9_-]/g, '_')}.json`;
            a.click();
            URL.revokeObjectURL(url);
        }

        function importTenderDraft(e) {
            const file = e.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = function(evt) {
                try {
                    const parsed = JSON.parse(evt.target.result);
                    if (!parsed.variant) throw new Error("Invalid draft file structure");
                    parsed.id = Date.now();
                    parsed.title = "(Imported) " + (parsed.title || "Tender Draft");
                    const drafts = getSavedDrafts();
                    drafts.unshift(parsed);
                    localStorage.setItem(DRAFT_STORAGE_KEY, JSON.stringify(drafts));
                    renderDraftsList();
                    updateDraftCount();
                    alert("Draft imported successfully!");
                } catch(err) {
                    alert("Failed to parse JSON draft: " + err.message);
                }
            };
            reader.readAsText(file);
        }

        // 4. TECHNICAL COMPLIANCE MATRIX GENERATOR
        function openComplianceModal() {
            renderComplianceMatrix();
            document.getElementById('complianceModal').classList.add('open');
        }
        function closeComplianceModal() { document.getElementById('complianceModal').classList.remove('open'); }

        function renderComplianceMatrix() {
            const variant = document.getElementById('bomVariant').value;
            const variantName = FLEET_VARIANTS[variant] ? FLEET_VARIANTS[variant].name : variant;
            const tbody = document.getElementById('complianceTableBody');
            if (!tbody) return;
            tbody.innerHTML = '';

            const clauses = [
                { cl: "1.1", req: "Country of Origin & Security Restrictions", spec: "100% Non-Chinese origin components. Strictly compliant with Ministry of Defence Clause 17 & DPIIT restrictions." },
                { cl: "1.2", req: "Make in India (MII) Purchase Preference", spec: "Class-I Local Supplier (MII >= 50%). Domestic design, fabrication, and firmware compilation in India." },
                { cl: "2.1", req: "Airframe Structure & Payload Mounts", spec: "Military-grade 3K woven carbon fiber composite frame with quick-release arms and IP54/IP67 weather sealing." },
                { cl: "2.2", req: "Propulsion Motors & Electronic Speed Controllers", spec: "High-efficiency BLDC brushless propulsion units paired with industrial 45A-80A ESCs and folding carbon propellers." },
                { cl: "2.3", req: "Flight Controller & Autonomous Navigation", spec: "Triple-redundant IMU autopilot with fail-safe return-to-home, geo-fencing, and autonomous mission waypoint sequencing." },
                { cl: "2.4", req: "Global Navigation Satellite System (GNSS)", spec: "Dual GPS/GLONASS + NavIC L5 positioning receiver with anti-spoofing and jam-resistant RF shielding." },
                { cl: "2.5", req: "Day/Night Electro-Optical (EO/IR) Payload", spec: "Integrated dual-sensor gyro-stabilized gimbal with optical zoom and long-wave infrared (LWIR) thermal core." },
                { cl: "2.6", req: "C2 Datalink & Ground Control Station (GCS)", spec: "Military AES-128/256 encrypted datalink with 10km+ telemetry and ruggedized sunlight-readable handheld GCS." },
                { cl: "3.1", req: "Field Operations & Transit Protection", spec: "Supplied in heavy-duty IP67 Pelican/transit hard case with rapid smart balance charger and field tool kit." },
                { cl: "4.1", req: "Warranty, Spares Support & Liquidated Damages", spec: "Comprehensive 1 to 3-year on-site replacement warranty with guaranteed spares availability for 5 years." }
            ];

            clauses.forEach(c => {
                tbody.innerHTML += `
                    <tr>
                        <td style="font-weight:700; color:#475569;">${c.cl}</td>
                        <td style="font-weight:600; color:#0f172a;">${c.req}</td>
                        <td style="text-align:center;"><span class="badge badge-green" style="font-weight:800;">COMPLIED</span></td>
                        <td style="color:#334155;">${c.spec}</td>
                    </tr>
                `;
            });
        }

        function downloadComplianceCSV() {
            const variant = document.getElementById('bomVariant').value;
            let csv = "TECHNICAL COMPLIANCE MATRIX — " + variant + "\\n";
            csv += "Clause #,Tender Requirement,Compliance Status,Offered Specification\\n";
            const rows = document.querySelectorAll('#complianceTableBody tr');
            rows.forEach(r => {
                const cols = r.querySelectorAll('td');
                if (cols.length >= 4) {
                    const cl = cols[0].innerText.trim();
                    const req = cols[1].innerText.trim().replace(/"/g, '""');
                    const comp = cols[2].innerText.trim();
                    const spec = cols[3].innerText.trim().replace(/"/g, '""');
                    csv += '"' + cl + '","' + req + '","' + comp + '","' + spec + '"\\n';
                }
            });
            const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `Technical_Compliance_Matrix_${variant}.csv`;
            a.click();
            URL.revokeObjectURL(url);
        }

        function copyComplianceTable() {
            let text = "Clause #\\tTender Requirement\\tCompliance Status\\tOffered Specification\\n";
            const rows = document.querySelectorAll('#complianceTableBody tr');
            rows.forEach(r => {
                const cols = r.querySelectorAll('td');
                if (cols.length >= 4) {
                    text += cols[0].innerText.trim() + "\\t" + cols[1].innerText.trim() + "\\t" + cols[2].innerText.trim() + "\\t" + cols[3].innerText.trim() + "\\n";
                }
            });
            navigator.clipboard.writeText(text).then(() => alert("Compliance matrix copied to clipboard! You can now paste directly into Microsoft Word or Excel."));
        }

        function printComplianceSheet() {
            const content = document.getElementById('complianceTable').outerHTML;
            const w = window.open('', '', 'width=900,height=900');
            w.document.write('<html><head><title>Technical Compliance Matrix</title>');
            w.document.write('<style>body{font-family:sans-serif;padding:30px;color:#0f172a;} table{width:100%;border-collapse:collapse;margin-top:16px;} th,td{border:1px solid #cbd5e1;padding:8px;font-size:11px;} th{background:#f1f5f9;font-weight:700;} .badge{background:#dcfce7;color:#15803d;padding:2px 6px;border-radius:3px;font-weight:700;}</style>');
            w.document.write('</head><body><h2 style="margin:0;">TECHNICAL COMPLIANCE STATEMENT</h2><p style="color:#64748b;font-size:12px;">Ministry of Defence / GeM Procurement Format</p>' + content + '</body></html>');
            w.document.close();
            w.print();
        }
"""

new_onload = js_logic + """
        window.onload = function() {
            updateDraftCount();
            recalculateBOM();"""

if target_onload in html:
    html = html.replace(target_onload, new_onload)
    print("[7/7] Advanced JS logic injected before window.onload")
else:
    print("Warning: target_onload not found")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Script execution completed!")
