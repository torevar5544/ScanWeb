
# 🔍 Website Security Scanner - Advanced

## Overview
This Python-based tool performs a **comprehensive security scan** for any website or IP address.  
It includes network diagnostics, subdomain discovery, DNS enumeration, SSL/TLS analysis, and safety verification.
# My Project

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey)

The tool provides a **graphical user interface (GUI)** with a **live log** and automatically generates **HTML and TXT reports**.

---

## Features

### Network Scans
- Full port scan (`nmap -p- -T4`)
- Detailed scan (`nmap -sS -sV -sC -O -T4`)
- Live **MTR trace** for 60 seconds

### WHOIS Lookup
- Domain registration info (Registrar, Owner, Dates, etc.)

### GeoIP Lookup
- Uses [iplocation.net](https://www.iplocation.net) for country, city, and ISP info

### Subdomain Enumeration
- Checks common subdomains like `www`, `mail`, `ftp`, `blog`, `dev`, `api`, `shop`, `test`, `portal`, `webmail`

### DNS Records
- Retrieves A, AAAA, MX, NS, and TXT records

### Safety & Reputation
- Checks **ScamAdviser** website status
- Checks **Cloudflare Radar** scan availability

### SSL/TLS Analysis
- Validates certificate
- Extracts CN and SANs
- Checks expiration date
- Lists supported TLS protocols and cipher suites
- Detects known SSL vulnerabilities

### Reports
- HTML and TXT files saved in `reports/`
- Easy access to ScamAdviser and Cloudflare Radar links

---

## Installation

### Linux
```bash
git clone https://github.com/torevar5544/ScanWeb.git
cd ScanWeb

```

### Windows
```bat
git clone https://github.com/torevar5544/ScanWeb.git
cd ScanWeb

```

The setup script will:
1. Install Python (if missing)
2. Create a virtual environment
3. Install Python dependencies
4. Install system tools (Nmap, MTR, OpenSSL / WinMTR)
5. Launch the scanner after setup

---

## Usage

1. Run the scanner (if not automatically launched):
```bash
# Linux
source venv/bin/activate
python ScanWeb.py

# Windows
call venv\Scripts\activate.bat
python ScanWeb.py
```

2. Enter a **domain or IP** in the GUI input box.

3. Click **Start Scan**.

4. Monitor the **live log** for progress.

5. After completion:
   - Open **HTML report** in browser
   - Access **TXT report**
   - Check links for **ScamAdviser** and **Cloudflare Radar**

---

## Requirements

### Python Packages
```text
requests>=2.31.0
python-whois>=0.8.0
beautifulsoup4>=4.12.2
dnspython>=2.4.2
```

### System Tools
- Linux: `nmap`, `mtr`, `openssl`
- Windows: `Nmap`, `WinMTR` (via winget)

---

## Security & Legal
This tool is intended for **educational and authorized security testing only**.  

---

## Notes
- Requires **Python 3.8+**
- Reports are stored in `reports/` with timestamped filenames
- MTR runs for 60 seconds to trace the route
- The scanner generates the report **after all scans complete**, including MTR
