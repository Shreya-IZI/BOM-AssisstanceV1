import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add CSS for Workflow Stepper, Simplified cards, and Tooltips
stepper_css = """
        /* Interactive Workflow Stepper */
        .workflow-banner {
            background: #ffffff;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 16px 20px;
            margin-bottom: 24px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.03);
        }

        .workflow-title-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 14px;
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
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .workflow-stepper {
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: relative;
        }

        .step-card {
            flex: 1;
            background: #f8fafc;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 10px 14px;
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
            border-color: #3b82f6;
            box-shadow: 0 0 0 1px #3b82f6;
        }

        .step-card.done-step {
            background: #f0fdf4;
            border-color: #86efac;
        }

        .step-number {
            font-size: 10px;
            font-weight: 800;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .step-card.active-step .step-number { color: #2563eb; }
        .step-card.done-step .step-number { color: #16a34a; }

        .step-heading {
            font-size: 12px;
            font-weight: 700;
            color: #0f172a;
            margin-top: 2px;
        }

        .step-subtext {
            font-size: 11px;
            color: #64748b;
            margin-top: 2px;
            line-height: 1.3;
        }

        .step-arrow {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 0 10px;
            color: #94a3b8;
            font-size: 14px;
            flex-shrink: 0;
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

        /* Quick Action Next Step Footer Bar */
        .quick-nav-bar {
            margin-top: 24px;
            padding: 14px 18px;
            background: #ffffff;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
"""

if '/* Interactive Workflow Stepper */' not in content:
    content = content.replace('@media print {', stepper_css + '\n        @media print {')

# 2. Add visual step badges to left navigation
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

new_nav = """        <!-- Navigation Rail (With clear Sales Step numbering) -->
        <nav class="nav-sidebar">
            <div class="nav-group-title">Tender Workflow</div>
            <div class="nav-item active" id="nav-item-extract" onclick="switchTab('tab-extract', this)">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="display:inline-block; width:18px; height:18px; border-radius:50%; background:#e0f2fe; color:#0369a1; font-size:10px; font-weight:800; text-align:center; line-height:18px;">1</span>
                    <span>Upload & Check</span>
                </div>
            </div>
            <div class="nav-item" id="nav-item-bom" onclick="switchTab('tab-bom', this)">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="display:inline-block; width:18px; height:18px; border-radius:50%; background:#f1f5f9; color:#475569; font-size:10px; font-weight:800; text-align:center; line-height:18px;" id="nav-badge-2">2</span>
                    <span>BOM & Quote Price</span>
                </div>
            </div>
            <div class="nav-item" id="nav-item-gaps" onclick="switchTab('tab-gaps', this)">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="display:inline-block; width:18px; height:18px; border-radius:50%; background:#f1f5f9; color:#475569; font-size:10px; font-weight:800; text-align:center; line-height:18px;" id="nav-badge-3">3</span>
                    <span>Missing Items</span>
                </div>
                <span id="gapNavBadge" class="nav-badge" style="display:none;">0</span>
            </div>

            <div class="nav-group-title" style="margin-top:20px;">Reference Data</div>
            <div class="nav-item" id="nav-item-catalog" onclick="switchTab('tab-catalog', this)">
                <div style="display:flex; align-items:center; gap:8px;">
                    <i class="fas fa-boxes-stacked" style="font-size:12px; color:#64748b;"></i>
                    <span>Parts Catalog (140)</span>
                </div>
            </div>
        </nav>"""

content = content.replace(old_nav, new_nav)

# 3. Add Workflow Banner with Arrows to Tab 1
tab1_start = """            <!-- ================= TAB 1: TENDER REQUIREMENTS ================= -->
            <div id="tab-extract" class="tab-panel active">
                <div class="section-header">
                    <h2 class="section-title">Technical Specification & Tender Ingestion</h2>
                    <p class="section-desc">Parse unstructured GeM tenders, extract engineering constraints, identify non-compliance risks, and generate mandatory deliverable checklists.</p>
                </div>"""

