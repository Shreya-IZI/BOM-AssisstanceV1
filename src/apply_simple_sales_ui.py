import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update CATEGORIES.TECHNICAL_HARDWARE with strict word boundaries
old_cat_hw = """            TECHNICAL_HARDWARE: [
                { name: "Airframe Assembly", rx: /frame|airframe|carbon/i },
                { name: "Propulsion Motor Units", rx: /motor|bldc|kv/i },
                { name: "Aerodynamic Propeller Sets", rx: /propeller|prop\\b|prop set/i },
                { name: "Electronic Speed Controllers (ESC)", rx: /esc\\b|speed controller/i },
                { name: "Autopilot Flight Controller", rx: /flight controller|autopilot|pixhawk|cube/i },
                { name: "Electro-Optical / IR Gimbal", rx: /camera|payload|gimbal|eo|ir|lwir|thermal|lrf/i },
                { name: "GPS / NavIC Receiver", rx: /gps|gnss|rtk|navic/i },
                { name: "Main Propulsion Battery Pack", rx: /battery|lipo|li-ion|mah|cell/i },
                { name: "C2 Datalink & Ground Station", rx: /radio controller|transmitter|gcs|datalink/i },
                { name: "Ordnance Release Mechanism", rx: /release mechanism|ordnance|payload holder|drop/i },
                { name: "Field Balance Charger", rx: /charger|balance charger/i },
                { name: "Military Transit Case (IP67)", rx: /hard case|transport case|box/i },
                { name: "Maintenance & Tool Kit", rx: /tool set|tools|kit|accessories/i },
                { name: "Technical Manuals & Logbook", rx: /log book|logbook|manual/i }
            ]"""

new_cat_hw = """            TECHNICAL_HARDWARE: [
                { name: "Airframe Assembly", rx: /\\b(airframe|carbon\\s*fiber\\s*frame|drone\\s*frame|chassis)\\b/i },
                { name: "Propulsion Motor Units", rx: /\\b(bldc|brushless\\s*motor|propulsion\\s*motor|\\d{4}\\s*kv)\\b/i },
                { name: "Aerodynamic Propeller Sets", rx: /\\b(propeller|folding\\s*prop|\\bprops\\b)\\b/i },
                { name: "Electronic Speed Controllers (ESC)", rx: /\\b(esc|speed\\s*controller|4-in-1\\s*esc)\\b/i },
                { name: "Autopilot Flight Controller", rx: /\\b(autopilot|flight\\s*controller|pixhawk|cube\\s*orange|agam)\\b/i },
                { name: "Electro-Optical / IR Gimbal", rx: /\\b(gimbal|eo\\/?ir|thermal\\s*camera|lwir|night\\s*vision|optical\\s*zoom|day[-\\s]?night\\s*camera)\\b/i },
                { name: "GPS / NavIC Receiver", rx: /\\b(navic|gnss|rtk\\s*gps|anti[-\\s]?jam\\s*gps|crpa)\\b/i },
                { name: "Main Propulsion Battery Pack", rx: /\\b(lipo|li-ion|solid\\s*state\\s*battery|propulsion\\s*battery|\\d{4,6}\\s*mah)\\b/i },
                { name: "C2 Datalink & Ground Station", rx: /\\b(gcs|ground\\s*control|datalink|telemetry|radio\\s*controller|handheld\\s*gcs)\\b/i },
                { name: "Ordnance Release Mechanism", rx: /\\b(release\\s*mechanism|servo\\s*release|bomb\\s*drop|payload\\s*dropper)\\b/i },
                { name: "Field Balance Charger", rx: /\\b(balance\\s*charger|battery\\s*charger|smart\\s*charger)\\b/i },
                { name: "Military Transit Case (IP67)", rx: /\\b(transit\\s*case|ip67\\s*case|pelican\\s*case|transport\\s*case|hard\\s*case)\\b/i },
                { name: "Maintenance & Tool Kit", rx: /\\b(maintenance\\s*kit|tool\\s*kit|spares\\s*kit|field\\s*repair\\s*kit)\\b/i },
                { name: "Technical Manuals & Logbook", rx: /\\b(technical\\s*manual|operator\\s*manual|maintenance\\s*manual|log\\s*book|user\\s*manual)\\b/i }
            ]"""

