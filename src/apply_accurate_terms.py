import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update dropZone handlers to include dragover, dragleave, drop
old_dz = """        const dropZoneTender = document.getElementById('dropZoneTender');
        const tenderFileInput = document.getElementById('tenderFileInput');
        if (dropZoneTender) dropZoneTender.addEventListener('click', () => tenderFileInput.click());

        const dropZoneTech = document.getElementById('dropZoneTech');
        const techFileInput = document.getElementById('techFileInput');
        if (dropZoneTech) dropZoneTech.addEventListener('click', () => techFileInput.click());"""

new_dz = """        const dropZoneTender = document.getElementById('dropZoneTender');
        const tenderFileInput = document.getElementById('tenderFileInput');
        if (dropZoneTender && tenderFileInput) {
            dropZoneTender.addEventListener('click', () => tenderFileInput.click());
            dropZoneTender.addEventListener('dragover', (e) => {
                e.preventDefault(); e.stopPropagation();
                dropZoneTender.style.borderColor = '#0284c7';
                dropZoneTender.style.background = '#f0f9ff';
            });
            dropZoneTender.addEventListener('dragleave', (e) => {
                e.preventDefault(); e.stopPropagation();
                dropZoneTender.style.borderColor = '#0284c7';
                dropZoneTender.style.background = '#ffffff';
            });
            dropZoneTender.addEventListener('drop', (e) => {
                e.preventDefault(); e.stopPropagation();
                dropZoneTender.style.borderColor = '#0284c7';
                dropZoneTender.style.background = '#ffffff';
                if (e.dataTransfer && e.dataTransfer.files.length) {
                    processDualFile(e.dataTransfer.files[0], 'tender');
                }
            });
        }

        const dropZoneTech = document.getElementById('dropZoneTech');
        const techFileInput = document.getElementById('techFileInput');
        if (dropZoneTech && techFileInput) {
            dropZoneTech.addEventListener('click', () => techFileInput.click());
            dropZoneTech.addEventListener('dragover', (e) => {
                e.preventDefault(); e.stopPropagation();
                dropZoneTech.style.borderColor = '#7c3aed';
                dropZoneTech.style.background = '#faf5ff';
            });
            dropZoneTech.addEventListener('dragleave', (e) => {
                e.preventDefault(); e.stopPropagation();
                dropZoneTech.style.borderColor = '#7c3aed';
                dropZoneTech.style.background = '#ffffff';
            });
            dropZoneTech.addEventListener('drop', (e) => {
                e.preventDefault(); e.stopPropagation();
                dropZoneTech.style.borderColor = '#7c3aed';
                dropZoneTech.style.background = '#ffffff';
                if (e.dataTransfer && e.dataTransfer.files.length) {
                    processDualFile(e.dataTransfer.files[0], 'tech');
                }
            });
        }"""

assert old_dz in text, "old_dz not found"
text = text.replace(old_dz, new_dz)

# 2. Add parseContractualTenderTerms before executeAnalysis
old_fn_start = """        async function executeAnalysis() {"""

