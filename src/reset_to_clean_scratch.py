with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update bomVariant select to have placeholder as first option
old_variant_start = """                            <select id="bomVariant" onchange="handleVariantChange()" style="width:100%; border:1px solid var(--border-dark); padding:6px 10px; border-radius:4px; font-size:12px; font-weight:600;">
                                <optgroup label="Tactical FPV Drones (Kamikaze / Strike / Recon)">"""

new_variant_start = """                            <select id="bomVariant" onchange="handleVariantChange()" style="width:100%; border:1px solid var(--border-dark); padding:6px 10px; border-radius:4px; font-size:12px; font-weight:600;">
                                <option value="" disabled selected>-- Select Platform or Upload Tender in Step 1 --</option>
                                <optgroup label="Tactical FPV Drones (Kamikaze / Strike / Recon)">"""

if old_variant_start in html:
    html = html.replace(old_variant_start, new_variant_start)
    print("[1/5] Added default disabled placeholder option to bomVariant")
else:
    print("Warning: old_variant_start not found")

# 2. Reset bomQty from 48 to empty placeholder
old_qty = '<input type="number" id="bomQty" value="48" min="1" onchange="recalculateBOM()"'
new_qty = '<input type="number" id="bomQty" value="" placeholder="e.g. 10" min="1" onchange="recalculateBOM()"'

if old_qty in html:
    html = html.replace(old_qty, new_qty)
    print("[2/5] Reset bomQty to blank placeholder")
else:
    print("Warning: old_qty not found")

# 3. Update recalculateBOM guard
old_recalc_guard = """            if (!tenderHasBeenAnalyzed) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="6" style="text-align:center; padding:36px 16px; color:#94a3b8; font-style:italic;">
                            <i class="fas fa-file-invoice" style="font-size:24px; display:block; margin-bottom:8px; color:#cbd5e1;"></i>
                            No tender loaded. Please go to "1. Tender Requirements", upload a GeM PDF or load a sample to generate the BOM.
                        </td>
                    </tr>
                `;
                document.getElementById('priceUnitBOM').innerText = "₹0";
                document.getElementById('priceTotalCost').innerText = "₹0";
                document.getElementById('priceBidEx').innerText = "₹0";
                document.getElementById('priceBidInc').innerText = "₹0";
                const miiBadge = document.getElementById('miiSummaryBadge');
                if (miiBadge) {
                    miiBadge.innerText = "MII: Pending Tender";
                    miiBadge.className = "badge badge-gray";
                }
                return;
            }"""

new_recalc_guard = """            const variantVal = document.getElementById('bomVariant')?.value || "";
            if (!tenderHasBeenAnalyzed || !variantVal) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="6" style="text-align:center; padding:36px 16px; color:#94a3b8; font-style:italic;">
                            <i class="fas fa-file-invoice" style="font-size:24px; display:block; margin-bottom:8px; color:#cbd5e1;"></i>
                            No tender loaded. Please go to "1. Upload & Scan", upload a GeM PDF or load a sample to generate the BOM.
                        </td>
                    </tr>
                `;
                document.getElementById('priceUnitBOM').innerText = "₹0";
                document.getElementById('priceTotalCost').innerText = "₹0";
                document.getElementById('priceBidEx').innerText = "₹0";
                document.getElementById('priceBidInc').innerText = "₹0";
                const miiBadge = document.getElementById('miiSummaryBadge');
                if (miiBadge) {
                    miiBadge.innerText = "MII: Pending Tender";
                    miiBadge.className = "badge badge-gray";
                }
                return;
            }"""

if old_recalc_guard in html:
    html = html.replace(old_recalc_guard, new_recalc_guard)
    print("[3/5] recalculateBOM guard updated to require both tenderHasBeenAnalyzed and variantVal")
else:
    print("Warning: old_recalc_guard not found")

# 4. Update updateCommercialTermsTable guard
old_comm_guard = """            if (!tenderHasBeenAnalyzed) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="6" style="text-align:center; padding:32px 16px; color:#94a3b8; font-style:italic;">
                            <i class="fas fa-file-contract" style="font-size:24px; display:block; margin-bottom:8px; color:#cbd5e1;"></i>
                            No tender loaded. Contractual terms (Warranty, AMC, and Training) will automatically populate when you upload or scan a tender in Step 1.
                        </td>
                    </tr>
                `;
                return;
            }"""

new_comm_guard = """            const variantVal = document.getElementById('bomVariant')?.value || "";
            if (!tenderHasBeenAnalyzed || !variantVal) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="6" style="text-align:center; padding:32px 16px; color:#94a3b8; font-style:italic;">
                            <i class="fas fa-file-contract" style="font-size:24px; display:block; margin-bottom:8px; color:#cbd5e1;"></i>
                            No tender loaded. Contractual terms (Warranty, AMC, and Training) will automatically populate when you upload or scan a tender in Step 1.
                        </td>
                    </tr>
                `;
                return;
            }"""

if old_comm_guard in html:
    html = html.replace(old_comm_guard, new_comm_guard)
    print("[4/5] updateCommercialTermsTable guard updated")
else:
    print("Warning: old_comm_guard not found")

# 5. Add guards to modals so they don't open with dummy/zero data when nothing is loaded
modal_guards = """
        // Modal Guards for Empty Initial State
        function checkTenderLoaded(actionName) {
            const v = document.getElementById('bomVariant')?.value;
            if (!tenderHasBeenAnalyzed || !v) {
                alert(`No tender loaded. Please go to Step 1 and upload a GeM PDF or load a sample first to ${actionName}.`);
                return false;
            }
            return true;
        }
"""

if 'function checkTenderLoaded(actionName)' not in html:
    html = html.replace('// 1. MAKE IN INDIA (MII) LOCAL CONTENT & CERTIFICATE', modal_guards + '\n        // 1. MAKE IN INDIA (MII) LOCAL CONTENT & CERTIFICATE')
    html = html.replace("function openMIIModal() {", "function openMIIModal() {\n            if (!checkTenderLoaded('generate the Make in India certificate')) return;")
    html = html.replace("function openRAModal() {", "function openRAModal() {\n            if (!checkTenderLoaded('simulate the Reverse Auction')) return;")
    html = html.replace("function openComplianceModal() {", "function openComplianceModal() {\n            if (!checkTenderLoaded('generate the compliance matrix')) return;")
    html = html.replace("function printOrSavePDF() {", "function printOrSavePDF() {\n            if (!checkTenderLoaded('export PDF')) return;")
    print("[5/5] Added empty state guards to modals and PDF export")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Reset to clean scratch script completed!")
