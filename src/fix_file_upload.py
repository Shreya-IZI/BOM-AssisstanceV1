import json

with open('/home/izi-system/Documents/Vana_BOMAutomation/index.html') as f:
    html = f.read()

# Fix the processDualFile function cleanly
bad_func = """        async function processDualFile(file, type) {
            const statusDiv = document.getElementById(type === 'tender' ? 'fileUploadStatusTender' : 'fileUploadStatusTech');
            statusDiv.style.display = 'block';
            statusDiv.innerText = ;

            try {
                let extractedText = "";
                if (file.name.toLowerCase().endsWith('.pdf')) {
                    extractedText = await extractTextFromPDF(file);
                } else {
                    extractedText = await new Promise((res, rej) => {
                        const reader = new FileReader();
                        reader.onload = (evt) => res(evt.target.result);
                        reader.onerror = rej;
                        reader.readAsText(file);
                    });
                }

                if (type === 'tender') {
                    tenderDocText = extractedText;
                    statusDiv.innerText = ;
                } else {
                    techSpecText = extractedText;
                    statusDiv.innerText = ;
                }

                // Combine both documents into unified specification buffer
                const combined = [
                    tenderDocText ? `=== SECTION 1: COMMERCIAL TENDER DOCUMENT ===\\n` : "",
                    techSpecText ? `=== SECTION 2: TECHNICAL SPECIFICATIONS & PARAMETERS ===\\n` : ""
                ].filter(Boolean).join("\\n\\n");

                document.getElementById('specInput').value = combined;
                updateCharCount();
                executeAnalysis();
            } catch (err) {
                console.error('File parsing error:', err);
                statusDiv.innerText = ;
            }
        }"""

good_func = """        async function processDualFile(file, type) {
            const statusDiv = document.getElementById(type === 'tender' ? 'fileUploadStatusTender' : 'fileUploadStatusTech');
            statusDiv.style.display = 'block';
            statusDiv.innerText = "Ingesting " + file.name + "...";

            try {
                let extractedText = "";
                if (file.name.toLowerCase().endsWith('.pdf')) {
                    extractedText = await extractTextFromPDF(file);
                } else {
                    extractedText = await new Promise((res, rej) => {
                        const reader = new FileReader();
                        reader.onload = (evt) => res(evt.target.result);
                        reader.onerror = rej;
                        reader.readAsText(file);
                    });
                }

                if (type === 'tender') {
                    tenderDocText = extractedText;
                    statusDiv.innerText = "[✓] Loaded Tender: " + file.name + " (" + Math.round(file.size/1024) + " KB)";
                } else {
                    techSpecText = extractedText;
                    statusDiv.innerText = "[✓] Loaded Tech Specs: " + file.name + " (" + Math.round(file.size/1024) + " KB)";
                }

                // Combine both documents into unified specification buffer
                const combined = [
                    tenderDocText ? "=== SECTION 1: COMMERCIAL TENDER DOCUMENT ===\\n" + tenderDocText : "",
                    techSpecText ? "=== SECTION 2: TECHNICAL SPECIFICATIONS & PARAMETERS ===\\n" + techSpecText : ""
                ].filter(Boolean).join("\\n\\n");

                document.getElementById('specInput').value = combined;
                updateCharCount();
                executeAnalysis();
            } catch (err) {
                console.error('File parsing error:', err);
                statusDiv.innerText = "Error parsing " + file.name;
            }
        }"""

if bad_func in html:
    html = html.replace(bad_func, good_func)
    with open('/home/izi-system/Documents/Vana_BOMAutomation/index.html', 'w') as f:
        f.write(html)
    print("Fixed processDualFile strings successfully!")
else:
    print("bad_func not matched")