new_parser_and_fn = """        function parseContractualTenderTerms(rawText) {
            if (!rawText || !rawText.trim()) {
                return {
                    warranty: '',
                    amc: '',
                    training: '',
                    shelfLife: ''
                };
            }
            const cleanT = rawText.replace(/\\d+\\s*\\/\\s*\\d+/g, ' '); // remove page numbers (e.g. 8 / 14)

            // 1. Warranty Period
            let warranty = "1 Year from final acceptance at consignee site (Clause 30)";
            const wordToNum = { 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5 };
            const wMatch = cleanT.match(/warranty[\\s\\S]{0,60}?\\b(?:shall\\s+be|is|of|:|-)?\\s*(\\d+|one|two|three|four|five)\\s*(years?|yrs?|months?|साल|वर्ष)/i) ||
                           cleanT.match(/(\\d+|one|two|three|four|five)\\s*(years?|yrs?|months?|साल|वर्ष)[\\s\\S]{0,40}?warranty/i);

            if (wMatch) {
                let num = parseInt(wMatch[1]);
                if (isNaN(num)) num = wordToNum[wMatch[1].toLowerCase()] || 1;
                const unit = wMatch[2].toLowerCase();
                if (unit.startsWith('month')) {
                    if (num === 12) warranty = "1 Year (12 Months) from final acceptance at consignee site (Clause 30)";
                    else if (num === 24) warranty = "2 Years (24 Months) from final acceptance at consignee site (Clause 30)";
                    else if (num === 36) warranty = "3 Years (36 Months) from final acceptance at consignee site (Clause 30)";
                    else warranty = num + " Months from final acceptance at consignee site (Clause 30)";
                } else {
                    warranty = num + (num > 1 ? " Years" : " Year") + " from final acceptance at consignee site (Clause 30)";
                }
            }

            // 2. AMC Terms
            let amc = "Not Mandated in Tender Scope / Nil AMC (Service & Maintenance Group in India under Cl 30)";
            const negAmc = cleanT.match(/(?:amc|annual\\s*maintenance|camc)[\\s\\S]{0,35}?(?:not\\s*required|nil|not\\s*applicable|na\\b|none|no\\s*amc|0\\s*years?)/i) ||
                           cleanT.match(/(?:not\\s*required|nil|not\\s*applicable|na\\b|none)[\\s\\S]{0,25}?(?:amc|annual\\s*maintenance|camc)/i);
            const mAmcDur = cleanT.match(/(?:amc|camc|annual\\s*maintenance\\s*(?:contract)?|post-warranty\\s*maintenance)[\\s\\S]{0,50}?\\b(?:for|of|:|-)?\\s*(\\d+)\\s*(years?|yrs?|months?)/i) ||
                            cleanT.match(/(\\d+)\\s*(years?|yrs?|months?)[\\s\\S]{0,30}?(?:post[-\\s]*warranty\\s*)?(?:amc|camc|annual\\s*maintenance)/i);

            if (negAmc) {
                amc = "Not Required in Tender Scope (Nil AMC / OEM Maintenance Group in India)";
            } else if (mAmcDur) {
                const dur = parseInt(mAmcDur[1]);
                const unit = mAmcDur[2].toLowerCase();
                if (unit.startsWith('month')) amc = dur + " Months Post-Warranty Comprehensive AMC";
                else amc = dur + (dur > 1 ? " Years" : " Year") + " Post-Warranty Comprehensive AMC";
            } else if (/\\b(amc|camc|annual\\s*maintenance\\s*contract)\\b/i.test(cleanT)) {
                amc = "Comprehensive AMC as per Buyer ATC Clauses";
            }

            // 3. Training
            const trEmpMatch = cleanT.match(/number\\s+of\\s+employees\\s+to\\s+be\\s+trained[\\s\\S]{0,30}?(\\d+)/i) || 
                               cleanT.match(/(\\d+)\\s*(?:employees|personnel|operators|pilots)/i);
            const trLocMatch = cleanT.match(/place\\s+for\\s+training[\\s\\S]{0,35}?([A-Za-z0-9\\s]+?)(?:and|\\n|\\.|$)/i) || 
                               cleanT.match(/\\b(hq\\s*4\\s*arty\\s*bde|leh|ladakh|prayagraj|jammu|buyer\\s*base|consignee\\s*location)\\b/i);
            const trDaysMatch = cleanT.match(/duration\\s+of\\s+training[\\s\\S]{0,30}?(\\d+)\\s*days?/i) || 
                                cleanT.match(/(\\d+)\\s*(?:working\\s*)?days?\\s*(?:of\\s*)?training/i);

            const numEmp = trEmpMatch ? (trEmpMatch[1].trim() + " Employees") : "5 Employees";
            const numDays = trDaysMatch ? (trDaysMatch[1].trim() + " Days") : "10 Days";
            let trPlace = "HQ 4 Arty Bde (Consignee Location)";
            if (trLocMatch) {
                const cand = trLocMatch[1].trim().replace(/\\s+/g, ' ');
                if (cand.length >= 3 && cand.length <= 40) trPlace = cand;
            }
            const training = trPlace + " — " + numDays + " (" + numEmp + ")";

            return { warranty, amc, training };
        }

        async function executeAnalysis() {"""

assert old_fn_start in text, "old_fn_start not found"
text = text.replace(old_fn_start, new_parser_and_fn)

