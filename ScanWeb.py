import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading, subprocess, socket, json, os, datetime, re
import dns.resolver

try:
    import whois
except:
    whois = None

APP_TITLE = "Website Security Scanner - Advanced"
REPORT_DIR = "reports"
os.makedirs(REPORT_DIR, exist_ok=True)

SUBDOMAINS = ["www","mail","ftp","blog","dev","api","shop","test","portal","webmail"]

def sanitize_target(raw: str) -> str:
    raw = raw.strip()
    raw = re.sub(r"^\s*https?://", "", raw, flags=re.I)
    raw = raw.split("/")[0].split("#")[0].split("?")[0]
    return raw

def timestamp(): 
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def log(msg): 
    LOG.insert(tk.END, msg+"\n")
    LOG.see(tk.END)
    ROOT.update_idletasks()

def save_reports(target, data):
    ts = timestamp()
    safe_target = re.sub(r"[^A-Za-z0-9_.-]", "_", target)
    txt_path = os.path.join(REPORT_DIR, f"report_{safe_target}_{ts}.txt")
    html_path = os.path.join(REPORT_DIR, f"report_{safe_target}_{ts}.html")

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"Scan Report for {target}\nGenerated: {datetime.datetime.now()}\n\n")
        for section, content in data.items():
            f.write(f"== {section} ==\n")
            if isinstance(content, (dict, list)): 
                f.write(json.dumps(content, indent=2, ensure_ascii=False))
            else: 
                f.write(str(content))
            f.write("\n\n")
    
    def pre(s): 
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    
    html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Scan Report - {target}</title>
