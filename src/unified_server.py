import http.server
import socketserver
import json
import urllib.parse
from tender_engine import TenderRuleEngine
from spec_extractor import SpecExtractorEngine

PORT = 8080
tender_engine = TenderRuleEngine()
spec_extractor = SpecExtractorEngine()

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VANA Spec Extraction & Tender Compliance Suite</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body class="bg-gray-50 text-gray-800 min-h-screen">
    <!-- Header -->
    <header class="bg-blue-900 text-white shadow-md sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-6 py-3 flex justify-between items-center">
            <div class="flex items-center space-x-3">
                <i class="fas fa-microchip text-2xl text-yellow-400"></i>
                <div>
                    <h1 class="text-lg font-bold">VANA DEFENCE & AEROSPACE</h1>
                    <p class="text-xs text-blue-200">Specification Extraction, Compliance Categorization & Deliverable Generator</p>
                </div>
            </div>
            <div class="flex space-x-2">
                <button onclick="switchTab('extractorTab')" id="tabBtn1" class="px-4 py-1.5 rounded-lg text-xs font-bold bg-blue-700 text-white hover:bg-blue-600 transition">
                    <i class="fas fa-file-search mr-1"></i> 1. Spec Extractor & Deliverables
                </button>
                <button onclick="switchTab('tenderTab')" id="tabBtn2" class="px-4 py-1.5 rounded-lg text-xs font-bold bg-blue-950 text-blue-200 hover:bg-blue-800 transition">
                    <i class="fas fa-calculator mr-1"></i> 2. BOM Pricing & Army Rules
                </button>
            </div>
        </div>
    </header>

    <main class="max-w-7xl mx-auto px-6 py-6">
        
        <!-- ================= TAB 1: SPECIFICATION EXTRACTOR ================= -->
        <div id="extractorTab" class="space-y-6">
            <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                <h2 class="text-base font-bold text-gray-900 mb-2 flex items-center">
                    <i class="fas fa-paste text-blue-600 mr-2"></i> Paste Technical Specifications / RFP / Tender Text
                </h2>
                <p class="text-xs text-gray-500 mb-4">Paste any specification document, GeM ATC text, or military BOQ clause below. The AI rule engine will automatically extract hardware items, categorize requirements, identify high-risk non-compliance clauses, and generate mandatory deliverable checklists.</p>
                
                <textarea id="specText" rows="6" class="w-full border border-gray-300 rounded-lg p-3 text-xs font-mono focus:ring-blue-500 focus:border-blue-500" placeholder="Paste technical specification text or clauses here..."></textarea>
                
                <div class="mt-3 flex justify-between items-center">
                    <div class="space-x-2">
                        <button type="button" onclick="loadSampleText('ord')" class="text-xs text-blue-600 hover:underline font-semibold">Load Sample: 10-Inch Ordnance Drone</button>
                        <span class="text-gray-300">|</span>
                        <button type="button" onclick="loadSampleText('tactical')" class="text-xs text-blue-600 hover:underline font-semibold">Load Sample: Tactical Surveillance Drone</button>
                    </div>
                    <button type="button" onclick="analyzeSpecifications()" class="bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold px-6 py-2.5 rounded-lg shadow transition flex items-center">
                        <i class="fas fa-wand-magic-sparkles mr-2"></i> Extract Requirements & Deliverables
                    </button>
                </div>
            </div>

            <!-- Extractor Results Grid -->
            <div id="extractionResults" class="grid grid-cols-1 lg:grid-cols-12 gap-6 hidden">
                
                <!-- Left: Critical Red Flags & Hardware Deliverables (7 cols) -->
                <div class="lg:col-span-7 space-y-6">
                    <!-- Red Flags -->
                    <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-200">
                        <h3 class="text-sm font-bold text-gray-900 mb-3 flex items-center text-red-600">
                            <i class="fas fa-triangle-exclamation mr-2"></i> High-Risk Compliance Gates & Red Flags
                        </h3>
                        <div id="criticalFlagsList" class="space-y-2 text-xs"></div>
                    </div>

                    <!-- Hardware Deliverables -->
                    <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-200">
                        <div class="flex justify-between items-center mb-3">
                            <h3 class="text-sm font-bold text-gray-900 flex items-center text-indigo-700">
                                <i class="fas fa-boxes mr-2"></i> Mandatory Hardware Deliverables List
                            </h3>
                            <span id="hwCount" class="text-xs bg-indigo-50 text-indigo-700 font-bold px-2 py-0.5 rounded">0 Items</span>
                        </div>
                        <div class="overflow-x-auto max-h-80 border rounded-lg">
                            <table class="min-w-full divide-y divide-gray-200 text-xs">
                                <thead class="bg-gray-50 sticky top-0 font-bold text-gray-600">
                                    <tr>
                                        <th class="px-3 py-2 text-left">Subsystem Deliverable</th>
                                        <th class="px-3 py-2 text-left">Specification Match / Clause</th>
                                        <th class="px-3 py-2 text-center">Category</th>
                                    </tr>
                                </thead>
                                <tbody id="hwTableBody" class="divide-y divide-gray-200"></tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- Right: Testing, SLA & Document Submissions (5 cols) -->
                <div class="lg:col-span-5 space-y-6">
                    <!-- Testing Deliverables -->
                    <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-200">
                        <h3 class="text-sm font-bold text-gray-900 mb-3 flex items-center text-yellow-700">
                            <i class="fas fa-vial mr-2"></i> Mandatory Testing, Inspection & Training
                        </h3>
                        <div id="testList" class="space-y-2 text-xs"></div>
                    </div>

                    <!-- Document Checklist -->
                    <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-200">
                        <h3 class="text-sm font-bold text-gray-900 mb-3 flex items-center text-purple-700">
                            <i class="fas fa-folder-closed mr-2"></i> Mandatory Document Submissions
                        </h3>
                        <div id="docList" class="space-y-1.5 text-xs max-h-72 overflow-y-auto"></div>
                    </div>
                </div>

            </div>
        </div>

        <!-- ================= TAB 2: BOM PRICING & ARMY RULES ================= -->
        <div id="tenderTab" class="hidden space-y-6">
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
                <!-- Configurator -->
                <div class="lg:col-span-4 bg-white p-5 rounded-xl shadow-sm border border-gray-200 space-y-3">
                    <h3 class="text-sm font-bold text-gray-900 border-b pb-2">Tender Parameters</h3>
                    <div>
                        <label class="text-xs font-semibold text-gray-600 block mb-1">BOQ Category</label>
                        <select id="t_type" class="w-full border rounded p-2 text-xs">
                            <option value="ORDNANCE_DROPPING">10-Inch Ordnance Dropping Drone (48 Qty)</option>
                            <option value="SURVEILLANCE_DAY_NIGHT">Multi-Mission Tactical Drone (EO+IR)</option>
                        </select>
                    </div>
                    <div>
                        <label class="text-xs font-semibold text-gray-600 block mb-1">Quantity</label>
                        <input type="number" id="t_qty" value="48" class="w-full border rounded p-2 text-xs">
                    </div>
                    <div class="space-y-2 pt-2 border-t text-xs">
                        <label class="flex items-center space-x-2">
                            <input type="checkbox" id="t_no_china" checked class="text-red-600 rounded">
                            <span class="font-semibold text-red-700">Strict Non-Chinese Origin (Zero Chinese parts)</span>
                        </label>
                        <label class="flex items-center space-x-2">
                            <input type="checkbox" id="t_samples" checked class="rounded">
                            <span>Advance Samples Clause Active (3 Units in 5 Days)</span>
                        </label>
                        <label class="flex items-center space-x-2">
                            <input type="checkbox" id="t_ra" checked class="rounded">
                            <span>Reverse Auction (RA) Headroom Buffer (10-15%)</span>
                        </label>
                    </div>
                    <button onclick="calculateBOM()" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 rounded text-xs mt-2">
                        Calculate Costed BOM
                    </button>
                </div>

                <!-- BOM & Cost Output -->
                <div class="lg:col-span-8 space-y-4">
                    <div class="grid grid-cols-3 gap-3 text-center">
                        <div class="bg-blue-50 p-3 rounded-lg border border-blue-200">
                            <p class="text-xs text-blue-600 font-bold uppercase">Hardware Unit Cost</p>
                            <p id="cost_unit" class="text-base font-extrabold text-blue-900">₹0</p>
                        </div>
                        <div class="bg-yellow-50 p-3 rounded-lg border border-yellow-200">
                            <p class="text-xs text-yellow-700 font-bold uppercase">Project Cost (Inc Buffer)</p>
                            <p id="cost_proj" class="text-base font-extrabold text-yellow-900">₹0</p>
                        </div>
                        <div class="bg-green-50 p-3 rounded-lg border border-green-200">
                            <p class="text-xs text-green-700 font-bold uppercase">Suggested Bid (Inc 18% GST)</p>
                            <p id="cost_bid" class="text-base font-extrabold text-green-900">₹0</p>
                        </div>
                    </div>

                    <div class="bg-white p-4 rounded-xl shadow-sm border border-gray-200">
                        <h4 class="text-xs font-bold uppercase text-gray-700 mb-2">Non-Chinese Compliant Component Breakdown</h4>
                        <div class="overflow-x-auto max-h-80 border rounded">
                            <table class="min-w-full divide-y divide-gray-200 text-xs">
                                <thead class="bg-gray-50 font-bold">
                                    <tr>
                                        <th class="px-2 py-1 text-left">Category</th>
                                        <th class="px-2 py-1 text-left">Component</th>
                                        <th class="px-2 py-1 text-center">Origin</th>
                                        <th class="px-2 py-1 text-center">Qty</th>
                                        <th class="px-2 py-1 text-right">Unit Price</th>
                                    </tr>
                                </thead>
                                <tbody id="bomRows" class="divide-y divide-gray-200"></tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </main>

    <script>
        function switchTab(tabId) {
            document.getElementById('extractorTab').classList.toggle('hidden', tabId !== 'extractorTab');
            document.getElementById('tenderTab').classList.toggle('hidden', tabId !== 'tenderTab');
            document.getElementById('tabBtn1').className = tabId === 'extractorTab' ? 'px-4 py-1.5 rounded-lg text-xs font-bold bg-blue-700 text-white' : 'px-4 py-1.5 rounded-lg text-xs font-bold bg-blue-950 text-blue-200';
            document.getElementById('tabBtn2').className = tabId === 'tenderTab' ? 'px-4 py-1.5 rounded-lg text-xs font-bold bg-blue-700 text-white' : 'px-4 py-1.5 rounded-lg text-xs font-bold bg-blue-950 text-blue-200';
        }

        const SAMPLES = {
            ord: `BOQ Title: 10 Inch Ord Dropping Drone\\nItem Category: Frame, Brushless Motors, 10 Inch Prop Set, Flight Controller, ESC, FPV Camera, VTX, GPS Module with Compass, Battery Pack, Dual Band Receiver, Radio Controller, Payload Holder with servo Release Mechanism, Allied Accessories, Connectors and Cables, Tool Set, User Technical Manual & Log book, Hard Case\\nQuantity: 48 Nos\\nOPTION CLAUSE: The Purchaser reserves the right to increase or decrease the quantity to be ordered up to 25 percent of bid quantity.\\nSample Clause: After award of contract - Successful Bidder shall submit 3 samples for Buyer approval within 5 days of award of contract.\\nUndertaking Certificate: We hereby confirm that we shall not use any components, parts, material and product sourced from china for the manufacturing of drone.\\nMalicious Code Certificate: Hardware and software being offered does not contain Embedded Malicious code.\\nIT equipment shall be IPv6 ready from day one.\\nReverse Auction: RA would be conducted amongst first 50% lowest priced technically qualified bidders.`,
            tactical: `BOQ Title: Multi Mission Tactical Drone / Surveillance Drone System\\nQuantity: 2 Pieces\\nScope of supply: Supply Installation Testing Commissioning of Goods and Training of operators.\\nInspection: Post Receipt Inspection at consignee site by Board of Officers.\\nUndertaking: Zero parts sourced from China.\\nMake in India: Minimum 50% Local Content required for qualifying as Class 1 Local Supplier.\\nScope of supply includes Training: 5 employees to be trained at HQ 4 Arty Bde for duration of 10 days.\\nWarranty: Warranty period of supplied products shall be 1 years from date of acceptance.\\nResidual Life: Minimum 3 years residual market life.`
        };

        function loadSampleText(type) {
            document.getElementById('specText').value = SAMPLES[type];
        }

        async function analyzeSpecifications() {
            const text = document.getElementById('specText').value;
            if (!text.trim()) {
                alert("Please paste specification text first.");
                return;
            }

            const res = await fetch('/api/extract', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text: text})
            });
            const data = await res.json();
            renderExtraction(data);
        }

        function renderExtraction(data) {
            document.getElementById('extractionResults').classList.remove('hidden');
            
            // Flags
            const flagBox = document.getElementById('criticalFlagsList');
            flagBox.innerHTML = '';
            data.critical_flags.forEach(f => {
                flagBox.innerHTML += `
                    <div class="p-2.5 bg-red-50 border-l-4 border-red-500 rounded">
                        <span class="font-bold text-red-900 uppercase">${f.flag}</span>
                        <p class="text-gray-700 mt-0.5">${f.action}</p>
                    </div>
                `;
            });

            // Hardware
            document.getElementById('hwCount').innerText = data.hardware_deliverables.length + " Items";
            const hwTable = document.getElementById('hwTableBody');
            hwTable.innerHTML = '';
            data.hardware_deliverables.forEach(hw => {
                hwTable.innerHTML += `
                    <tr class="hover:bg-gray-50">
                        <td class="px-3 py-1.5 font-bold text-blue-900">${hw.subsystem}</td>
                        <td class="px-3 py-1.5 text-gray-600">${hw.tender_ref}</td>
                        <td class="px-3 py-1.5 text-center font-semibold text-gray-500">${hw.source_clause}</td>
                    </tr>
                `;
            });

            // Testing
            const testBox = document.getElementById('testList');
            testBox.innerHTML = '';
            data.testing_deliverables.forEach(t => {
                testBox.innerHTML += `
                    <div class="p-2 bg-yellow-50 border border-yellow-200 rounded">
                        <p class="font-bold text-yellow-900">${t.name}</p>
                        <p class="text-gray-500 text-xs">${t.type} • Timeline: ${t.timeline || 'Contractual'}</p>
                    </div>
                `;
            });

            // Docs
            const docBox = document.getElementById('docList');
            docBox.innerHTML = '';
            data.document_deliverables.forEach(d => {
                docBox.innerHTML += `
                    <label class="flex items-center space-x-2 p-1.5 hover:bg-gray-100 rounded cursor-pointer">
                        <input type="checkbox" class="rounded text-purple-600 h-3.5 w-3.5">
                        <span class="text-gray-800 font-medium">${d.name}</span>
                    </label>
                `;
            });
        }

        async function calculateBOM() {
            const payload = {
                tender_type: document.getElementById('t_type').value,
                quantity: parseInt(document.getElementById('t_qty').value) || 1,
                no_chinese_components: document.getElementById('t_no_china').checked,
                advance_sample_required: document.getElementById('t_samples').checked,
                reverse_auction_enabled: document.getElementById('t_ra').checked
            };

            const res = await fetch('/api/evaluate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            const s = data.tender_summary;
            document.getElementById('cost_unit').innerText = "₹" + s.bom_unit_hardware_cost.toLocaleString('en-IN');
            document.getElementById('cost_proj').innerText = "₹" + s.total_estimated_cost.toLocaleString('en-IN');
            document.getElementById('cost_bid').innerText = "₹" + s.suggested_bid_with_gst.toLocaleString('en-IN');

            const tbody = document.getElementById('bomRows');
            tbody.innerHTML = '';
            data.calculated_bom.forEach(b => {
                tbody.innerHTML += `
                    <tr>
                        <td class="px-2 py-1 font-semibold">${b.category}</td>
                        <td class="px-2 py-1">${b.part}</td>
                        <td class="px-2 py-1 text-center"><span class="px-1.5 py-0.5 rounded text-xs ${b.origin==='India'?'bg-green-100 text-green-800':'bg-gray-100'}">${b.origin}</span></td>
                        <td class="px-2 py-1 text-center font-bold">${b.qty_per_unit}</td>
                        <td class="px-2 py-1 text-right font-medium">₹${b.unit_cost.toLocaleString('en-IN')}</td>
                    </tr>
                `;
            });
        }

        // On load
        window.onload = function() {
            loadSampleText('ord');
            analyzeSpecifications();
            calculateBOM();
        };
    </script>
</body>
</html>
"""

class UnifiedRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        elif self.path == "/health":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy"}).encode("utf-8"))
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        payload = json.loads(post_data.decode("utf-8"))

        if self.path == "/api/extract":
            text = payload.get("text", "")
            result = spec_extractor.analyze_specification_text(text)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode("utf-8"))

        elif self.path == "/api/evaluate":
            result = tender_engine.evaluate_tender(payload)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode("utf-8"))
        else:
            self.send_error(404, "Endpoint Not Found")

def run():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), UnifiedRequestHandler) as httpd:
        print(f"VANA Automated Extraction & Compliance Suite running at http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run()