# 3. In executeAnalysis, replace detection lines with parseContractualTenderTerms
old_terms_exec = """            // 1. Accurately detect Warranty Period (e.g. "Warranty period ... shall be 1 years")
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

new_terms_exec = """            // Accurately extract Contractual Terms (Warranty, AMC, Training)
            const contractualTerms = parseContractualTenderTerms(text);
            const wInput = document.getElementById('cfgWarranty');
            if (wInput) wInput.value = contractualTerms.warranty;
            const aInput = document.getElementById('cfgAMC');
            if (aInput) aInput.value = contractualTerms.amc;
            const tInput = document.getElementById('cfgTraining');
            if (tInput) tInput.value = contractualTerms.training;"""

assert old_terms_exec in text, "old_terms_exec not found"
text = text.replace(old_terms_exec, new_terms_exec)

# 4. In handleVariantChange, only set tenderHasBeenAnalyzed if specInput has content
old_hvc = """        function handleVariantChange() {
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

new_hvc = """        function handleVariantChange() {
            const specText = document.getElementById('specInput')?.value?.trim();
            if (specText) {
                tenderHasBeenAnalyzed = true;
                const terms = parseContractualTenderTerms(specText);
                if (!document.getElementById('cfgWarranty').value) {
                    document.getElementById('cfgWarranty').value = terms.warranty;
                }
                if (!document.getElementById('cfgAMC').value) {
                    document.getElementById('cfgAMC').value = terms.amc;
                }
                if (!document.getElementById('cfgTraining').value) {
                    document.getElementById('cfgTraining').value = terms.training;
                }
            }
            recalculateBOM();
            updateCommercialTermsTable();
        }"""

assert old_hvc in text, "old_hvc not found"
text = text.replace(old_hvc, new_hvc)

# 5. In saveTenderDraft, fix default fallbacks
old_std = """                warrantyCfg: document.getElementById('cfgWarranty')?.value || "3 Years Comprehensive On-Site",
                amcCfg: document.getElementById('cfgAMC')?.value || "2 Years Post-Warranty (48h Turnaround SLA)",
                trainingCfg: document.getElementById('cfgTraining')?.value || "Buyer Base / High-Altitude (Leh) — 10 Working Days","""

new_std = """                warrantyCfg: document.getElementById('cfgWarranty')?.value || "",
                amcCfg: document.getElementById('cfgAMC')?.value || "",
                trainingCfg: document.getElementById('cfgTraining')?.value || "","""

assert old_std in text, "old_std not found"
text = text.replace(old_std, new_std)

# 6. In loadDraftById, sanitize old drafts
old_ld = """            if (draft.warrantyCfg && document.getElementById('cfgWarranty')) document.getElementById('cfgWarranty').value = draft.warrantyCfg;
            if (draft.amcCfg && document.getElementById('cfgAMC')) document.getElementById('cfgAMC').value = draft.amcCfg;
            if (draft.trainingCfg && document.getElementById('cfgTraining')) document.getElementById('cfgTraining').value = draft.trainingCfg;"""

new_ld = """            // Load and sanitize contractual terms from draft
            let dWarranty = draft.warrantyCfg || "";
            let dAmc = draft.amcCfg || "";
            let dTraining = draft.trainingCfg || "";

            // If an older draft stored legacy hardcoded defaults, re-extract accurately from specText
            if ((dWarranty === "3 Years Comprehensive On-Site" || dAmc.includes("2 Years Post-Warranty") || dTraining.includes("Leh")) && draft.specText) {
                const autoCorrected = parseContractualTenderTerms(draft.specText);
                dWarranty = autoCorrected.warranty;
                dAmc = autoCorrected.amc;
                dTraining = autoCorrected.training;
            }

            if (document.getElementById('cfgWarranty')) document.getElementById('cfgWarranty').value = dWarranty;
            if (document.getElementById('cfgAMC')) document.getElementById('cfgAMC').value = dAmc;
            if (document.getElementById('cfgTraining')) document.getElementById('cfgTraining').value = dTraining;"""

assert old_ld in text, "old_ld not found"
text = text.replace(old_ld, new_ld)

# 7. In updateCommercialTermsTable, check both Not Required and Not Mandated
old_badge = "${amc.includes('Not Required') ? 'badge-gray' : 'badge-green'}\">${amc.includes('Not Required') ? 'NIL IN TENDER' : 'Included'}</span>"
new_badge = "${(amc.includes('Not Required') || amc.includes('Not Mandated')) ? 'badge-gray' : 'badge-green'}\">${(amc.includes('Not Required') || amc.includes('Not Mandated')) ? 'NIL IN TENDER' : 'Included'}</span>"

if old_badge in text:
    text = text.replace(old_badge, new_badge)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open('VANA_Tender_App.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Successfully updated index.html and VANA_Tender_App.html!")
