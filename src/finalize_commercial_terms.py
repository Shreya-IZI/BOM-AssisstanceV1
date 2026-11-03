with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update executeAnalysis to detect Warranty, AMC, Training
old_analysis_anchor = """            const qtyMatch = text.match(/(?:total\\s+quantity|कुल\\s+मात्रा)[\\s:/\\-]+(\\d+)/i) || text.match(/quantity[\\s:/\\-]+(\\d+)/i);
            if (qtyMatch && qtyMatch[1]) document.getElementById('bomQty').value = parseInt(qtyMatch[1]);
            tenderHasBeenAnalyzed = true;
            recalculateBOM();
            setStep(5, 'done');"""

new_analysis_anchor = """            const qtyMatch = text.match(/(?:total\\s+quantity|कुल\\s+मात्रा)[\\s:/\\-]+(\\d+)/i) || text.match(/quantity[\\s:/\\-]+(\\d+)/i);
            if (qtyMatch && qtyMatch[1]) document.getElementById('bomQty').value = parseInt(qtyMatch[1]);

            // Auto-detect Warranty Period
            const wMatch = text.match(/(\\d+)\\s*(?:year|yr)s?\\s*(?:comprehensive\\s*)?(?:warranty|guarantee)/i);
            if (wMatch && wMatch[1]) {
                const wInput = document.getElementById('cfgWarranty');
                if (wInput) wInput.value = `${wMatch[1]} Years Comprehensive On-Site`;
            }

            // Auto-detect AMC Terms
            const amcMatch = text.match(/(\\d+)\\s*(?:year|yr)s?\\s*(?:amc|camc|annual\\s*maintenance)/i);
            if (amcMatch && amcMatch[1]) {
                const aInput = document.getElementById('cfgAMC');
                if (aInput) aInput.value = `${amcMatch[1]} Years Post-Warranty (48h Turnaround SLA)`;
            }

            // Auto-detect Training Location & Days
            const trDaysMatch = text.match(/(\\d+)\\s*(?:working\\s*)?days?\\s*(?:training|instruction)/i) || text.match(/training[\\s\\S]{0,40}?(\\d+)\\s*days?/i);
            const trLocMatch = text.match(/(leh|ladakh|high[-\\s]altitude|buyer\\s*location|consignee\\s*base|field\\s*site)/i);
            const trDays = trDaysMatch ? `${trDaysMatch[1]} Working Days` : "10 Working Days";
            const trLoc = trLocMatch ? trLocMatch[1].toUpperCase() : "Buyer Base / Leh Field";
            const tInput = document.getElementById('cfgTraining');
            if (tInput) tInput.value = `${trLoc} — ${trDays}`;

            tenderHasBeenAnalyzed = true;
            recalculateBOM();
            updateCommercialTermsTable();
            setStep(5, 'done');"""

if old_analysis_anchor in html:
    html = html.replace(old_analysis_anchor, new_analysis_anchor)
    print("[1/3] executeAnalysis updated with Warranty, AMC, Training extraction")
else:
    print("Warning: old_analysis_anchor not found")

# 2. Update Draft saving and loading for the 3 fields
old_draft_save = """            const draft = {
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
            };"""

new_draft_save = """            const draft = {
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
                warrantyCfg: document.getElementById('cfgWarranty')?.value || "3 Years Comprehensive On-Site",
                amcCfg: document.getElementById('cfgAMC')?.value || "2 Years Post-Warranty (48h Turnaround SLA)",
                trainingCfg: document.getElementById('cfgTraining')?.value || "Buyer Base / High-Altitude (Leh) — 10 Working Days",
                sourcingGaps: sourcingGaps,
                officialBid: window.currentOfficialBid || 0
            };"""

if old_draft_save in html:
    html = html.replace(old_draft_save, new_draft_save)
    print("[2/3] saveTenderDraft updated")
else:
    print("Warning: old_draft_save not found")

old_draft_load = """            tenderHasBeenAnalyzed = true;
            recalculateBOM();
            closeDraftsModal();
            switchTab('tab-bom', document.getElementById('nav-step-2'));
            alert(`Tender Draft "${draft.title}" loaded successfully!`);"""

new_draft_load = """            if (draft.warrantyCfg && document.getElementById('cfgWarranty')) document.getElementById('cfgWarranty').value = draft.warrantyCfg;
            if (draft.amcCfg && document.getElementById('cfgAMC')) document.getElementById('cfgAMC').value = draft.amcCfg;
            if (draft.trainingCfg && document.getElementById('cfgTraining')) document.getElementById('cfgTraining').value = draft.trainingCfg;

            tenderHasBeenAnalyzed = true;
            recalculateBOM();
            updateCommercialTermsTable();
            closeDraftsModal();
            switchTab('tab-bom', document.getElementById('nav-step-2'));
            alert(`Tender Draft "${draft.title}" loaded successfully!`);"""

if old_draft_load in html:
    html = html.replace(old_draft_load, new_draft_load)
    print("[3/3] loadDraftById updated")
else:
    print("Warning: old_draft_load not found")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Finalize script executed successfully!")