if old_cat_hw in html:
    html = html.replace(old_cat_hw, new_cat_hw)
    print("Updated CATEGORIES.TECHNICAL_HARDWARE regexes")
else:
    print("Warning: old_cat_hw not found in html")

# 2. Add CSS for Stepper, Arrows, and Sales Guides
stepper_css = """
        /* ================= SALES STEPPER & PROCEDURE UI ================= */
        .workflow-banner {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 16px 20px;
            margin-bottom: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        }

        .workflow-title-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 12px;
            padding-bottom: 10px;
            border-bottom: 1px solid #f1f5f9;
        }

        .workflow-title {
            font-size: 13px;
            font-weight: 700;
            color: #0f172a;
            display: flex;
            align-items: center;
            gap: 8px;
            letter-spacing: 0.3px;
        }

        .workflow-stepper {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
        }

        .step-card {
            flex: 1;
            background: #f8fafc;
            border: 1.5px solid #e2e8f0;
            border-radius: 8px;
            padding: 12px 14px;
            cursor: pointer;
            transition: all 0.2s ease;
            position: relative;
        }

        .step-card:hover {
            border-color: #38bdf8;
            background: #f0f9ff;
            transform: translateY(-1px);
        }

        .step-card.active-step {
            background: #eff6ff;
            border-color: #0284c7;
            box-shadow: 0 0 0 1px #0284c7;
        }

        .step-card.done-step {
            background: #f0fdf4;
            border-color: #22c55e;
        }

        .step-badge {
            font-size: 10px;
            font-weight: 800;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: flex;
            align-items: center;
            gap: 6px;
            margin-bottom: 4px;
        }

        .step-card.active-step .step-badge { color: #0284c7; }
        .step-card.done-step .step-badge { color: #16a34a; }

        .step-heading {
            font-size: 13px;
            font-weight: 700;
            color: #0f172a;
        }

        .step-subtext {
            font-size: 11px;
            color: #64748b;
            margin-top: 3px;
            line-height: 1.35;
        }

        .step-arrow-divider {
            display: flex;
            align-items: center;
            justify-content: center;
            color: #94a3b8;
            font-size: 16px;
            padding: 0 4px;
            flex-shrink: 0;
        }

        /* Procedure flow pill steps */
        .procedure-pills {
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 8px;
            background: #ffffff;
            border: 1px dashed #cbd5e1;
            border-radius: 6px;
            padding: 8px 12px;
            margin-top: 8px;
        }

        .proc-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: #f1f5f9;
            color: #1e293b;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
        }

        .proc-arrow {
            color: #0284c7;
            font-weight: 900;
            font-size: 12px;
        }

        /* Non-technical user callout banner */
        .sales-tip-box {
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            border-left: 4px solid #0284c7;
            border-radius: 6px;
            padding: 12px 16px;
            margin-bottom: 20px;
            font-size: 12px;
            color: #334155;
            display: flex;
            align-items: flex-start;
            gap: 12px;
            line-height: 1.5;
        }

        /* Bottom Quick Action Navigation Bar */
        .step-nav-footer {
            margin-top: 24px;
            padding: 14px 18px;
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
"""

if '/* ================= SALES STEPPER & PROCEDURE UI ================= */' not in html:
    html = html.replace('@media print {', stepper_css + '\n        @media print {')
    print("Added Stepper CSS")

# 3. Update Left Navigation Rail
old_nav = """        <!-- Navigation Rail -->
        <nav class="nav-sidebar">
            <div class="nav-group-title">Operations</div>
            <div class="nav-item active" onclick="switchTab('tab-extract', this)">
                <span>1. Tender Requirements</span>
            </div>
            <div class="nav-item" onclick="switchTab('tab-bom', this)">
                <span>2. Compliant BOM & Pricing</span>
            </div>
            <div class="nav-item" onclick="switchTab('tab-gaps', this)">
                <span>3. Sourcing Gaps</span>
                <span id="gapNavBadge" class="nav-badge" style="display:none;">0</span>
            </div>

            <div class="nav-group-title" style="margin-top:16px;">Master Data</div>
            <div class="nav-item" onclick="switchTab('tab-catalog', this)">
                <span>4. Component Master</span>
            </div>
        </nav>"""

