import http.server
import socketserver
import json
import urllib.parse
from tender_engine import TenderRuleEngine

PORT = 8080
engine = TenderRuleEngine()

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VANA Tender & Bid Automation System</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        .badge-red { background-color: #fee2e2; color: #991b1b; }
        .badge-amber { background-color: #fef3c7; color: #92400e; }
        .badge-green { background-color: #d1fae5; color: #065f46; }
    </style>
</head>
<body class="bg-gray-50 text-gray-800 min-h-screen">
    <!-- Header -->
    <header class="bg-blue-900 text-white shadow-lg sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
            <div class="flex items-center space-x-3">
                <i class="fas fa-fighter-jet text-3xl text-yellow-400"></i>
                <div>
                    <h1 class="text-xl font-bold tracking-wide">VANA DEFENCE & AEROSPACE</h1>
                    <p class="text-xs text-blue-200">Autonomous Tender Compliance & BOM Generation Engine</p>
                </div>
            </div>
            <div class="text-right text-xs text-blue-200">
                <span class="inline-block bg-blue-800 px-3 py-1 rounded-full text-green-300 font-semibold">
                    <i class="fas fa-shield-alt mr-1"></i> MoD & GeM Rules Enabled
                </span>
            </div>
        </div>
    </header>

    <main class="max-w-7xl mx-auto px-6 py-8 grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        <!-- Left Column: Tender Configuration Form (4 Cols) -->
        <section class="lg:col-span-5 bg-white p-6 rounded-xl shadow-md border border-gray-200">
            <h2 class="text-lg font-bold text-gray-900 mb-4 flex items-center border-b pb-2">
                <i class="fas fa-file-contract text-blue-700 mr-2"></i> 1. Tender Requirements Input
            </h2>
            
            <form id="tenderForm" class="space-y-4">
                <div>
                    <label class="block text-xs font-semibold uppercase text-gray-600 mb-1">Target Client / Ministry</label>
                    <select id="client" class="w-full border-gray-300 rounded-md shadow-sm border p-2 text-sm focus:ring-blue-500 focus:border-blue-500">
                        <option value="INDIAN_ARMY">Indian Army / Ministry of Defence (MoD)</option>
                        <option value="PARAMILITARY">Paramilitary / MHA (CRPF, BSF, ITBP)</option>
                        <option value="CIVILIAN">Civilian / PSU / Survey of India</option>
                    </select>
                </div>

                <div>
                    <label class="block text-xs font-semibold uppercase text-gray-600 mb-1">VANA Platform / BOQ Category</label>
                    <select id="tender_type" class="w-full border-gray-300 rounded-md shadow-sm border p-2 text-sm focus:ring-blue-500 focus:border-blue-500">
                        <option value="ORDNANCE_DROPPING">10-inch Ordnance Dropping Drone (Kamikaze / Attack)</option>
                        <option value="SURVEILLANCE_DAY_NIGHT">Multi-Mission Tactical Drone (EO+IR Day/Night)</option>
                    </select>
                </div>

                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-semibold uppercase text-gray-600 mb-1">Tender Quantity</label>
                        <input type="number" id="quantity" value="48" min="1" class="w-full border-gray-300 rounded-md shadow-sm border p-2 text-sm">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold uppercase text-gray-600 mb-1">Delivery Lead Time</label>
                        <div class="flex items-center">
                            <input type="number" id="delivery_days" value="15" min="1" class="w-full border-gray-300 rounded-md shadow-sm border p-2 text-sm">
                            <span class="ml-2 text-xs text-gray-500 font-bold">Days</span>
                        </div>
                    </div>
                </div>

                <div class="border-t pt-4">
                    <h3 class="text-xs font-bold uppercase text-gray-500 tracking-wider mb-2">Special GeM & MoD Clauses</h3>
                    
                    <div class="space-y-2">
                        <label class="flex items-center space-x-2 text-sm text-gray-700">
                            <input type="checkbox" id="no_chinese_components" checked class="rounded text-red-600 focus:ring-red-500 h-4 w-4">
                            <span class="font-medium text-red-700">Strict Non-Chinese Origin Undertaking (Zero Chinese Parts)</span>
                        </label>

                        <label class="flex items-center space-x-2 text-sm text-gray-700">
                            <input type="checkbox" id="advance_sample_required" checked class="rounded text-blue-600 h-4 w-4">
                            <span>Advance Sample Required for Approval</span>
                        </label>

                        <div id="sample_details" class="pl-6 grid grid-cols-2 gap-2 text-xs bg-gray-50 p-2 rounded">
                            <div>
                                <label class="text-gray-500">Sample Units:</label>
                                <input type="number" id="advance_sample_qty" value="3" class="w-full border p-1 rounded">
                            </div>
                            <div>
                                <label class="text-gray-500">Days to Submit:</label>
                                <input type="number" id="advance_sample_days" value="5" class="w-full border p-1 rounded">
                            </div>
                        </div>

                        <label class="flex items-center space-x-2 text-sm text-gray-700">
                            <input type="checkbox" id="reverse_auction_enabled" checked class="rounded text-blue-600 h-4 w-4">
                            <span>Reverse Auction (RA) Enabled (Price War Risk)</span>
                        </label>

                        <label class="flex items-center space-x-2 text-sm text-gray-700">
                            <input type="checkbox" id="training_required" class="rounded text-blue-600 h-4 w-4">
                            <span>On-Site Training & Commissioning in Scope</span>
                        </label>
                    </div>
                </div>

                <div class="border-t pt-4">
                    <label class="block text-xs font-semibold uppercase text-gray-600 mb-1">Buyer Option Clause (Repeat Order)</label>
                    <select id="option_clause_pct" class="w-full border-gray-300 rounded-md shadow-sm border p-2 text-sm">
                        <option value="25">Up to +25% Additional Quantity at Contracted Rate</option>
                        <option value="50">Up to +50% Additional Quantity at Contracted Rate</option>
                        <option value="0">None / No Option Clause</option>
                    </select>
                </div>

                <button type="button" onclick="runEvaluation()" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-lg shadow-md transition duration-150 flex justify-center items-center">
                    <i class="fas fa-calculator mr-2"></i> Evaluate Tender & Generate BOM
                </button>
            </form>
        </section>

        <!-- Right Column: Compliance Dashboard, Red Flags & Auto-BOM (7 Cols) -->
        <section class="lg:col-span-7 space-y-6">
            
            <!-- Financial & Bid Pricing Card -->
            <div class="bg-white p-6 rounded-xl shadow-md border border-gray-200">
                <h2 class="text-lg font-bold text-gray-900 mb-4 flex items-center justify-between border-b pb-2">
                    <span><i class="fas fa-coins text-yellow-500 mr-2"></i> Cost Estimation & Quote Guidance</span>
                    <span id="quantity_tag" class="text-xs bg-gray-100 text-gray-700 px-3 py-1 rounded-full font-semibold">Qty: 48</span>
                </h2>

                <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                    <div class="bg-blue-50 p-3 rounded-lg border border-blue-100">
                        <p class="text-xs text-blue-600 uppercase font-bold">Hardware BOM Unit</p>
                        <p id="bom_unit" class="text-base font-extrabold text-blue-900">₹0</p>
                    </div>
                    <div class="bg-gray-50 p-3 rounded-lg border border-gray-200">
                        <p class="text-xs text-gray-500 uppercase font-bold">Total Project Cost</p>
                        <p id="total_cost" class="text-base font-extrabold text-gray-800">₹0</p>
                    </div>
                    <div class="bg-yellow-50 p-3 rounded-lg border border-yellow-200">
                        <p class="text-xs text-yellow-700 uppercase font-bold">Suggested Bid (Ex. GST)</p>
                        <p id="suggested_bid" class="text-base font-extrabold text-yellow-800">₹0</p>
                    </div>
                    <div class="bg-green-50 p-3 rounded-lg border border-green-200">
                        <p class="text-xs text-green-700 uppercase font-bold">Total Bid (Inc. 18% GST)</p>
                        <p id="bid_gst" class="text-base font-extrabold text-green-900">₹0</p>
                    </div>
                </div>

                <div id="cost_breakdown_chips" class="mt-4 flex flex-wrap gap-2 text-xs text-gray-600">
                    <!-- Populated dynamically -->
                </div>
            </div>

            <!-- Critical Compliance Alerts & Risk Matrix -->
            <div class="bg-white p-6 rounded-xl shadow-md border border-gray-200">
                <h2 class="text-lg font-bold text-gray-900 mb-3 flex items-center">
                    <i class="fas fa-exclamation-triangle text-red-500 mr-2"></i> Must-Not-Miss Compliance Gates
                </h2>
                <div id="alerts_container" class="space-y-3">
                    <!-- Populated dynamically -->
                </div>
            </div>

            <!-- Dynamic Auto-Generated Compliant BOM Table -->
            <div class="bg-white p-6 rounded-xl shadow-md border border-gray-200">
                <div class="flex justify-between items-center mb-3">
                    <h2 class="text-lg font-bold text-gray-900 flex items-center">
                        <i class="fas fa-list-ol text-indigo-600 mr-2"></i> Compliant BOM Explosion
                    </h2>
                    <span class="text-xs bg-green-100 text-green-800 font-semibold px-2.5 py-0.5 rounded-full">
                        <i class="fas fa-check-circle mr-1"></i> 100% Non-Chinese Verified
                    </span>
                </div>
                
                <div class="overflow-x-auto max-h-72 border rounded-lg">
                    <table class="min-w-full divide-y divide-gray-200 text-xs">
                        <thead class="bg-gray-100 sticky top-0">
                            <tr>
                                <th class="px-3 py-2 text-left font-bold text-gray-600">Category</th>
                                <th class="px-3 py-2 text-left font-bold text-gray-600">Selected Component / Assembly</th>
                                <th class="px-3 py-2 text-center font-bold text-gray-600">Origin</th>
                                <th class="px-3 py-2 text-center font-bold text-gray-600">Qty/U</th>
                                <th class="px-3 py-2 text-right font-bold text-gray-600">Unit Cost</th>
                            </tr>
                        </thead>
                        <tbody id="bom_tbody" class="bg-white divide-y divide-gray-200">
                            <!-- Populated dynamically -->
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Mandatory Document Checklist -->
            <div class="bg-white p-6 rounded-xl shadow-md border border-gray-200">
                <h2 class="text-lg font-bold text-gray-900 mb-3 flex items-center">
                    <i class="fas fa-folder-open text-purple-600 mr-2"></i> Mandatory Bid Submission Documents
                </h2>
                <div id="doc_checklist" class="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs">
                    <!-- Populated dynamically -->
                </div>
            </div>

        </section>
    </main>

    <footer class="text-center text-xs text-gray-400 py-6 border-t mt-8">
        VANA Autonomous BOM Automation & Tender Compliance Engine — Built for Defence & GeM Operations
    </footer>

    <script>
        function formatINR(val) {
            return "₹" + Number(val).toLocaleString('en-IN', { maximumFractionDigits: 0 });
        }

        async function runEvaluation() {
            const payload = {
                client: document.getElementById('client').value,
                tender_type: document.getElementById('tender_type').value,
                quantity: parseInt(document.getElementById('quantity').value) || 1,
                delivery_days: parseInt(document.getElementById('delivery_days').value) || 15,
                no_chinese_components: document.getElementById('no_chinese_components').checked,
                advance_sample_required: document.getElementById('advance_sample_required').checked,
                advance_sample_qty: parseInt(document.getElementById('advance_sample_qty').value) || 3,
                advance_sample_days: parseInt(document.getElementById('advance_sample_days').value) || 5,
                reverse_auction_enabled: document.getElementById('reverse_auction_enabled').checked,
                training_required: document.getElementById('training_required').checked,
                option_clause_pct: parseInt(document.getElementById('option_clause_pct').value) || 0
            };

            const response = await fetch('/api/evaluate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            renderDashboard(data);
        }

        function renderDashboard(data) {
            const summary = data.tender_summary;
            document.getElementById('quantity_tag').innerText = "Tender Qty: " + summary.quantity;
            document.getElementById('bom_unit').innerText = formatINR(summary.bom_unit_hardware_cost);
            document.getElementById('total_cost').innerText = formatINR(summary.total_estimated_cost);
            document.getElementById('suggested_bid').innerText = formatINR(summary.suggested_bid_before_gst);
            document.getElementById('bid_gst').innerText = formatINR(summary.suggested_bid_with_gst);

            // Chips
            const chips = document.getElementById('cost_breakdown_chips');
            chips.innerHTML = `
                <span class="bg-gray-100 px-2.5 py-1 rounded">Warranty Reserve (5%): ${formatINR(summary.warranty_buffer)}</span>
                <span class="bg-gray-100 px-2.5 py-1 rounded">Contingency Buffer (4%): ${formatINR(summary.contingency_buffer)}</span>
                <span class="bg-gray-100 px-2.5 py-1 rounded">Officer Inspection Fee: ${formatINR(summary.inspection_buffer)}</span>
                ${summary.training_cost > 0 ? `<span class="bg-blue-100 text-blue-800 px-2.5 py-1 rounded font-semibold">Training & Commissioning: ${formatINR(summary.training_cost)}</span>` : ''}
            `;

            // Alerts
            const alertBox = document.getElementById('alerts_container');
            alertBox.innerHTML = '';

            data.critical_alerts.forEach(a => {
                alertBox.innerHTML += `
                    <div class="p-3 bg-red-50 border-l-4 border-red-500 rounded text-xs text-red-900">
                        <p class="font-bold uppercase tracking-wide flex items-center">
                            <i class="fas fa-ban mr-1.5 text-red-600"></i> ${a.title}
                        </p>
                        <p class="mt-1">${a.detail}</p>
                    </div>
                `;
            });

            data.warnings.forEach(w => {
                alertBox.innerHTML += `
                    <div class="p-3 bg-yellow-50 border-l-4 border-yellow-500 rounded text-xs text-yellow-900">
                        <p class="font-bold uppercase tracking-wide flex items-center">
                            <i class="fas fa-exclamation-circle mr-1.5 text-yellow-600"></i> ${w.title}
                        </p>
                        <p class="mt-1">${w.detail}</p>
                    </div>
                `;
            });

            data.action_items.forEach(act => {
                alertBox.innerHTML += `
                    <div class="p-3 bg-blue-50 border-l-4 border-blue-500 rounded text-xs text-blue-900">
                        <p class="font-bold uppercase tracking-wide flex items-center">
                            <i class="fas fa-tasks mr-1.5 text-blue-600"></i> ${act.title}
                        </p>
                        <p class="mt-1">${act.detail}</p>
                    </div>
                `;
            });

            // BOM Table
            const tbody = document.getElementById('bom_tbody');
            tbody.innerHTML = '';
            data.calculated_bom.forEach(line => {
                tbody.innerHTML += `
                    <tr class="hover:bg-gray-50">
                        <td class="px-3 py-1.5 font-semibold text-gray-700">${line.category}</td>
                        <td class="px-3 py-1.5">${line.part}</td>
                        <td class="px-3 py-1.5 text-center">
                            <span class="px-2 py-0.5 rounded text-xs font-semibold ${line.origin === 'India' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-700'}">
                                ${line.origin}
                            </span>
                        </td>
                        <td class="px-3 py-1.5 text-center font-bold">${line.qty_per_unit}</td>
                        <td class="px-3 py-1.5 text-right font-medium">${formatINR(line.unit_cost)}</td>
                    </tr>
                `;
            });

            // Document checklist
            const docBox = document.getElementById('doc_checklist');
            docBox.innerHTML = '';
            data.mandatory_documents.forEach(doc => {
                docBox.innerHTML += `
                    <label class="flex items-center space-x-2 bg-gray-50 p-2 rounded border border-gray-100 hover:bg-gray-100 cursor-pointer">
                        <input type="checkbox" class="h-3.5 w-3.5 text-blue-600 rounded">
                        <span class="text-gray-700">${doc}</span>
                    </label>
                `;
            });
        }

        // Run default evaluation on load
        window.onload = runEvaluation;
    </script>
</body>
</html>
"""

class TenderRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        elif self.path == "/health":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "running"}).encode("utf-8"))
        else:
            self.send_error(404, "Page Not Found")

    def do_POST(self):
        if self.path == "/api/evaluate":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            payload = json.loads(post_data.decode("utf-8"))
            result = engine.evaluate_tender(payload)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode("utf-8"))
        else:
            self.send_error(404, "Endpoint Not Found")

def start_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), TenderRequestHandler) as httpd:
        print(f"VANA Tender Automation Server running at http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    start_server()