tab1_with_stepper = """            <!-- ================= TAB 1: TENDER REQUIREMENTS ================= -->
            <div id="tab-extract" class="tab-panel active">
                
                <!-- 3-Step Interactive Visual Flow for Non-Technical Sales Users -->
                <div class="workflow-banner">
                    <div class="workflow-title-bar">
                        <span class="workflow-title">
                            <i class="fas fa-route" style="color:#0284c7;"></i> Simple 3-Step Tender Procedure for Sales Team
                        </span>
                        <span style="font-size:11px; color:#64748b; font-weight:600;">Follow the arrows from Step 1 to Step 3</span>
                    </div>

                    <div class="workflow-stepper">
                        <!-- Step 1 (Current) -->
                        <div class="step-card active-step" onclick="switchTab('tab-extract', document.getElementById('nav-item-extract'))">
                            <div class="step-number">
                                <i class="fas fa-circle-dot" style="color:#2563eb;"></i> STEP 1 (Current)
                            </div>
                            <div class="step-heading">1. Upload Documents</div>
                            <div class="step-subtext">Drop tender PDF or click demo button to scan clauses & penalties.</div>
                        </div>

                        <div class="step-arrow">
                            <i class="fas fa-arrow-right"></i>
                        </div>

                        <!-- Step 2 -->
                        <div class="step-card" onclick="switchTab('tab-bom', document.getElementById('nav-item-bom'))">
                            <div class="step-number">
                                <i class="fas fa-circle" style="font-size:8px;"></i> STEP 2
                            </div>
                            <div class="step-heading">2. Review Price & BOM</div>
                            <div class="step-subtext">See exact quote to submit on GeM and download Excel sheet.</div>
                        </div>

                        <div class="step-arrow">
                            <i class="fas fa-arrow-right"></i>
                        </div>

                        <!-- Step 3 -->
                        <div class="step-card" onclick="switchTab('tab-gaps', document.getElementById('nav-item-gaps'))">
                            <div class="step-number">
                                <i class="fas fa-circle" style="font-size:8px;"></i> STEP 3
                            </div>
                            <div class="step-heading">3. Handle Missing Parts</div>
                            <div class="step-subtext">Put provisional costs for custom items so tender is never delayed.</div>
                        </div>
                    </div>
                </div>

                <div class="sales-tip-box">
                    <i class="fas fa-lightbulb" style="color:#0284c7; font-size:16px; margin-top:2px;"></i>
                    <div>
                        <strong style="color:#0f172a;">How to use this screen (For Sales & Bidding):</strong>
                        <div style="margin-top:2px; color:#475569;">
                            1. Drop your tender file into Box 1 (and optional technical spec into Box 2), or click either blue sample button below.<br>
                            2. Click the black <strong>"Execute Extraction & Scan"</strong> button.<br>
                            3. The system scans all 19 GeM clauses, warns you of disqualification traps (like China bans and 5-day samples), and automatically builds your tender proposal.
                        </div>
                    </div>
                </div>"""

content = content.replace(tab1_start, tab1_with_stepper)

# 4. Add Tab 2 Workflow Banner & Explanations
tab2_start = """            <!-- ================= TAB 2: BOM EXPLOSION & PRICING ================= -->
            <div id="tab-bom" class="tab-panel">
                <div class="section-header">
                    <h2 class="section-title">Compliant Bill of Materials & Cost Rollup</h2>
                    <p class="section-desc">Automated derivation of 100% Non-Chinese compliant components, statutory reserves, reverse auction buffers, and official GeM quotation figures.</p>
                </div>"""

tab2_with_stepper = """            <!-- ================= TAB 2: BOM EXPLOSION & PRICING ================= -->
            <div id="tab-bom" class="tab-panel">
                
                <!-- 3-Step Interactive Visual Flow -->
                <div class="workflow-banner">
                    <div class="workflow-title-bar">
                        <span class="workflow-title">
                            <i class="fas fa-route" style="color:#0284c7;"></i> Simple 3-Step Tender Procedure for Sales Team
                        </span>
                        <span style="font-size:11px; color:#64748b; font-weight:600;">Step 2 of 3: Pricing & Quotation</span>
                    </div>

                    <div class="workflow-stepper">
                        <!-- Step 1 -->
                        <div class="step-card done-step" onclick="switchTab('tab-extract', document.getElementById('nav-item-extract'))">
                            <div class="step-number">
                                <i class="fas fa-check-circle" style="color:#16a34a;"></i> STEP 1
                            </div>
                            <div class="step-heading">1. Documents Uploaded</div>
                            <div class="step-subtext">Clauses, risks and deliverables analyzed. Click to view.</div>
                        </div>

                        <div class="step-arrow">
                            <i class="fas fa-arrow-right"></i>
                        </div>

                        <!-- Step 2 (Current) -->
                        <div class="step-card active-step" onclick="switchTab('tab-bom', document.getElementById('nav-item-bom'))">
                            <div class="step-number">
                                <i class="fas fa-circle-dot" style="color:#2563eb;"></i> STEP 2 (Current)
                            </div>
                            <div class="step-heading">2. Review Price & BOM</div>
                            <div class="step-subtext">Pick drone variant, set quantity, and see official GeM quote price.</div>
                        </div>

                        <div class="step-arrow">
                            <i class="fas fa-arrow-right"></i>
                        </div>

                        <!-- Step 3 -->
                        <div class="step-card" onclick="switchTab('tab-gaps', document.getElementById('nav-item-gaps'))">
                            <div class="step-number">
                                <i class="fas fa-circle" style="font-size:8px;"></i> STEP 3
                            </div>
                            <div class="step-heading">3. Handle Missing Parts</div>
                            <div class="step-subtext">Add custom items or check sourcing status.</div>
                        </div>
                    </div>
                </div>

                <div class="sales-tip-box" style="border-left-color:#16a34a; background:#f0fdf4;">
                    <i class="fas fa-money-bill-wave" style="color:#16a34a; font-size:16px; margin-top:2px;"></i>
                    <div>
                        <strong style="color:#14532d;">Which number should the sales team quote on GeM?</strong>
                        <div style="margin-top:2px; color:#334155;">
                            • Quote the <strong>GREEN CARD ("Official GeM Bid")</strong> on the GeM portal — it includes all statutory reserves and 18% GST.<br>
                            • The <strong>BLUE CARD ("Recommended Bid Base")</strong> is your company's net revenue before tax.<br>
                            • If there is a <strong>Live Reverse Auction (RA)</strong>, your lowest walk-away price floor is the <strong>GREY CARD ("Total Project Cost")</strong>. Never bid below that grey card!
                        </div>
                    </div>
                </div>"""