new_nav = """        <!-- Navigation Rail (Numbered Workflow for Sales Team) -->
        <nav class="nav-sidebar">
            <div class="nav-group-title">Tender Workflow</div>
            <div class="nav-item active" id="nav-step-1" onclick="switchTab('tab-extract', this)">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="display:inline-block; width:18px; height:18px; border-radius:50%; background:#e0f2fe; color:#0369a1; font-size:10px; font-weight:800; text-align:center; line-height:18px;">1</span>
                    <span>1. Upload & Scan</span>
                </div>
            </div>
            <div class="nav-item" id="nav-step-2" onclick="switchTab('tab-bom', this)">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="display:inline-block; width:18px; height:18px; border-radius:50%; background:#f1f5f9; color:#475569; font-size:10px; font-weight:800; text-align:center; line-height:18px;">2</span>
                    <span>2. BOM & Quote Price</span>
                </div>
            </div>
            <div class="nav-item" id="nav-step-3" onclick="switchTab('tab-gaps', this)">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="display:inline-block; width:18px; height:18px; border-radius:50%; background:#f1f5f9; color:#475569; font-size:10px; font-weight:800; text-align:center; line-height:18px;">3</span>
                    <span>3. Missing Items</span>
                </div>
                <span id="gapNavBadge" class="nav-badge" style="display:none;">0</span>
            </div>

            <div class="nav-group-title" style="margin-top:20px;">Master Reference</div>
            <div class="nav-item" id="nav-step-4" onclick="switchTab('tab-catalog', this)">
                <div style="display:flex; align-items:center; gap:8px;">
                    <i class="fas fa-database" style="font-size:12px; color:#64748b;"></i>
                    <span>Parts Catalog (140)</span>
                </div>
            </div>
        </nav>"""

if old_nav in html:
    html = html.replace(old_nav, new_nav)
    print("Updated Navigation Rail")
else:
    print("Warning: old_nav not found")

# 4. Insert Stepper + Procedure + Sales Guide into TAB 1
tab1_target = """            <!-- ================= TAB 1: TENDER REQUIREMENTS ================= -->
            <div id="tab-extract" class="tab-panel active">
                <div class="section-header">
                    <h2 class="section-title">Technical Specification & Tender Ingestion</h2>
                    <p class="section-desc">Parse unstructured GeM tenders, extract engineering constraints, identify non-compliance risks, and generate mandatory deliverable checklists.</p>
                </div>"""