<style>body{{font-family:Arial,sans-serif;background:#f8f9fa;color:#222;padding:20px}}pre{{background:#222;color:#0f0;padding:10px;border-radius:8px;overflow-x:auto}}h2{{color:#333;margin-top:25px}}</style></head><body>
<h1>Scan Report for {pre(target)}</h1><p>Generated: {datetime.datetime.now()}</p>"""
    
    for section, content in data.items():
        html += f"<h2>{pre(section)}</h2><pre>{pre(json.dumps(content, indent=2) if isinstance(content, (dict, list)) else str(content))}</pre>"
    
    html += "</body></html>"
    
    with open(html_path, "w", encoding="utf-8") as f: 
        f.write(html)
    
    return txt_path, html_path

def run_mtr(ip):
    log(f"[*] Starting MTR to {ip} for 10s...")
    try:
        proc = subprocess.Popen(["mtr", "-r", "-c", "10", ip], 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out, err = proc.communicate(timeout=15)
        log(f"[✓] MTR finished:\n{out}")
        return out
    except subprocess.TimeoutExpired:
        proc.kill()
        log("[!] MTR terminated after timeout.")
        return "MTR timeout"
    except Exception as e: 
        log(f"[!] MTR error: {e}")
        return f"MTR error: {e}"

def get_iplocation(ip):
    log("[*] Fetching IP location...")
    try:
        # استخدام خدمة ipapi.co للحصول على معلومات الموقع
        import requests
        response = requests.get(f"http://ipapi.co/{ip}/json/", timeout=10)
        data = response.json()
        
        # استخراج المعلومات المهمة فقط
        geo_info = {
            "IP": data.get("ip", "N/A"),
            "City": data.get("city", "N/A"),
            "Region": data.get("region", "N/A"),
            "Country": data.get("country_name", "N/A"),
            "ISP": data.get("org", "N/A"),
            "ASN": data.get("asn", "N/A")
        }
        
        log(f"[✓] IP location fetched: {geo_info['City']}, {geo_info['Country']}")
        return geo_info
    except Exception as e:
        log(f"[!] IP location error: {e}")
        return {"error": str(e)}

def check_subdomains(domain):
    log("[*] Starting subdomain enumeration...")
    found = {}
    for sub in SUBDOMAINS:
        full = sub + "." + domain
        try: 
            ip = socket.gethostbyname(full)
            found[full] = ip
            log(f"[+] Found: {full} -> {ip}")
        except: 
            pass
    
    if not found: 
        log("[i] No common subdomains found.")
    
    return found

def get_dns_records(domain):
    log("[*] Fetching DNS records (A, AAAA, MX, NS, TXT)...")
    records = {}
    types = ["A", "AAAA", "MX", "NS", "TXT"]
    
    for t in types:
        try:
            answers = dns.resolver.resolve(domain, t)
            records[t] = [str(r) for r in answers]
            log(f"[+] {t} records: {records[t]}")
        except Exception as e:
            records[t] = f"Error: {e}"
            log(f"[!] {t} lookup error: {e}")
    
    return records

def do_scan():
    # تعطيل زر البدء أثناء المسح
    SCAN_BUTTON.config(state=tk.DISABLED)
    
    target_raw = ENTRY.get().strip()
    if not target_raw: 
        messagebox.showerror("Error", "Please enter a domain or IP.")
        SCAN_BUTTON.config(state=tk.NORMAL)
        return
    
    LOG.delete("1.0", tk.END)
    target = sanitize_target(target_raw)
    log(f"[+] Target: {target}")

    try: 
        ip = socket.gethostbyname(target)
        log(f"[+] Resolved IP: {ip}")
    except Exception as e: 
        log(f"[!] Failed to resolve: {e}")
        SCAN_BUTTON.config(state=tk.NORMAL)
        return

    results = {"Resolved IP": ip, "Target": target}

    # فحص MTR
    log("[*] Running MTR...")
    results["MTR Results"] = run_mtr(ip)

    # فحص Nmap للمنافذ الكاملة
    log("[*] Running Nmap full port scan (-p- -T4)...")
    try: 
        nmap_all = subprocess.check_output(["nmap", "-p-", "-T4", ip], 
                                         stderr=subprocess.STDOUT, text=True, timeout=300)
        results["Nmap All Ports"] = nmap_all
        log("[✓] Nmap full ports done.")
    except subprocess.TimeoutExpired:
        results["Nmap All Ports"] = "Scan timed out after 5 minutes"
        log("[!] Nmap full port scan timed out.")
    except Exception as e: 
        results["Nmap All Ports"] = f"Nmap error: {e}"
        log(f"[!] Nmap error: {e}")

    # فحص Nmap المفصل
    log("[*] Running Nmap detailed scan (-sS -sV -sC -O -T4)...")
    try: 
        nmap_det = subprocess.check_output(["nmap", "-sS", "-sV", "-sC", "-O", "-T4", ip], 
                                         stderr=subprocess.STDOUT, text=True, timeout=600)
        results["Nmap Detailed"] = nmap_det
        log("[✓] Nmap detailed done.")
    except subprocess.TimeoutExpired:
        results["Nmap Detailed"] = "Detailed scan timed out after 10 minutes"
        log("[!] Nmap detailed scan timed out.")
    except Exception as e: 
        results["Nmap Detailed"] = f"Nmap detailed error: {e}"
        log(f"[!] Nmap detailed error: {e}")

    # فحص WHOIS
    log("[*] Running WHOIS...")
    if whois is None: 
        results["WHOIS"] = "python-whois not installed."
        log("[!] WHOIS module not available.")
    else:
        try: 
            w = whois.whois(target)
            results["WHOIS"] = json.dumps({k: str(v) for k, v in dict(w).items()}, indent=2)
            log("[✓] WHOIS done.")
        except Exception as e: 
            results["WHOIS"] = f"WHOIS error: {e}"
            log(f"[!] WHOIS error: {e}")

    # معلومات الموقع الجغرافي
    results["GeoIP"] = get_iplocation(ip)

    # البحث عن النطاقات الفرعية
    results["Subdomains"] = check_subdomains(target)

    # سجلات DNS
    results["DNS Records"] = get_dns_records(target)

    # حفظ التقارير
    log("[*] Saving reports...")
    txt_path, html_path = save_reports(target, results)
    log(f"[✓] TXT: {os.path.abspath(txt_path)}")
    log(f"[✓] HTML: {os.path.abspath(html_path)}")
    
    # إعادة تمكين زر البدء
    SCAN_BUTTON.config(state=tk.NORMAL)
    
    messagebox.showinfo("Scan completed", 
                       f"Scan completed successfully!\n\nReports saved:\n{os.path.abspath(txt_path)}\n{os.path.abspath(html_path)}")

def start_scan_thread(): 
    threading.Thread(target=do_scan, daemon=True).start()

# واجهة المستخدم
ROOT = tk.Tk()
ROOT.title(APP_TITLE)
ROOT.geometry("940x750")

# إطار العلوي
top = tk.Frame(ROOT)
top.pack(pady=10, fill=tk.X)

tk.Label(top, text="Enter Domain or IP:", font=("Arial", 11)).pack(side=tk.LEFT, padx=8)

ENTRY = tk.Entry(top, width=50, font=("Arial", 11))
ENTRY.pack(side=tk.LEFT, padx=6)

SCAN_BUTTON = tk.Button(top, text="Start Scan", bg="green", fg="white", 
                       font=("Arial", 11), command=start_scan_thread)
SCAN_BUTTON.pack(side=tk.LEFT, padx=6)

# منطقة السجلات
LOG = scrolledtext.ScrolledText(ROOT, width=120, height=35, 
                               bg="#0b0f14", fg="#9ae6a0", 
                               insertbackground="#9ae6a0", 
                               font=("Consolas", 10))
LOG.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

ROOT.mainloop()