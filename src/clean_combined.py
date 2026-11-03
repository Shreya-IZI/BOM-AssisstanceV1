with open('/home/izi-system/Documents/Vana_BOMAutomation/index.html') as f:
    text = f.read()

import re
bad_block = """                const combined = [
                    tenderDocText ? ("=== SECTION 1: COMMERCIAL TENDER DOCUMENT ===\\n" + tenderDocText) : "",
" + tenderDocText : "",
                    techSpecText ? ("=== SECTION 2: TECHNICAL SPECIFICATIONS & PARAMETERS ===\\n" + techSpecText) : ""
" + techSpecText : ""
                ].filter(Boolean).join("

");"""

good_block = """                const combined = [
                    tenderDocText ? ("=== SECTION 1: COMMERCIAL TENDER DOCUMENT ===\\n" + tenderDocText) : "",
                    techSpecText ? ("=== SECTION 2: TECHNICAL SPECIFICATIONS & PARAMETERS ===\\n" + techSpecText) : ""
                ].filter(Boolean).join("\\n\\n");"""

text = text.replace(bad_block, good_block)
with open('/home/izi-system/Documents/Vana_BOMAutomation/index.html', 'w') as f:
    f.write(text)

print("Cleaned up combined block cleanly!")