tab1_replacement = """            <!-- ================= TAB 1: TENDER REQUIREMENTS ================= -->
            <div id="tab-extract" class="tab-panel active">

                <!-- 3-Step Interactive Visual Flow -->
                <div class="workflow-banner">
                    <div class="workflow-title-bar">
                        <span class="workflow-title">
                            <i class="fas fa-route" style="color:#0284c7;"></i> Simple 3-Step Bidding Procedure for Sales Team
                        </span>
                        <span style="font-size:11px; color:#64748b; font-weight:600;">Follow the arrows from Step 1 to Step 3</span>
                    </div>

                    <div class="workflow-stepper">
                        <!-- Step 1 (Active) -->
                        <div class="step-card active-step" onclick="switchTab('tab-extract', document.getElementById('nav-step-1'))">
                            <div class="step-badge">
                                <i class="fas fa-circle-dot" style="color:#0284c7;"></i> STEP 1 (Current)
                            </div>
                            <div class="step-heading">1. Upload & Scan</div>
                            <div class="step-subtext">Drop tender PDF or click sample to scan clauses, risks & deliverables.</div>
                        </div>

                        <div class="step-arrow-divider">
                            <i class="fas fa-arrow-right"></i>
                        </div>

                        <!-- Step 2 -->
                        <div class="step-card" onclick="switchTab('tab-bom', document.getElementById('nav-step-2'))">
                            <div class="step-badge">
                                <i class="fas fa-circle" style="font-size:8px;"></i> STEP 2
                            </div>
                            <div class="step-heading">2. Review Price & BOM</div>
                            <div class="step-subtext">Pick drone variant, set quantity, and see official GeM bid price.</div>
                        </div>

                        <div class="step-arrow-divider">
                            <i class="fas fa-arrow-right"></i>
                        </div>

                        <!-- Step 3 -->
                        <div class="step-card" onclick="switchTab('tab-gaps', document.getElementById('nav-step-3'))">
                            <div class="step-badge">
                                <i class="fas fa-circle" style="font-size:8px;"></i> STEP 3
                            </div>
                            <div class="step-heading">3. Handle Missing Parts</div>
                            <div class="step-subtext">Add provisional costs for custom items so quotation is never delayed.</div>
                        </div>
                    </div>

                    <!-- Step-by-Step Procedure with Arrows -->
                    <div class="procedure-pills">
                        <span style="font-size:11px; font-weight:700; color:#475569; margin-right:4px;">Quick Procedure:</span>
                        <span class="proc-pill"><i class="fas fa-file-pdf" style="color:#dc2626;"></i> 1. Select Tender PDF</span>
                        <span class="proc-arrow">&rarr;</span>
                        <span class="proc-pill"><i class="fas fa-bolt" style="color:#0284c7;"></i> 2. Click "Execute Scan"</span>
                        <span class="proc-arrow">&rarr;</span>
                        <span class="proc-pill"><i class="fas fa-shield-halved" style="color:#d97706;"></i> 3. Check Disqualification Risks</span>
                        <span class="proc-arrow">&rarr;</span>
                        <span class="proc-pill" style="background:#e0f2fe; color:#0369a1; font-weight:700;"><i class="fas fa-arrow-right"></i> 4. Proceed to Step 2 for Price</span>
                    </div>
                </div>

                <div class="sales-tip-box">
                    <i class="fas fa-lightbulb" style="color:#0284c7; font-size:18px; margin-top:2px; flex-shrink:0;"></i>
                    <div>
                        <strong style="color:#0f172a; font-size:13px;">How to use this screen (For Non-Technical Sales Users):</strong>
                        <div style="margin-top:4px; color:#475569;">
                            • <strong>Drop your tender PDF</strong> into Box 1 below, or click either blue <strong>Sample Tender</strong> button to load one instantly.<br>
                            • Click the black <strong>"Execute Extraction & Scan"</strong> button.<br>
                            • The engine automatically scans all statutory clauses, flags non-compliance risks (like China bans, 5-day flight samples, and penalties), and derives your deliverables checklist!
                        </div>
                    </div>
                </div>

                <div class="section-header">
                    <h2 class="section-title">Technical Specification & Tender Ingestion</h2>
                    <p class="section-desc">Parse unstructured GeM tenders, extract engineering constraints, identify non-compliance risks, and generate mandatory deliverable checklists.</p>
                </div>"""

if tab1_target in html:
    html = html.replace(tab1_target, tab1_replacement)
    print("Injected Stepper into TAB 1")
else:
    print("Warning: tab1_target not found")

# Add Bottom Action Button in Tab 1
tab1_bottom_target = """                    <!-- 4 Buckets Grid: Hardware, Commercial Obligations, Testing & SLAs, Mandatory Docs -->"""
tab1_bottom_replace = """                <!-- Quick Step Navigation for Sales -->
                <div class="step-nav-footer">
                    <div style="font-size:12px; color:#64748b;">
                        <i class="fas fa-info-circle" style="color:#0284c7;"></i> Completed scanning tender requirements? Move to Step 2 to calculate the bid price.
                    </div>
                    <button type="button" class="btn-primary" style="padding:8px 18px; font-weight:700;" onclick="switchTab('tab-bom', document.getElementById('nav-step-2'))">
                        Next: Step 2 — Review Price & BOM &rarr;
                    </button>
                </div>

                <!-- 4 Buckets Grid: Hardware, Commercial Obligations, Testing & SLAs, Mandatory Docs -->"""

if tab1_bottom_target in html:
    html = html.replace(tab1_bottom_target, tab1_bottom_replace)
    print("Injected Next Step button in TAB 1")

# 5. Insert Stepper + Procedure + Sales Guide into TAB 2
tab2_target = """            <!-- ================= TAB 2: BOM EXPLOSION & PRICING ================= -->
            <div id="tab-bom" class="tab-panel">
                <div class="section-header">
                    <h2 class="section-title">Compliant Bill of Materials & Cost Rollup</h2>
                    <p class="section-desc">Automated derivation of 100% Non-Chinese compliant components, statutory reserves, reverse auction buffers, and official GeM quotation figures.</p>
                </div>"""