content = content.replace(tab2_start, tab2_with_stepper)

# 5. Add Tab 3 Workflow Banner & Explanations
tab3_start = """            <!-- ================= TAB 3: SOURCING GAPS ================= -->
            <div id="tab-gaps" class="tab-panel">
                <div class="section-header" style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <h2 class="section-title">Technical Sourcing & Procurement Gaps</h2>
                        <p class="section-desc">Manage unmapped items identified in tenders that require provisional costing, vendor quotes, or in-house engineering.</p>
                    </div>
                    <button type="button" class="btn-primary" onclick="openCustomPartModal()">+ Add Custom Component / Provisional Cost</button>
                </div>"""

tab3_with_stepper = """            <!-- ================= TAB 3: SOURCING GAPS ================= -->
            <div id="tab-gaps" class="tab-panel">
                
                <!-- 3-Step Interactive Visual Flow -->
                <div class="workflow-banner">
                    <div class="workflow-title-bar">
                        <span class="workflow-title">
                            <i class="fas fa-route" style="color:#0284c7;"></i> Simple 3-Step Tender Procedure for Sales Team
                        </span>
                        <span style="font-size:11px; color:#64748b; font-weight:600;">Step 3 of 3: Sourcing & Custom Specs</span>
                    </div>

                    <div class="workflow-stepper">
                        <!-- Step 1 -->
                        <div class="step-card done-step" onclick="switchTab('tab-extract', document.getElementById('nav-item-extract'))">
                            <div class="step-number">
                                <i class="fas fa-check-circle" style="color:#16a34a;"></i> STEP 1
                            </div>
                            <div class="step-heading">1. Documents Uploaded</div>
                            <div class="step-subtext">Clauses, risks and deliverables analyzed.</div>
                        </div>

                        <div class="step-arrow">
                            <i class="fas fa-arrow-right"></i>
                        </div>

                        <!-- Step 2 -->
                        <div class="step-card done-step" onclick="switchTab('tab-bom', document.getElementById('nav-item-bom'))">
                            <div class="step-number">
                                <i class="fas fa-check-circle" style="color:#16a34a;"></i> STEP 2
                            </div>
                            <div class="step-heading">2. BOM & Pricing</div>
                            <div class="step-subtext">Prices calculated and ready to download.</div>
                        </div>

                        <div class="step-arrow">
                            <i class="fas fa-arrow-right"></i>
                        </div>

                        <!-- Step 3 (Current) -->
                        <div class="step-card active-step" onclick="switchTab('tab-gaps', document.getElementById('nav-item-gaps'))">
                            <div class="step-number">
                                <i class="fas fa-circle-dot" style="color:#2563eb;"></i> STEP 3 (Current)
                            </div>
                            <div class="step-heading">3. Handle Missing Parts</div>
                            <div class="step-subtext">Put provisional costs for custom items so tender is never delayed.</div>
                        </div>
                    </div>
                </div>

                <div class="sales-tip-box" style="border-left-color:#eab308; background:#fefce8;">
                    <i class="fas fa-info-circle" style="color:#ca8a04; font-size:16px; margin-top:2px;"></i>
                    <div>
                        <strong style="color:#713f12;">What should sales do if a customer asks for a non-standard item?</strong>
                        <div style="margin-top:2px; color:#475569;">
                            • Click <strong>"+ Add Custom Component / Provisional Cost"</strong> button on the right.<br>
                            • Type in the item name and an estimated budget price. It will automatically update the total price in Step 2 so your bid is ready on time!<br>
                            • Engineering/Procurement will then finalize the vendor quote in parallel.
                        </div>
                    </div>
                </div>

                <div class="section-header" style="display:flex; justify-content:space-between; align-items:center; margin-top:16px;">
                    <div>
                        <h2 class="section-title">Technical Sourcing & Procurement Gaps</h2>
                        <p class="section-desc">Manage unmapped items identified in tenders that require provisional costing, vendor quotes, or in-house engineering.</p>
                    </div>
                    <button type="button" class="btn-primary" onclick="openCustomPartModal()">+ Add Custom Component / Provisional Cost</button>
                </div>"""

content = content.replace(tab3_start, tab3_with_stepper)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated index.html with interactive step flow and sales guidance!")
