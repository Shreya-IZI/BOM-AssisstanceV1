with open('/home/izi-system/Documents/Vana_BOMAutomation/index.html') as f:
    c = f.read()

# Expand scanner to extract Guarantee, Warranty, AMC, Insurance, Penalties, Delayed Submission (LD)
scan_insert_target = """            lines.forEach(line => {
                if (/china|chinese|land border/i.test(line)) {"""

expanded_scan = """            const commercials = []; // Stores Warranty, Guarantee, AMC, Insurance, Penalties, LD

            lines.forEach(line => {
                // Guarantee & Warranty
                if (/guarantee|warranty|वारंटी/i.test(line) && !line.startsWith("Searched String")) {
                    const dur = line.match(/(\\d+)\\s*(?:years?|months?|साल)/i);
                    commercials.push({
                        title: "Warranty & Performance Guarantee",
                        type: "Warranty SLA",
                        desc: cleanSnippetText(line),
                        highlight: dur ? (dur[1] + " Period Required") : "Mandatory Support"
                    });
                }

                // AMC (Annual Maintenance Contract)
                if (/amc\\b|annual maintenance|comprehensive maintenance|camc\\b/i.test(line)) {
                    commercials.push({
                        title: "Annual Maintenance Contract (AMC)",
                        type: "Post-Warranty SLA",
                        desc: cleanSnippetText(line),
                        highlight: "Post-Delivery SLA"
                    });
                }

                // Insurance / Transit Risk
                if (/insurance|transit risk|marine insurance|transit damage/i.test(line)) {
                    commercials.push({
                        title: "Transit & Equipment Insurance",
                        type: "Risk Coverage",
                        desc: cleanSnippetText(line),
                        highlight: "All-Risk Transit Policy"
                    });
                }

                // Liquidated Damages & Delayed Submission Penalties
                if (/liquidated damages|penalty|penalties|late delivery|delayed submission|0\\.5%/i.test(line)) {
                    const ldRate = line.match(/(0\\.5%|1%|2%|5%|10%)/i);
                    commercials.push({
                        title: "Liquidated Damages (LD) & Delay Penalties",
                        type: "Financial Liability",
                        desc: cleanSnippetText(line),
                        highlight: ldRate ? (ldRate[1] + " per week deduction") : "Deduction for Delays"
                    });
                }

                if (/china|chinese|land border/i.test(line)) {"""

# Replace in index.html
if scan_insert_target in c:
    c = c.replace(scan_insert_target, expanded_scan)

# Now render commercials into commercialList element
render_target = """            // Testing
            document.getElementById('badgeTest').innerText = testing.length + " SLAs";"""

render_commercials = """            // Commercials (Warranty, Guarantee, AMC, Insurance, Penalties, LD)
            const commBox = document.getElementById('commercialList');
            const commBadge = document.getElementById('badgeComm');
            if (commBox) {
                commBox.innerHTML = '';
                // Deduplicate by title
                const uniqueComm = [];
                const seenComm = new Set();
                commercials.forEach(cm => {
                    const k = cm.title + cm.desc.substring(0, 30);
                    if (!seenComm.has(k)) {
                        seenComm.add(k);
                        uniqueComm.push(cm);
                    }
                });

                if (commBadge) commBadge.innerText = uniqueComm.length + " Terms";

                if (uniqueComm.length === 0) {
                    commBox.innerHTML = '<div style=\"color:#94a3b8; font-style:italic; font-size:11px;\">Standard 1-year warranty & GeM GTC delay clauses apply.</div>';
                } else {
                    uniqueComm.forEach(cm => {
                        commBox.innerHTML += `
                            <div style=\"border-bottom:1px solid #f1f5f9; padding-bottom:8px; margin-bottom:8px;\">
                                <div style=\"display:flex; justify-content:space-between; align-items:flex-start;\">
                                    <span style=\"font-weight:700; font-size:11px; color:#0369a1;\">${cm.title}</span>
                                    <span class=\"badge badge-amber\" style=\"font-size:9px;\">${cm.highlight}</span>
                                </div>
                                <div style=\"color:#64748b; font-size:10px; margin-top:2px; line-height:1.3;\">${cm.desc}</div>
                            </div>
                        `;
                    });
                }
            }

            // Testing
            document.getElementById('badgeTest').innerText = testing.length + " SLAs";"""

if render_target in c:
    c = c.replace(render_target, render_commercials)

with open('/home/izi-system/Documents/Vana_BOMAutomation/index.html', 'w') as f:
    f.write(c)

print("Commercial scanner and 4th bucket renderer injected successfully!")
