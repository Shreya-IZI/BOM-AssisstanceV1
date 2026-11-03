with open('/home/izi-system/Documents/Vana_BOMAutomation/index.html') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'tenderDocText ? "=== SECTION 1' in line:
        new_lines.append('                    tenderDocText ? ("=== SECTION 1: COMMERCIAL TENDER DOCUMENT ===\\n" + tenderDocText) : "",\n')
    elif 'techSpecText ? "=== SECTION 2' in line:
        new_lines.append('                    techSpecText ? ("=== SECTION 2: TECHNICAL SPECIFICATIONS & PARAMETERS ===\\n" + techSpecText) : ""\n')
    else:
        new_lines.append(line)

with open('/home/izi-system/Documents/Vana_BOMAutomation/index.html', 'w') as f:
    f.writelines(new_lines)
print("Line-by-line replacement done!")
