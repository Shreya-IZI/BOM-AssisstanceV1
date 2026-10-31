import csv
import json
import sqlite3
import re
from pathlib import Path

# Paths
DB_PATH = Path("/home/izi-system/Documents/Vana_BOMAutomation/data/vana_catalog.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

RAW_CSV_DATA = """# Component Category,What it is / Function
01,Motor,Brushless (BLDC) motor that spins the propellers to generate lift & thrust
02,ESC,Electronic Speed Controller — regulates power/RPM delivered to each motor
03,Propeller,Rotor blades that convert motor rotation into aerodynamic thrust
04,Battery,Li-ion / LiPo pack — primary energy source for the electric propulsion
05,Camera / Payload,EO / IR / EO+IR gimbal imaging payload for surveillance & targeting
06,Antenna,RF antenna for command telemetry & video link
07,GPS / GNSS,Satellite positioning & navigation receiver
08,Tethered System,Ground-tethered power & data station for persistent hover
09,GPS-Denied / VIO,Visual-inertial navigation for GPS-denied operation
10,Generator,Portable AC/DC generator for field battery charging
11,Transmitter / RC,Radio controller / ground station for piloting & datalink
12,Anti-Jamming / Anti-Spoof,GNSS resilience module against jamming & spoofing
13,Rugged Laptop / Tablet,Ruggedised ground-control computer
14,Power Module,Current / Voltage Sensor
15,Battery Charger,Recharges Li-ion/LiPo packs; 1-ch & 2-ch for 4S/6S all capacities
16,Navigation Lights,Position & anti-collision strobe lights for orientation / night-BVLOS legality
17,Flight Controller,Core autopilot computer
"""

ITEMS_DATA = [
    # Motors
    ("Motor", "Vector", "3115 SL - 900KV", "BLDC Motor", "India", "BLDC; KV 900; 6-12S", 5000, 1),
    ("Motor", "Vector", "4006 SL - 380KV", "BLDC Motor", "India", "BLDC; KV 380; 6-12S; 4-6 kg AUW", 6500, 1),
    ("Motor", "Vector", "6008SL - 340KV", "BLDC Motor", "India", "BLDC; KV 340; 6-12S; Heavy Lift", 12150, 1),
    ("Motor", "Vector", "5004 pro - 500KV", "BLDC Motor", "India", "BLDC; KV 500; 6-12S", 10200, 1),
    ("Motor", "T Motor", "340KV", "BLDC Motor", "China", "Low-KV endurance BLDC", 9823, 0),
    ("Motor", "T Motor", "780kv", "BLDC Motor", "China", "Higher-KV BLDC for agility", 4400, 0),
    ("Motor", "T Motor", "700kv", "BLDC Motor", "China", "Higher-KV BLDC", 4229, 0),
    ("Motor", "T Motor", "920kv", "BLDC Motor", "China", "Higher-KV BLDC", 3431, 0),
    ("Motor", "T Motor", "380kv", "BLDC Motor", "China", "Low-KV endurance BLDC", 17800, 0),
    ("Motor", "Flameback", "4006 - 360kv", "BLDC Motor", "India", "BLDC 360KV", 5649, 1),
    ("Motor", "Flameback", "6206 - 300KV", "BLDC Motor", "India", "BLDC 300KV Heavy lift", 10999, 1),
    ("Motor", "Flameback", "3115 - 900kv", "BLDC Motor", "India", "BLDC 900KV", 5499, 1),
    ("Motor", "Flameback", "5308 - 340kv", "BLDC Motor", "India", "BLDC 340KV", 8849, 1),
    ("Motor", "T-Motor", "Antigravity MN6007 II", "BLDC Motor", "China", "Thrust ~6.5kg; 155g", 11215, 0),
    ("Motor", "T-Motor", "MN705-S 220KV", "BLDC Motor", "China", "220 KV; 6-12S", 51000, 0),
    ("Motor", "SunnySky", "X4108S 380KV", "BLDC Motor", "China", "380 KV; 6S", 12500, 0),
    ("Motor", "Reflex Drive", "RD5008 340 KV", "BLDC Motor", "India", "RD5008 340KV", 9600, 1),

    # ESC
    ("ESC", "T Motor", "40A ESC", "ESC", "China", "Continuous 40A; 6-12S", 3000, 0),
    ("ESC", "T Motor", "60A ESC", "ESC", "China", "Continuous 60A; 6-12S", 6857, 0),
    ("ESC", "Vector", "40A ESC", "ESC", "India", "Continuous 40A; 2-6S", 6500, 1),
    ("ESC", "Flameback Tech", "45A ESC", "ESC", "India", "Continuous 45A; 6-12S", 3380, 1),
    ("ESC", "T-Motor", "FLAME 60A HV", "ESC", "China", "60A cont.; 6-12S sinusoidal", 8600, 0),
    ("ESC", "T-Motor", "ALPHA 60A HV", "ESC", "China", "60A FOC precision", 6857, 0),
    ("ESC", "Hobbywing", "XRotor Pro 80A HV", "ESC", "China", "80A; 6-14S", 9274, 0),
    ("ESC", "APD", "120F3[X]", "ESC", "USA", "120A; 12S FOC", 17000, 0),
    ("ESC", "BotLab", "BotDrive 50A 4-in-1", "ESC", "India", "50A 8-bit 4-in-1 ESC", 4500, 1),
    ("ESC", "T Motor", "F55A PRO III 4-in-1", "ESC", "China", "55A 3-8S 4-in-1 ESC", 14700, 0),

    # Propeller
    ("Propeller", "T Motor", "18 inch CF Folding", "Propeller", "China", "18 inch CF folding", 4500, 0),
    ("Propeller", "T Motor", "17 inch CF Folding", "Propeller", "China", "17 inch CF folding", 6830, 0),
    ("Propeller", "Reflex drive", "17 inch CF Folding", "Propeller", "India", "RD-1760 17 inch folding prop", 2099, 1),
    ("Propeller", "T-Motor", "P21x6.3 CF Folding", "Propeller", "China", "21 inch carbon folding", 12000, 0),
    ("Propeller", "Mejzlik", "18x6.1 CF", "Propeller", "Czech Rep.", "18 inch balanced CF", 7372, 0),
    ("Propeller", "APC", "18x5.5 MR", "Propeller", "USA", "18 inch multirotor series", 1500, 0),
    ("Propeller", "T-Motor", "NS20*6.2 CF", "Propeller", "China", "20x6.2 Prop pair", 10695, 0),

    # Battery
    ("Battery", "M power", "34000mAh 4S", "Li-ion", "India", "34000mAh 4S high energy density", 19800, 1),
    ("Battery", "M power", "10200mAh 6S", "Li-ion", "India", "10200mAh 6S pack", 11682, 1),
    ("Battery", "M power", "18000mAh 6S", "Li-ion", "India", "18000mAh 6S pack", 25448, 1),
    ("Battery", "M power", "12000mAh 6S", "Li-ion", "India", "12000mAh 6S pack", 14400, 1),
    ("Battery", "M power", "40000mAh 4S", "Li-ion", "India", "40000mAh 4S pack", 18880, 1),
    ("Battery", "M power", "6000mAh 4S", "Li-ion", "India", "6000mAh 4S pack", 4400, 1),
    ("Battery", "GenX Power", "40000mAh 6S Solid State", "Solid State", "India", "40000mAh 6S 350 Wh/kg 7C", 39896, 1),
    ("Battery", "Revogreen", "6000mAh 6S", "Li-ion", "India", "6000mAh 6S pack", 7556, 1),
    ("Battery", "GenX", "16000mAh 6S", "Li-ion", "India", "21700 Li-ion cells 250-300 Wh/kg", 12197, 1),
    ("Battery", "GenX", "36000mAh 4S Solid State", "Solid State", "India", "36000mAh 4S solid state", 30129, 1),
    ("Battery", "Grepow / Tattu", "22000mAh 6S", "Li-ion", "China", "High-C industrial UAV pack", 17923, 0),

    # Camera / Payload
    ("Camera / Payload", "Wonwoo", "MM - G405 EO Zoom", "EO Camera", "South Korea", "1080p 40x opt 32x dig 355g", 46731, 0),
    ("Camera / Payload", "Wonwoo", "MC - G 305 EO Zoom", "EO Camera", "South Korea", "1080p 30x opt 278g", 41765, 0),
    ("Camera / Payload", "Wonwoo", "MC-G105 EO Zoom", "EO Camera", "South Korea", "1080p 10x opt 165g", 25852, 0),
    ("Camera / Payload", "Sony", "FCB-EV9520L", "EO Camera", "Japan", "Full HD 30x opt 239g", 58000, 0),
    ("Camera / Payload", "Sony", "FCB-ER8530 4K", "EO Camera", "Japan", "4K 20x opt 250g", 71000, 0),
    ("Camera / Payload", "Sony", "FCB-EW9500H 4K", "EO Camera", "Japan", "4K 30x opt STARVIS 439g", 82304, 0),
    ("Camera / Payload", "Tamron", "MP3010M-EV", "EO Camera", "Japan", "Full HD 10x opt 70g", 38000, 0),
    ("Camera / Payload", "MYK", "TMCM 640 LWIR", "IR Core", "South Korea", "640x512 8x dig 22g", 352760, 0),
    ("Camera / Payload", "Thermoteknix", "MicroCAM3", "IR Core", "UK", "640x480 8x dig 32g", 576320, 0),
    ("Camera / Payload", "FLIR", "Boson 55mm LWIR", "IR Core", "USA", "640x512 8x thermal", 608910, 0),
    ("Camera / Payload", "FLIR", "HADRON 640R", "EO/IR Core", "USA", "640x512 radiometric + EO", 401645, 0),
    ("Camera / Payload", "Lynred / Digital Core", "L6P Indian IR Core", "IR Core", "India", "640x480 2x/4x/8x 100g", 200000, 1),
    ("Camera / Payload", "Lynred / Digital Core", "L3P Indian IR Core", "IR Core", "India", "320x240 100g", 150000, 1),
    ("Camera / Payload", "Thermoeye", "TMC256B", "IR Core", "South Korea", "256x192 VOx microbolometer", 79520, 0),
    ("Camera / Payload", "Thermoeye", "TMC384B", "IR Core", "South Korea", "384x288 VOx", 168944, 0),
    ("Camera / Payload", "NextVision", "Nighthawk 2", "EO+IR Gimbal", "Israel", "1080p EO 20x + 640x480 IR 250g", 1912613, 0),
    ("Camera / Payload", "NextVision", "Dragon Eye 2", "EO+IR Gimbal", "Israel", "1080p EO 20x + 640x480 IR 125g", 839525, 0),
    ("Camera / Payload", "NextVision", "Raptor 360", "EO+IR Gimbal", "Israel", "1080p 20x + 1280x720 IR 640g", 2985701, 0),
    ("Camera / Payload", "Workswell", "WIRIS Pro", "EO+IR Gimbal", "Czech Rep.", "1080p 10x + 640x512 IR 430g", 1091998, 0),
    ("Camera / Payload", "Delopt", "EO Stabilize Gimbal", "EO+IR Gimbal", "India", "1080p 16x + 640x480 IR 800g", 800000, 1),
    ("Camera / Payload", "Vega Imaging", "Spectrum 300", "EO+IR Gimbal", "Turkey", "4K 40x + 640x512 IR 330g", 1296680, 0),
    ("Camera / Payload", "MotionMatics", "GazeX10", "EO Camera", "India", "1920x1080 10x opt", 198000, 1),
    ("Camera / Payload", "MotionMatics", "Nxy LWIR", "IR Core", "India", "640x512 8x 304g", 594000, 1),
    ("Camera / Payload", "MotionMatics", "ECLIPSE10 Gimbal", "EO+IR Gimbal", "India", "1080p 10x + 640x512 IR 450g", 747000, 1),
    ("Camera / Payload", "Gremsy", "VIO F1 FLIR 640R + LRF", "EO+IR+LRF Gimbal", "Vietnam", "4K 20x + 640x512 IR + Laser Rangefinder", 1356197, 0),
    ("Camera / Payload", "Indowings", "Rhythm3 EO+IR+LRF", "EO+IR+LRF Gimbal", "India", "4K 20x + 640x512 IR + LRF 815g", 950000, 1),
    ("Camera / Payload", "Skydroid", "C14 PRO EO+IR+LRF", "EO+IR+LRF Gimbal", "China", "4K 100x hybrid + 640x512 IR + LRF 210g", 125226, 0),
    ("Camera / Payload", "Gremsy", "LYNX NDAA Version", "EO+IR Gimbal", "Vietnam", "4K 10x + 640x512 190g NDAA", 700421, 0),

    # Power Module
    ("Power Module", "Mauch", "PL-050 / HS-050", "Current Sensor", "Germany", "50A continuous 2-6S / up to 14S Hall", 4000, 0),
    ("Power Module", "Mauch", "PL-100 / HS-100", "Current Sensor", "Germany", "100A continuous Hall sensor 17-22g", 4000, 0),
    ("Power Module", "Mauch", "PL-200 / HS-200", "Current Sensor", "Germany", "200A continuous high-current", 4600, 0),
    ("Power Module", "Holybro", "PM02 / PM02D", "Current Sensor", "China", "60A cont 90A burst 3-6S", 2400, 0),
    ("Power Module", "Holybro", "PM06 V2 PDB+PM", "Current Sensor", "China", "60A cont 5V/3A BEC 28g", 2917, 0),
    ("Power Module", "CUAV", "HV CAN PM", "Current Sensor", "China", "60-120A DroneCAN Hall sensor", 5728, 0),

    # Antenna
    ("Antenna", "L-com", "2.4/5.8GHz Omni/Patch", "RF Antenna", "USA", "2-8 dBi SMA/N-type MIMO", 11500, 0),
    ("Antenna", "MP Antenna", "Super-M Ultra", "RF Antenna", "USA", "Multi-polarised wideband BVLOS", 14500, 0),
    ("Antenna", "TrueRC", "Singularity / X-Air", "RF Antenna", "Canada", "Circular polarised video antenna", 5200, 0),
    ("Antenna", "Doodle Labs", "Mesh Rider Kit", "RF Antenna", "USA", "Sub-6 GHz MIMO mesh", 18500, 0),

    # GPS / GNSS
    ("GPS / GNSS", "3DR", "Multi-GNSS Receiver", "GNSS", "USA", "Multi-constellation GPS/GLO", 8053, 0),
    ("GPS / GNSS", "GEPRC", "Multi-GNSS Receiver", "GNSS", "China", "Basic GPS receiver", 1999, 0),
    ("GPS / GNSS", "Holybro", "DroneCAN M9N", "GNSS", "China", "u-blox M9N DroneCAN + compass", 10236, 0),
    ("GPS / GNSS", "CubePilot", "Here3+ / Here4", "RTK GNSS", "Australia", "RTK multi-band DroneCAN", 41000, 0),
    ("GPS / GNSS", "Septentrio", "mosaic-X5", "Resilient GNSS", "Belgium", "Multi-band RTK + AIM+ anti-jam", 75000, 0),
    ("GPS / GNSS", "u-blox", "ZED-F9P", "RTK GNSS", "Switzerland", "Dual-band RTK cm-level", 20000, 0),
    ("GPS / GNSS", "Orbit Nano", "NEO-F9P-15B RTK + NavIC", "RTK GNSS", "India", "Made in India RTK + NavIC smallest module", 19000, 1),

    # Anti-Jamming
    ("Anti-Jamming", "Xtrageon", "Mosaic G5 P8 Kit", "Anti-Jamming", "India", "GNSS anti-jam / anti-spoof front-end", 192500, 1),
    ("Anti-Jamming", "Globaz Tech", "Sunstone AJ Module", "Anti-Jamming", "India", "High-resilience anti-jamming", 360000, 1),
    ("Anti-Jamming", "Septentrio", "mosaic-X5 AIM+", "Anti-Jamming", "Belgium", "AIM+ interference mitigation", 85000, 0),
    ("Anti-Jamming", "NovAtel", "GAJT-710ML CRPA", "Anti-Jamming", "Canada", "Controlled Reception Pattern Antenna nulling", 450000, 0),

    # GPS-Denied / VIO
    ("GPS-Denied / VIO", "Vyorius", "VIO Vision Nav", "VIO Navigation", "India", "Camera + IMU fusion GPS-denied", 280000, 1),
    ("GPS-Denied / VIO", "Stride Dynamics", "VIO Sensor Suite", "VIO Navigation", "India", "Visual-inertial odometry module", 425000, 1),
    ("GPS-Denied / VIO", "Vecros", "Spatial AI Nav", "VIO Navigation", "India", "Obstacle avoidance + VIO", 350000, 1),
    ("GPS-Denied / VIO", "Unbird", "VIO Module", "VIO Navigation", "China", "Visual-inertial odometry", 63523, 0),

    # Flight Controller
    ("Flight Controller", "Pixhawk", "Pixhawk 2.4.8 Kit", "Autopilot", "Switzerland", "Standard PX4/ArduPilot FC", 16475, 0),
    ("Flight Controller", "CubePilot", "Orange Cube+ with Mini Carrier", "Autopilot", "Taiwan", "Triple redundant IMU Cube+", 43500, 0),
    ("Flight Controller", "Agam", "Agam Indian Autopilot", "Autopilot", "India", "Indigenous secure autopilot", 32000, 1),
    ("Flight Controller", "BotLab", "BotStack F405 FC", "Autopilot", "India", "Solderless design F405 FC", 7999, 1),
    ("Flight Controller", "Matek", "F405-HDTE", "Autopilot", "China", "F4 Flight controller 30.5mm", 8000, 0),
    ("Flight Controller", "CoPilot", "CoPilot Micro AI PX4", "Autopilot", "China", "AI based PX4 autopilot", 117020, 0),

    # Transmitter / RC / GCS
    ("Transmitter / RC", "Axle Drone", "Axle GCS 10km", "Radio Controller", "India", "Handheld GCS 10km HD video+telemetry", 128000, 1),
    ("Transmitter / RC", "Apex", "Apex GCS 20km", "Radio Controller", "India", "Long range 20km integrated GCS", 210000, 1),
    ("Transmitter / RC", "Bharat Component", "Bharat C2 10km", "Radio Controller", "India", "Handheld ground station 10km", 225000, 1),
    ("Transmitter / RC", "HereLink", "HereLink Standard", "Radio Controller", "China", "12 km HD video + telemetry", 200000, 0),
    ("Transmitter / RC", "HereLink", "HereLink Blue NDAA", "Radio Controller", "USA", "12 km NDAA compliant GCS", 385000, 0),
    ("Transmitter / RC", "Skydroid", "H12 Pro", "Radio Controller", "China", "5 km handheld controller", 30000, 0),
    ("Transmitter / RC", "Skydroid", "T12 Pro", "Radio Controller", "China", "5 km basic radio", 16000, 0),
    ("Transmitter / RC", "SIYI", "MK32 GCS", "Radio Controller", "China", "12 km 7-inch dual screen GCS", 60244, 0),
    ("Transmitter / RC", "Skydroid", "G30 GCS", "Radio Controller", "China", "15 km long-range radio", 94351, 0),
    ("Transmitter / RC", "Microhard", "pMDDL2450 OEM Radio", "Datalink", "Canada", "20 km 2.4GHz MIMO OEM datalink", 271545, 0),
    ("Transmitter / RC", "Silvus", "StreamCaster 4200 MANET", "Mesh Radio", "USA", "Military-grade anti-jam mesh radio", 850000, 0),

    # Battery Charger
    ("Battery Charger", "Indian Power Tech", "Vana Smart Balance Charger 1200W", "Charger", "India", "Dual channel 1200W indigenous charger", 24000, 1),
    ("Battery Charger", "SkyRC", "PC1080 Dual Channel", "Charger", "China", "1080W (540Wx2) 20A/ch 2-6S", 17054, 0),
    ("Battery Charger", "Tattu", "TA1000 G-Tech Dual", "Charger", "China", "1000W 25Ax2 1-7S LiPo/LiHV", 27000, 0),
    ("Battery Charger", "Tattu", "TA3200 HV Heavy Dual", "Charger", "China", "3200W 60A 6-14S", 71904, 0),
    ("Battery Charger", "ToolkitRC", "M6D 500W Dual", "Charger", "China", "500W 2x25A DC 1-6S", 7349, 0),
    ("Battery Charger", "ISDT", "CM1620 Industrial", "Charger", "China", "1100W 20A 2-16S", 15793, 0),
    ("Battery Charger", "HOTA", "D6 Ultra Dual", "Charger", "China", "AC 300W / DC 650W 15A", 11399, 0),

    # Rugged Laptop / Tablet
    ("Rugged Laptop / Tablet", "Getac", "S510 / B360 Rugged", "Rugged Laptop", "Taiwan", "MIL-STD-810H IP65 sunlight readable", 195000, 0),
    ("Rugged Laptop / Tablet", "Zebra", "L10ax Rugged Tablet", "Rugged Tablet", "USA", "MIL-STD-810H IP65", 95000, 0),
    ("Rugged Laptop / Tablet", "Panasonic", "Toughbook 40", "Rugged Laptop", "Japan", "Fully rugged hot-swap battery", 280000, 0),
    ("Rugged Laptop / Tablet", "Dell", "Latitude 7230 Rugged Extreme", "Rugged Tablet", "USA", "IP65 MIL-STD-810H", 210000, 0),

    # Generator
    ("Generator", "Prince Generator", "Portable 2.5kVA AC", "Generator", "India", "230V 50Hz field charger generator", 227000, 1),
    ("Generator", "Honda", "EU22i Inverter Genset", "Generator", "Japan", "2.2 kVA ultra-quiet clean sine", 141935, 0),
    ("Generator", "Yamaha", "EF2000iS Inverter", "Generator", "Japan", "2.0 kVA inverter genset", 132000, 0),
    ("Generator", "EcoFlow", "Delta Pro Hybrid Station", "Power Station", "China", "Battery + solar hybrid silent", 534000, 0),

    # Tethered System
    ("Tethered System", "Elistair", "Safe-T 2 Station", "Tethered Station", "France", "Continuous power + micro-tether 100m+", 1650000, 0),
    ("Tethered System", "Hoverfly", "LiveSky Military Tether", "Tethered Station", "USA", "Military tethered persistent hover", 2200000, 0),

    # Navigation Lights
    ("Navigation Lights", "Vector", "Anti-Collision RGB Strobe", "Nav Lights", "India", "High-intensity RGB strobe 3.3-12V", 3500, 1),
    ("Navigation Lights", "Lumenier", "Ultra-Bright Strobe LED", "Nav Lights", "USA", "High-visibility multi-colour", 4800, 0),
    ("Navigation Lights", "Matek", "WS2812 LED Strobe Board", "Nav Lights", "China", "2-6S programmable LED board", 1200, 0),
    ("Navigation Lights", "Firehouse Tech", "ARC 3-Mile Anti-Collision", "Nav Lights", "USA", "FAA-style strobe 3-mile visible", 6500, 0),

    # Miscellaneous / Accessories required by Army Tenders
    ("Accessories", "Vana", "10-inch Ordnance Release Mech", "Payload Release", "India", "Servo-driven bomb/grenade release kit", 25000, 1),
    ("Accessories", "Pelican / Vana", "Military Hard Case IP67", "Packaging", "India", "Custom foam-cut airtight transport case", 22000, 1),
    ("Accessories", "Vana", "Tool Set & Field Repair Kit", "Tools", "India", "Hex drivers, prop wrenches, spare connectors", 8500, 1),
    ("Accessories", "Vana", "Technical Manual & Flight Logbook", "Documentation", "India", "Army format bilingual logs & user manual", 3500, 1),
]

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        manufacturer TEXT NOT NULL,
        model TEXT NOT NULL,
        type TEXT,
        country TEXT NOT NULL,
        specs TEXT,
        price_inr REAL NOT NULL,
        is_mii INTEGER DEFAULT 0, -- 1 if Made in India / Class 1 MII friendly
        is_active INTEGER DEFAULT 1
    );
    """)

    cur.execute("DELETE FROM items;")
    cur.executemany("""
    INSERT INTO items (category, manufacturer, model, type, country, specs, price_inr, is_mii)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, ITEMS_DATA)

    conn.commit()
    conn.close()
    print(f"Catalog database created successfully at {DB_PATH} with {len(ITEMS_DATA)} parts.")

if __name__ == "__main__":
    init_db()
