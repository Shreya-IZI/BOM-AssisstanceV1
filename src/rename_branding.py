with open('/home/izi-system/Documents/Vana_BOMAutomation/index.html') as f:
    c = f.read()

# Update Title
c = c.replace('<title>VANA Enterprise — Technical Bidding & BOM Workspace</title>', '<title>BOM Assist — Autonomous Drone Tender & BOM Intelligence Workspace</title>')

# Update Brand Section in Header
c = c.replace('<div class="brand-logo">V</div>', '<div class="brand-logo" style="background:#0284c7; font-weight:900;">B</div>')
c = c.replace('<span class="brand-name">VANA DEFENCE & AEROSPACE</span>', '<span class="brand-name">BOM ASSIST</span>')
c = c.replace('<span class="brand-subtitle">Tender Intelligence & Engineering Rules System</span>', '<span class="brand-subtitle">Autonomous Drone Tender & Engineering Intelligence</span>')

# Update Base revenue label
c = c.replace('Base revenue to VANA (Excl. GST)', 'Base Revenue / Company Target (Excl. GST)')

# Update Gaps text
c = c.replace("When a tender asks for something not in VANA's catalog", "When a tender asks for something not in the master catalog")
c = c.replace("If a tender asks for an exotic item or custom bracket not found in VANA's current catalog", "If a tender asks for an exotic item or custom bracket not found in the current catalog")

# Update Catalog Section Title
c = c.replace('<h2 class="section-title">VANA Master Item Catalog</h2>', '<h2 class="section-title">Multi-Fleet Master Component Catalog</h2>')

# Update User Guide modal title
c = c.replace('VANA Workspace User Guide', 'BOM Assist Workspace User Guide')

# Update CSV export header
c = c.replace('VANA DEFENCE & AEROSPACE — OFFICIAL COMPLIANT BOM REPORT', 'BOM ASSIST — OFFICIAL MULTI-FLEET COMPLIANT BOM REPORT')

with open('/home/izi-system/Documents/Vana_BOMAutomation/index.html', 'w') as f:
    f.write(c)

print("Branding successfully renamed to BOM Assist!")