tab2_replacement = """            <!-- ================= TAB 2: BOM EXPLOSION & PRICING ================= -->
            <div id="tab-bom" class="tab-panel">

                <!-- 3-Step Interactive Visual Flow -->
                <div class="workflow-banner">
                    <div class="workflow-title-bar">
                        <span class="workflow-title">
                            <i class="fas fa-route" style="color:#0284c7;"></i> Simple 3-Step Bidding Procedure for Sales Team
                        </span>
                        <span style="font-size:11px; color:#64748b; font-weight:600;">Step 2 of 3: Costing & Quotation</span>
                    </div>

                    <div class="workflow-stepper">
                        <!-- Step 1 (Done) -->
                        <div class="step-card done-step" onclick="switchTab('tab-extract', document.getElementById('nav-step-1'))">
                            <div class="step-badge">
                                <i class="fas fa-check-circle" style="color:#16a34a;"></i> STEP 1 (Done)
                            </div>
                            <div class="step-heading">1. Documents Scanned</div>
                            <div class="step-subtext">Clauses, risks and deliverables analyzed. Click to review.</div>
                        </div>

                        <div class="step-arrow-divider">
                            <i class="fas fa-arrow-right"></i>
                        </div>

                        <!-- Step 2 (Active) -->
                        <div class="step-card active-step" onclick="switchTab('tab-bom', document.getElementById('nav-step-2'))">
                            <div class="step-badge">
                                <i class="fas fa-circle-dot" style="color:#0284c7;"></i> STEP 2 (Current)
                            </div>
                            <div class="step-heading">2. Review Price & BOM</div>
                            <div class="step-subtext">Pick drone variant, set quantity, and see official GeM bid price.</div>
                        </div>

                        <div class="step-arrow-divider">
                            <i class="fas fa-arrow-right"></i>
                        </div>

                        <!-- Step 3 -->
                        <div class="step-card" onclick="switchTab('tab-gaps', document.getElementById('nav-step-3'))">
                            <div class="step-badge">
                                <i class="fas fa-circle" style="font-size:8px;"></i> STEP 3
                            </div>
                            <div class="step-heading">3. Handle Missing Parts</div>
                            <div class="step-subtext">Add provisional costs for custom items so quotation is never delayed.</div>
                        </div>
                    </div>

                    <!-- Step-by-Step Procedure with Arrows -->
                    <div class="procedure-pills">
                        <span style="font-size:11px; font-weight:700; color:#475569; margin-right:4px;">Sales Procedure:</span>
                        <span class="proc-pill"><i class="fas fa-crosshairs" style="color:#0284c7;"></i> 1. Choose Drone Model</span>
                        <span class="proc-arrow">&rarr;</span>
                        <span class="proc-pill"><i class="fas fa-cubes" style="color:#0284c7;"></i> 2. Enter Quantity & Margin %</span>
                        <span class="proc-arrow">&rarr;</span>
                        <span class="proc-pill" style="background:#dcfce7; color:#15803d; font-weight:700;"><i class="fas fa-tag"></i> 3. Quote Green Card Price on GeM</span>
                        <span class="proc-arrow">&rarr;</span>
                        <span class="proc-pill"><i class="fas fa-file-excel" style="color:#16a34a;"></i> 4. Download Excel / PDF</span>
                    </div>
                </div>

                <!-- Clear Sales Guide for Pricing Cards -->
                <div class="sales-tip-box" style="border-left-color:#16a34a; background:#f0fdf4;">
                    <i class="fas fa-money-bill-wave" style="color:#16a34a; font-size:18px; margin-top:2px; flex-shrink:0;"></i>
                    <div>
                        <strong style="color:#14532d; font-size:13px;">Which number should sales quote on the GeM portal?</strong>
                        <div style="margin-top:4px; color:#334155; line-height:1.5;">
                            • <strong>GREEN CARD (&quot;Official GeM Bid&quot;):</strong> <strong>THIS IS YOUR QUOTATION NUMBER!</strong> Enter this exact figure on the GeM portal. It includes all physical BOM items, 5% warranty reserve, 4% contingency buffer, sales margin, and 18% GST.<br>
                            • <strong>BLUE CARD (&quot;Recommended Bid Base&quot;):</strong> Company revenue before taxes.<br>
                            • <strong>GREY CARD (&quot;Total Project Cost&quot;):</strong> <strong>Reverse Auction (RA) Floor.</strong> Never drop below this price during live bidding, or the contract loses money.
                        </div>
                    </div>
                </div>

                <div class="section-header">
                    <h2 class="section-title">Compliant Bill of Materials & Cost Rollup</h2>
                    <p class="section-desc">Automated derivation of 100% Non-Chinese compliant components, statutory reserves, reverse auction buffers, and official GeM quotation figures.</p>
                </div>"""

if tab2_target in html:
    html = html.replace(tab2_target, tab2_replacement)
    print("Injected Stepper into TAB 2")
else:
    print("Warning: tab2_target not found")

# Add Bottom Action Buttons in Tab 2
tab2_bottom_target = """                    <div class="panel-body" style="padding:0; overflow-x:auto;">
                        <table class="enterprise-table">
                            <thead>
                                <tr>
                                    <th>Subsystem</th>
                                    <th>Selected Component Specification</th>
                                    <th style="text-align:center;">Origin</th>
                                    <th style="text-align:center;">Qty/U</th>
                                    <th style="text-align:right;">Unit Rate (INR)</th>
                                    <th style="text-align:right;">Line Total (INR)</th>
                                </tr>
                            </thead>
                            <tbody id="bomTableBody"></tbody>
                        </table>
                    </div>
                </div>
            </div>"""

tab2_bottom_replace = """                    <div class="panel-body" style="padding:0; overflow-x:auto;">
                        <table class="enterprise-table">
                            <thead>
                                <tr>
                                    <th>Subsystem</th>
                                    <th>Selected Component Specification</th>
                                    <th style="text-align:center;">Origin</th>
                                    <th style="text-align:center;">Qty/U</th>
                                    <th style="text-align:right;">Unit Rate (INR)</th>
                                    <th style="text-align:right;">Line Total (INR)</th>
                                </tr>
                            </thead>
                            <tbody id="bomTableBody"></tbody>
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

if tab2_bottom_target in html:
    html = html.replace(tab2_bottom_target, tab2_bottom_replace)
    print("Injected Next/Back Step buttons in TAB 2")

# 6. Insert Stepper + Procedure + Sales Guide into TAB 3
tab3_target = """            <!-- ================= TAB 3: SOURCING GAPS ================= -->
            <div id="tab-gaps" class="tab-panel">
                <div class="section-header" style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <h2 class="section-title">Technical Sourcing & Procurement Gaps</h2>
                        <p class="section-desc">Manage unmapped items identified in tenders that require provisional costing, vendor quotes, or in-house engineering.</p>
                    </div>
                    <button type="button" class="btn-primary" onclick="openCustomPartModal()">+ Add Custom Component / Provisional Cost</button>
                </div>"""

tab3_replacement = """            <!-- ================= TAB 3: SOURCING GAPS ================= -->
            <div id="tab-gaps" class="tab-panel">

                <!-- 3-Step Interactive Visual Flow -->
                <div class="workflow-banner">
                    <div class="workflow-title-bar">
                        <span class="workflow-title">
                            <i class="fas fa-route" style="color:#0284c7;"></i> Simple 3-Step Bidding Procedure for Sales Team
                        </span>
                        <span style="font-size:11px; color:#64748b; font-weight:600;">Step 3 of 3: Sourcing & Custom Requirements</span>
                    </div>

                    <div class="workflow-stepper">
                        <!-- Step 1 (Done) -->
                        <div class="step-card done-step" onclick="switchTab('tab-extract', document.getElementById('nav-step-1'))">
                            <div class="step-badge">
                                <i class="fas fa-check-circle" style="color:#16a34a;"></i> STEP 1 (Done)
                            </div>
                            <div class="step-heading">1. Documents Scanned</div>
                            <div class="step-subtext">Clauses, risks and deliverables analyzed.</div>
                        </div>

                        <div class="step-arrow-divider">
                            <i class="fas fa-arrow-right"></i>
                        </div>

                        <!-- Step 2 (Done) -->
                        <div class="step-card done-step" onclick="switchTab('tab-bom', document.getElementById('nav-step-2'))">
                            <div class="step-badge">
                                <i class="fas fa-check-circle" style="color:#16a34a;"></i> STEP 2 (Done)
                            </div>
                            <div class="step-heading">2. Price & BOM Ready</div>
                            <div class="step-subtext">BOM calculated and quotation ready.</div>
                        </div>

                        <div class="step-arrow-divider">
                            <i class="fas fa-arrow-right"></i>
                        </div>

                        <!-- Step 3 (Active) -->
                        <div class="step-card active-step" onclick="switchTab('tab-gaps', document.getElementById('nav-step-3'))">
                            <div class="step-badge">
                                <i class="fas fa-circle-dot" style="color:#0284c7;"></i> STEP 3 (Current)
                            </div>
                            <div class="step-heading">3. Handle Missing Parts</div>
                            <div class="step-subtext">Add provisional costs for custom items so quotation is never delayed.</div>
                        </div>
                    </div>

                    <!-- Step-by-Step Procedure with Arrows -->
                    <div class="procedure-pills">
                        <span style="font-size:11px; font-weight:700; color:#475569; margin-right:4px;">Sales Procedure:</span>
                        <span class="proc-pill"><i class="fas fa-magnifying-glass" style="color:#0284c7;"></i> 1. Check Unmapped Items</span>
                        <span class="proc-arrow">&rarr;</span>
                        <span class="proc-pill"><i class="fas fa-plus" style="color:#0284c7;"></i> 2. Click "+ Add Custom Component"</span>
                        <span class="proc-arrow">&rarr;</span>
                        <span class="proc-pill"><i class="fas fa-calculator" style="color:#16a34a;"></i> 3. Put Provisional Cost</span>
                        <span class="proc-arrow">&rarr;</span>
                        <span class="proc-pill" style="background:#dcfce7; color:#15803d; font-weight:700;"><i class="fas fa-check"></i> 4. BOM Auto-Recalculates!</span>
                    </div>
                </div>

                <!-- Clear Sales Guide for Missing Items -->
                <div class="sales-tip-box" style="border-left-color:#eab308; background:#fefce8;">
                    <i class="fas fa-lightbulb" style="color:#ca8a04; font-size:18px; margin-top:2px; flex-shrink:0;"></i>
                    <div>
                        <strong style="color:#713f12; font-size:13px;">What should sales do if a customer asks for a non-standard item?</strong>
                        <div style="margin-top:4px; color:#475569; line-height:1.5;">
                            • Click the <strong>&quot;+ Add Custom Component / Provisional Cost&quot;</strong> button below.<br>
                            • Type the item name and an estimated budget cost (e.g. &#8377;45,000 for a custom thermal mount).<br>
                            • <strong>The total tender quote in Step 2 updates immediately!</strong> Your tender submission is never held up waiting for engineering vendor quotes.
                        </div>
                    </div>
                </div>

                <div class="section-header" style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <h2 class="section-title">Technical Sourcing & Procurement Gaps</h2>
                        <p class="section-desc">Manage unmapped items identified in tenders that require provisional costing, vendor quotes, or in-house engineering.</p>
                    </div>
                    <button type="button" class="btn-primary" onclick="openCustomPartModal()">+ Add Custom Component / Provisional Cost</button>
                </div>"""

if tab3_target in html:
    html = html.replace(tab3_target, tab3_replacement)
    print("Injected Stepper into TAB 3")
else:
    print("Warning: tab3_target not found")

# Add Bottom Action Buttons in Tab 3
tab3_bottom_target = """                    <tbody id="gapsTableBody"></tbody>
                </table>
            </div>"""

tab3_bottom_replace = """                    <tbody id="gapsTableBody"></tbody>
                </table>

                <!-- Quick Step Navigation for Sales -->
                <div class="step-nav-footer">
                    <button type="button" class="btn-secondary" onclick="switchTab('tab-bom', document.getElementById('nav-step-2'))">
                        &larr; Back to Step 2: Price & BOM
                    </button>
                    <div style="display:flex; gap:10px;">
                        <button type="button" class="btn-secondary" onclick="exportBOMCSV()">
                            <i class="fas fa-download"></i> Download BOM (Excel CSV)
                        </button>
                        <button type="button" class="btn-primary" onclick="printOrSavePDF()">
                            <i class="fas fa-file-pdf"></i> Export Executive PDF
                        </button>
                    </div>
                </div>
            </div>"""

if tab3_bottom_target in html:
    html = html.replace(tab3_bottom_target, tab3_bottom_replace)
    print("Injected Action buttons in TAB 3")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Finished applying sales UI to index.html!")
