import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import os
import sys
import platform
import ctypes
import datetime
import json
import shutil
import secrets
import string
import socket
import ssl
import time
import io
import hmac
import html
import ipaddress
import tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

# QR Kod kütüphanesi kontrolü
try:
    import qrcode
    QR_KUTUPHANE_VAR = True
except ImportError:
    QR_KUTUPHANE_VAR = False

ISLETIM_SISTEMI = platform.system()
AYAR_DOSYASI = os.path.join(os.path.expanduser("~"), ".comar_config.json")
SUNUCU_PORT = 8765
MAX_PAYLOAD_SIZE = 64 * 1024  # 64 KB DoS / Payload Sınırı
OTURUM_ZAMAN_ASIMI = 300      # 5 dakika hareketsizlik durumunda oturum sonlandırma

def yerel_ip_bul():
    """İnternet erişimi gerektirmeden etkin yerel ağ arayüzünün IP adresini bulur."""
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # TEST-NET adresine yönlendirme tablosu üzerinden bakılır; paket gönderilmez.
        s.connect(("192.0.2.1", 9))
        ip = s.getsockname()[0]
        return ip if ip and not ip.startswith("127.") else "127.0.0.1"
    except Exception:
        return "127.0.0.1"
    finally:
        if s:
            s.close()

CEVIRILER = {
    "TR": {
        "baslik": "🐕 Çomar - Güvenli Sistem Bakım Aracı",
        "alt_baslik": f"Sistem: {ISLETIM_SISTEMI} | Wi-Fi Uzaktan Kontrol Güvenli Mod",
        "islemler": "Bakım ve Onarım Görevleri",
        "tumunu_sec": "Tümünü Seç",
        "temizle": "Temizle",
        "kuru_calistir": "Kuru çalıştırma (Simülasyon)",
        "oto_rapor": "Raporu otomatik aç",
        "tema_degistir": "🌓 Tema",
        "dil_degistir": "🌐 EN",
        "sunucu_ac": "🌐 Web Kontrolü Aç",
        "sunucu_kapat": "🛑 Web Kontrolü Kapat",
        "baslat": "🚀 Çomar'ı Başlat",
        "hazir": "Hazır. Görev bekliyor...",
        "rapor_ac": "📄 Raporu Aç",
        "uyari_secim": "Lütfen en az bir bakım görevi seçin.",
        "yetki_baslik": "Yönetici / Root İzni",
        "yetki_mesaj_win": "Tam temizlik için Yönetici izni gerekiyor.\nYönetici olarak yeniden başlatılsın mı?",
        "yetki_mesaj_unix": "Root (sudo) yetkisi olmadan çalışıyorsunuz. Devam edilsin mi?",
        "cikis_onay": "Çomar şu an çalışıyor. Yine de çıkılsın mı?",
        "rapor_yok": "Henüz bir bakım raporu oluşturulmadı.",
        "isleniyor": "Çalışıyor",
        "tamamlandi": "Tüm görevler tamamlandı! Rapor masaüstündeki arşive kaydedildi.",
        "gorevler": {
            "geri_yukleme": "Sistem geri yükleme / Anlık görüntü",
            "gecici_temizlik": "Geçici dosya (Temp/Cache) temizliği",
            "tarayici_temizlik": "Tarayıcı önbellek temizliği",
            "dns_temizlik": "DNS önbelleği temizliği",
            "paket_guncelleme": "Uygulama ve paket güncellemeleri",
            "sistem_onarim": "Sistem dosya bütünlüğü onarımı",
            "sistem_bilgi": "Sistem, RAM ve disk kapasite bilgisi",
            "baslangic": "Başlangıç uygulamaları / Servisler",
            "olay_gunlukleri": "Kritik sistem hata günlükleri",
            "disk_saglik": "Disk sağlık (S.M.A.R.T.) durumu"
        }
    },
    "EN": {
        "baslik": "🐕 Comar - Secure System Maintenance Tool",
        "alt_baslik": f"OS: {ISLETIM_SISTEMI} | Wi-Fi Remote Control Secure Mode",
        "islemler": "Maintenance & Repair Tasks",
        "tumunu_sec": "Select All",
        "temizle": "Clear",
        "kuru_calistir": "Dry Run (Simulation)",
        "oto_rapor": "Auto-open report",
        "tema_degistir": "🌓 Theme",
        "dil_degistir": "🌐 TR",
        "sunucu_ac": "🌐 Start Web Control",
        "sunucu_kapat": "🛑 Stop Web Control",
        "baslat": "🚀 Unleash Comar",
        "hazir": "Ready. Waiting for tasks...",
        "rapor_ac": "📄 Open Report",
        "uyari_secim": "Please select at least one task.",
        "yetki_baslik": "Administrator / Root Privilege",
        "yetki_mesaj_win": "Comar needs Administrator privileges.\nRestart as Administrator?",
        "yetki_mesaj_unix": "Running without root (sudo). Continue anyway?",
        "cikis_onay": "Comar is working. Exit anyway?",
        "rapor_yok": "No maintenance report generated yet.",
        "isleniyor": "Processing",
        "tamamlandi": "All tasks completed! Report saved to Desktop archive.",
        "gorevler": {
            "geri_yukleme": "System restore point / Snapshot",
            "gecici_temizlik": "Temporary files (Temp/Cache) cleanup",
            "tarayici_temizlik": "Browser cache cleanup",
            "dns_temizlik": "Flush DNS cache",
            "paket_guncelleme": "Application & package updates",
            "sistem_onarim": "System file integrity repair",
            "sistem_bilgi": "System, RAM & disk usage info",
            "baslangic": "Startup programs / Services",
            "olay_gunlukleri": "Critical system error logs",
            "disk_saglik": "Disk health (S.M.A.R.T.) status"
        }
    }
}

TEMALAR = {
    "light": {"bg": "#f0f2f5", "fg": "#202124", "log_bg": "#ffffff", "log_fg": "#202124", "accent": "#1a73e8", "sub_fg": "#5f6368"},
    "dark": {"bg": "#18191a", "fg": "#e4e6eb", "log_bg": "#121212", "log_fg": "#00ff88", "accent": "#4dabf7", "sub_fg": "#b0b3b8"}
}

def yonetici_mi():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0 if ISLETIM_SISTEMI == "Windows" else os.geteuid() == 0
    except Exception:
        return False

def yonetici_olarak_baslat():
    if ISLETIM_SISTEMI == "Windows":
        try:
            script = os.path.abspath(sys.argv[0])
            params = " ".join([f'"{a}"' for a in sys.argv[1:]])
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)
        except Exception:
            pass

class ComarWebHandler(BaseHTTPRequestHandler):
    app_ref = None

    def _cors_headers(self):
        # Panel aynı sunucudan sunulur; gereksiz çapraz-kaynak erişimi açılmaz.
        self.send_header("Vary", "Origin")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Referrer-Policy", "no-referrer")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors_headers()
        self.end_headers()

    def _yanit_gonder(self, kod, veri):
        govde = json.dumps(veri, ensure_ascii=False).encode("utf-8")
        self.send_response(kod)
        self._cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(govde)))
        self.end_headers()
        self.wfile.write(govde)

    def _istemci_yerel_mi(self):
        try:
            adres = ipaddress.ip_address(self.client_address[0])
            return adres.is_private or adres.is_loopback or adres.is_link_local
        except ValueError:
            return False

    def _oturum_dogrula(self, app):
        if not self._istemci_yerel_mi():
            self._yanit_gonder(403, {"durum": "YASAKLI", "mesaj": "Yalnızca yerel ağdan erişime izin verilir."})
            return False
        with app.guvenlik_kilidi:
            if not app.sunucu_aktif or not app.guvenlik_kodu:
                self._yanit_gonder(401, {"durum": "KAPALI", "mesaj": "Web kontrol sunucusu kapalı."})
                return False
            if time.time() - app.son_aktivite_zamani > OTURUM_ZAMAN_ASIMI:
                app.root.after(0, app.sunucu_kapat_otomatik)
                self._yanit_gonder(401, {"durum": "ZAMAN_ASIMI", "mesaj": "Oturum zaman aşımına uğradı. Bilgisayardan yeniden bağlanın."})
                return False
            if app.hatali_giris >= 5:
                self._yanit_gonder(429, {"durum": "KILITLI", "mesaj": "Çok sayıda hatalı deneme. Web kontrolünü kapatıp yeniden açın."})
                return False
            token = self.headers.get("X-Comar-Token", "")
            if not hmac.compare_digest(token, app.guvenlik_kodu):
                app.hatali_giris += 1
                self._yanit_gonder(401, {"durum": "YETKISIZ", "mesaj": "Geçersiz güvenlik kodu."})
                return False
            app.son_aktivite_zamani = time.time()
            return True

    def do_GET(self):
        app = self.app_ref
        parsed = urlparse(self.path)

        # Panelin kendisi de yalnızca yerel ağdan görüntülenebilir.
        if parsed.path == "/" and not self._istemci_yerel_mi():
            return self._yanit_gonder(403, {"durum": "YASAKLI", "mesaj": "Yalnızca yerel ağdan erişime izin verilir."})

        # Zenginleştirilmiş Mini HTML/CSS/JS Arayüzü (Ana Dizin /)
        if parsed.path == "/":
            self.send_response(200)
            self._cors_headers()
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            html_icerik = r"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#000000">
<title>Çomar | Mobil Kontrol</title>
<style>
:root{--black:#000000;--cream:#F7F7F7;--orange:#FFB22C;--brown:#854836;--surface:#17100d;--surface2:#211610;--muted:#c4b5ad;--line:rgba(247,247,247,.13);--danger:#ff8c78;--ok:#FFB22C}
*{box-sizing:border-box}
html{color-scheme:dark}
body{margin:0;min-height:100vh;background:var(--black);color:var(--cream);font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;padding:env(safe-area-inset-top) 14px env(safe-area-inset-bottom);line-height:1.5}
button,input{font:inherit}
button{touch-action:manipulation}
.shell{width:min(100%,680px);margin:0 auto;padding:18px 0 32px}
.topbar{display:flex;align-items:center;gap:12px;padding:8px 2px 20px}
.logo{width:48px;height:48px;border-radius:16px;display:grid;place-items:center;background:var(--orange);color:var(--black);font-size:27px;box-shadow:0 7px 24px rgba(255,178,44,.17)}
.brand{font-size:1.12rem;font-weight:900;letter-spacing:.04em}
.subtitle{color:var(--muted);font-size:.82rem}
.card{background:linear-gradient(145deg,var(--surface2),var(--surface));border:1px solid var(--line);border-radius:22px;padding:clamp(18px,5vw,28px);box-shadow:0 18px 50px rgba(0,0,0,.32)}
h1{font-size:clamp(1.55rem,6vw,2.1rem);line-height:1.15;margin:0 0 8px}
h2{font-size:1.12rem;margin:0 0 14px}
p{color:var(--muted);margin:0 0 18px}
.kicker{display:inline-flex;align-items:center;gap:7px;color:var(--orange);font-size:.76rem;font-weight:850;letter-spacing:.12em;text-transform:uppercase;margin-bottom:10px}
.auth-copy{font-size:.93rem}
.token-wrap{display:grid;grid-template-columns:1fr;gap:10px;margin-top:20px}
input[type=text]{width:100%;min-height:58px;border:1px solid rgba(255,178,44,.45);border-radius:14px;background:#090706;color:var(--cream);padding:14px 16px;text-align:center;font-size:1.35rem;font-weight:850;letter-spacing:.3em;text-transform:uppercase;outline:none}
input:focus{border-color:var(--orange);box-shadow:0 0 0 3px rgba(255,178,44,.15)}
.btn{width:100%;min-height:52px;border:0;border-radius:14px;padding:13px 18px;background:var(--orange);color:var(--black);font-weight:900;font-size:1rem;cursor:pointer}
.btn:active{transform:scale(.99)}
.btn:disabled{opacity:.55;cursor:wait}
.btn.secondary{background:var(--brown);color:var(--cream)}
.feedback{min-height:24px;margin-top:12px;font-size:.9rem;color:var(--orange)}
.feedback.error{color:var(--danger)}
#control-panel{display:none}
.connected{display:flex;align-items:center;gap:9px;padding:13px 14px;border-radius:13px;background:rgba(255,178,44,.10);border:1px solid rgba(255,178,44,.25);color:var(--cream);font-size:.9rem;margin:16px 0 22px}
.dot{width:9px;height:9px;border-radius:50%;background:var(--orange);box-shadow:0 0 0 4px rgba(255,178,44,.12);flex:none}
.task-list{display:grid;gap:9px}
.task-item{display:flex;align-items:center;gap:12px;min-height:54px;padding:12px 13px;border:1px solid var(--line);border-radius:13px;background:rgba(247,247,247,.035);font-size:.92rem;cursor:pointer}
.task-item:has(input:checked){border-color:rgba(255,178,44,.55);background:rgba(255,178,44,.08)}
.task-item input{width:21px;height:21px;flex:none;accent-color:var(--orange)}
.actions{margin-top:18px}
.progress-container{display:none;height:9px;background:#34251e;border-radius:99px;overflow:hidden;margin:18px 0 10px}
.progress-bar{width:0;height:100%;background:var(--orange);transition:width .3s}
.status-msg{font-size:.9rem;color:var(--orange);margin:10px 0}
.log-box{display:none;white-space:pre-wrap;overflow:auto;max-height:260px;background:#080605;border:1px solid var(--line);border-radius:13px;padding:14px;color:#F7F7F7;font: .8rem/1.55 ui-monospace,SFMono-Regular,Consolas,monospace}
.footnote{text-align:center;color:#8f8179;font-size:.76rem;margin:17px 8px 0}
@media(min-width:560px){body{padding-left:22px;padding-right:22px}.token-wrap{grid-template-columns:1fr 145px}.token-wrap .btn{height:58px}.task-list{grid-template-columns:1fr 1fr}.task-item{font-size:.86rem}}
</style>
</head>
<body>
<div class="shell">
  <header class="topbar"><div class="logo">🐕</div><div><div class="brand">ÇOMAR</div><div class="subtitle">Güvenli mobil bakım paneli</div></div></header>
  <main>
    <section class="card" id="auth-panel">
      <span class="kicker">● Yerel ağ bağlantısı</span>
      <h1>Bilgisayarını telefonundan yönet.</h1>
      <p class="auth-copy">Bilgisayardaki Çomar uygulamasında gösterilen 6 karakterli güvenlik kodunu girerek devam et.</p>
      <form id="authForm" class="token-wrap">
        <input type="text" id="tokenInput" maxlength="6" minlength="6" placeholder="A1B2C3" autocomplete="one-time-code" autocapitalize="characters" spellcheck="false" aria-label="6 karakterli güvenlik kodu" required>
        <button class="btn" id="loginBtn" type="submit">Bağlan</button>
      </form>
      <div class="feedback" id="authFeedback" role="status" aria-live="polite"></div>
    </section>

    <section class="card" id="control-panel">
      <span class="kicker">● Bağlantı kuruldu</span>
      <h1>Uzaktan bakım</h1>
      <div class="connected"><span class="dot"></span><span id="systemInfo">Çomar'a bağlı</span></div>
      <h2>Bakım görevlerini seç</h2>
      <div class="task-list" id="taskList">
        <label class="task-item"><input type="checkbox" value="geri_yukleme"> Sistem geri yükleme / anlık görüntü</label>
        <label class="task-item"><input type="checkbox" value="gecici_temizlik" checked> Geçici dosya temizliği</label>
        <label class="task-item"><input type="checkbox" value="tarayici_temizlik" checked> Tarayıcı önbelleği</label>
        <label class="task-item"><input type="checkbox" value="dns_temizlik" checked> DNS önbelleği</label>
        <label class="task-item"><input type="checkbox" value="paket_guncelleme"> Paket güncellemeleri</label>
        <label class="task-item"><input type="checkbox" value="sistem_onarim"> Sistem dosyası onarımı</label>
        <label class="task-item"><input type="checkbox" value="sistem_bilgi" checked> Sistem, RAM ve disk bilgisi</label>
        <label class="task-item"><input type="checkbox" value="baslangic"> Başlangıç uygulamaları</label>
        <label class="task-item"><input type="checkbox" value="olay_gunlukleri"> Kritik hata günlükleri</label>
        <label class="task-item"><input type="checkbox" value="disk_saglik" checked> Disk sağlık durumu (S.M.A.R.T.)</label>
      </div>
      <div class="progress-container" id="progressBarContainer"><div class="progress-bar" id="progressBar"></div></div>
      <div class="status-msg" id="statusMsg" role="status" aria-live="polite"></div>
      <div class="actions"><button class="btn" id="runBtn" type="button">🚀 Bakımı başlat</button></div>
      <pre class="log-box" id="logBox">İşlem günlükleri burada görüntülenecek.</pre>
    </section>
  </main>
  <div class="footnote">Telefon ve bilgisayar aynı Wi-Fi ağına bağlı olmalıdır.</div>
</div>
<script>
let token = "";
let pollInterval = null;
const $ = id => document.getElementById(id);
function feedback(message, error=false){ $("authFeedback").textContent=message; $("authFeedback").classList.toggle("error",error); }

$("tokenInput").addEventListener("input", e => {
  e.target.value=e.target.value.toUpperCase().replace(/[^A-Z0-9]/g,"").slice(0,6);
});
$("authForm").addEventListener("submit", async e => {
  e.preventDefault();
  const candidate=$("tokenInput").value.trim().toUpperCase();
  if(!/^[A-Z0-9]{6}$/.test(candidate)){feedback("Lütfen 6 karakterli güvenlik kodunu gir.",true);return;}
  $("loginBtn").disabled=true; feedback("Güvenlik kodu doğrulanıyor…");
  try{
    const res=await fetch("/status",{method:"GET",cache:"no-store",headers:{"X-Comar-Token":candidate}});
    const data=await res.json();
    if(!res.ok){feedback(data.mesaj||"Kod doğrulanamadı.",true);return;}
    token=candidate;
    $("auth-panel").style.display="none";
    $("control-panel").style.display="block";
    $("systemInfo").textContent="Bağlı bilgisayar: "+(data.sistem||"Bilinmiyor");
    $("statusMsg").textContent=data.son_durum||"Bağlantı hazır. Bakım görevlerini seçebilirsin.";
    $("tokenInput").value="";
  }catch(err){feedback("Sunucuya ulaşılamadı. Wi-Fi bağlantısını ve bilgisayarın açık olduğunu kontrol et.",true);}
  finally{$("loginBtn").disabled=false;}
});

$("runBtn").addEventListener("click", async () => {
  const gorevler=Array.from(document.querySelectorAll("#taskList input:checked")).map(x=>x.value);
  if(!gorevler.length){$("statusMsg").textContent="Önce en az bir görev seç.";return;}
  if(!confirm("Seçilen bakım görevleri bilgisayarda çalıştırılacak. Devam edilsin mi?"))return;
  $("runBtn").disabled=true;$("progressBarContainer").style.display="block";$("logBox").style.display="block";
  $("progressBar").style.width="12%";$("statusMsg").textContent="Bakım komutu gönderiliyor…";
  $("logBox").textContent="🐕 Çomar'a bakım komutu gönderildi…\n";
  try{
    const res=await fetch("/run",{method:"POST",cache:"no-store",headers:{"Content-Type":"application/json","X-Comar-Token":token},body:JSON.stringify({gorevler})});
    const data=await res.json();
    if(!res.ok){$("statusMsg").textContent=data.mesaj||"İşlem başlatılamadı.";$("runBtn").disabled=false;return;}
    $("progressBar").style.width="30%";$("statusMsg").textContent=data.mesaj||"İşlemler yürütülüyor…";
    if(pollInterval)clearInterval(pollInterval);
    pollInterval=setInterval(durumSorgula,1500);
    durumSorgula();
  }catch(err){$("statusMsg").textContent="Sunucuyla iletişim kesildi.";$("runBtn").disabled=false;}
});

async function durumSorgula(){
  try{
    const res=await fetch("/status",{cache:"no-store",headers:{"X-Comar-Token":token}});
    const data=await res.json();
    if(!res.ok){clearInterval(pollInterval);$("statusMsg").textContent=data.mesaj||"Oturum sona erdi.";$("runBtn").disabled=true;return;}
    $("statusMsg").textContent="Durum: "+(data.son_durum||"Kontrol ediliyor");
    if(data.son_log){$("logBox").textContent=data.son_log;$("logBox").scrollTop=$("logBox").scrollHeight;}
    if(!data.calisiyor){
      clearInterval(pollInterval);pollInterval=null;$("progressBar").style.width="100%";
      $("statusMsg").textContent="✓ İşlem tamamlandı. Ayrıntılar için bilgisayardaki raporu kontrol et.";
      $("runBtn").disabled=false;
    }else{$("progressBar").style.width="65%";}
  }catch(err){$("statusMsg").textContent="Bağlantı geçici olarak kesildi; yeniden deneniyor…";}
}
</script>
</body>
</html>"""
            self.wfile.write(html_icerik.encode("utf-8"))
            return

        if not self._oturum_dogrula(app):
            return
        if parsed.path == "/status":
            # Son log verisini de arayüze anlık olarak gönderiyoruz
            with app.durum_kilidi:
                log_icerik = "\n".join(app.log_satirlari[-250:])
                son_durum = app.son_durum_metni
            return self._yanit_gonder(200, {
                "durum": "OK",
                "sistem": ISLETIM_SISTEMI,
                "calisiyor": app.calisiyor,
                "son_durum": son_durum,
                "son_log": log_icerik
            })
        return self._yanit_gonder(404, {"durum": "HATA", "mesaj": "Bilinmeyen uç nokta"})

    def do_POST(self):
        app = self.app_ref
        if not self._oturum_dogrula(app):
            return
        parsed = urlparse(self.path)
        if parsed.path == "/run":
            if app.calisiyor:
                return self._yanit_gonder(409, {"durum": "MESGUL", "mesaj": "Çomar şu an zaten bir görev yürütüyor."})

            try:
                uzunluk = int(self.headers.get("Content-Length", "0"))
            except (TypeError, ValueError):
                return self._yanit_gonder(400, {"durum": "HATA", "mesaj": "Geçersiz istek boyutu."})
            if uzunluk <= 0 or uzunluk > MAX_PAYLOAD_SIZE:
                return self._yanit_gonder(413, {"durum": "HATA", "mesaj": "İstek boyutu geçersiz veya çok büyük."})

            try:
                govde = self.rfile.read(uzunluk).decode("utf-8")
                veri = json.loads(govde)
                if not isinstance(veri, dict) or not isinstance(veri.get("gorevler"), list):
                    return self._yanit_gonder(400, {"durum": "HATA", "mesaj": "Görev listesi geçersiz."})
                secilenler = veri.get("gorevler", [])
                gecerli_gorevler = list(dict.fromkeys(g for g in secilenler if isinstance(g, str) and g in app.GOREV_ANAHTARLARI))
                if not gecerli_gorevler:
                    return self._yanit_gonder(400, {"durum": "HATA", "mesaj": "Geçerli görev seçilmedi."})

                istemci_ip = self.client_address[0]
                app.yaz(f"\n🌐 [WI-FI KOMUT - {istemci_ip}] Tetiklenen görevler: {', '.join(gecerli_gorevler)}")
                app.root.after(0, lambda: app.uzaktan_baslat(gecerli_gorevler))
                return self._yanit_gonder(200, {"durum": "BASLADI", "mesaj": "Görevler başarıyla başlatıldı!"})
            except Exception:
                return self._yanit_gonder(400, {"durum": "HATA", "mesaj": "İstek işlenemedi."})

        return self._yanit_gonder(404, {"durum": "HATA", "mesaj": "Geçersiz istek"})

    def log_message(self, format, *args):
        pass

class ComarUygulama:
    GOREV_ANAHTARLARI = [
        "geri_yukleme", "gecici_temizlik", "tarayici_temizlik", "dns_temizlik",
        "paket_guncelleme", "sistem_onarim", "sistem_bilgi", "baslangic",
        "olay_gunlukleri", "disk_saglik"
    ]

    def __init__(self, root):
        self.root = root
        self.ayarlar = self.ayarlari_yukle()
        self.dil = self.ayarlar.get("dil", "TR")
        self.tema_adi = self.ayarlar.get("tema", "dark")

        self.root.geometry("1040x840")
        self.dry_run = tk.BooleanVar(value=self.ayarlar.get("dry_run", False))
        self.otomatik = tk.BooleanVar(value=self.ayarlar.get("otomatik", True))
        self.calisiyor = False
        self.kuru_calistirma = bool(self.dry_run.get())
        self.otomatik_rapor_calistir = bool(self.otomatik.get())
        self.vars = {}
        self.sonuclar = {}
        self.durum_kilidi = threading.RLock()
        self.log_satirlari = []
        self.son_durum_metni = self.t("hazir")

        self.httpd = None
        self.sunucu_aktif = False
        self.guvenlik_kodu = ""
        self.hatali_giris = 0
        self.guvenlik_kilidi = threading.RLock()
        self.son_aktivite_zamani = 0
        self.aktif_wifi = self.ag_bilgisi_al()

        masaustu = os.path.join(os.path.expanduser("~"), "Desktop")
        if not os.path.exists(masaustu):
            masaustu = os.path.expanduser("~")
        
        # Arşiv Klasörü Yapısı
        self.arsiv_klasor = os.path.join(masaustu, "Comar_Arsiv")
        if not os.path.exists(self.arsiv_klasor):
            os.makedirs(self.arsiv_klasor, exist_ok=True)
            
        zaman_damgasi = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.rapor_yolu = os.path.join(self.arsiv_klasor, f"Comar_Rapor_{zaman_damgasi}.html")

        self.arayuz_kur()
        self.tema_uygula()
        self.root.protocol("WM_DELETE_WINDOW", self.kapat)
        self.ag_kontrol_baslat()

    def ag_bilgisi_al(self):
        try:
            return yerel_ip_bul()
        except Exception:
            return "Bilinmiyor"

    def ag_kontrol_baslat(self):
        def kontrol():
            while True:
                time.sleep(10)
                yeni_ip = self.ag_bilgisi_al()
                if self.sunucu_aktif and yeni_ip != self.aktif_wifi:
                    self.yaz("\n⚠️ [AĞ GÜVENLİĞİ] Wi-Fi ağı değiştiği algılandı! Güvenlik gereği sunucu kapatılıyor.")
                    self.root.after(0, self.sunucu_kapat_otomatik)
                    break
        threading.Thread(target=kontrol, daemon=True).start()

    def sunucu_kapat_otomatik(self):
        if self.sunucu_aktif:
            if self.httpd:
                try:
                    self.httpd.shutdown()
                    self.httpd.server_close()
                except Exception:
                    pass
            with self.guvenlik_kilidi:
                self.sunucu_aktif = False
                self.guvenlik_kodu = ""
            self.btn_sunucu.config(text=self.t("sunucu_ac"))
            self.lbl_sunucu_bilgi.config(text="")
            self.yaz("\n🛑 Web Kontrol Sunucusu güvenlik nedeniyle otomatik durduruldu.")

    def ayarlari_yukle(self):
        if os.path.exists(AYAR_DOSYASI):
            try:
                with open(AYAR_DOSYASI, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def ayarlari_kaydet(self):
        veri = {"dil": self.dil, "tema": self.tema_adi, "dry_run": self.dry_run.get(), "otomatik": self.otomatik.get()}
        try:
            with open(AYAR_DOSYASI, "w", encoding="utf-8") as f:
                json.dump(veri, f, indent=4)
        except Exception:
            pass

    def t(self, anahtar):
        return CEVIRILER[self.dil].get(anahtar, anahtar)

    def arayuz_kur(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title(self.t("baslik"))
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.ana = ttk.Frame(self.root, padding=15)
        self.ana.pack(fill="both", expand=True)

        ust_bar = ttk.Frame(self.ana)
        ust_bar.pack(fill="x", pady=(0, 10))

        baslik_kutu = ttk.Frame(ust_bar)
        baslik_kutu.pack(side="left")
        self.lbl_baslik = ttk.Label(baslik_kutu, text=self.t("baslik"), font=("Segoe UI", 16, "bold"))
        self.lbl_baslik.pack(anchor="w")
        self.lbl_alt = ttk.Label(baslik_kutu, text=self.t("alt_baslik"), font=("Segoe UI", 9))
        self.lbl_alt.pack(anchor="w")

        sag_butonlar = ttk.Frame(ust_bar)
        sag_butonlar.pack(side="right")
        self.btn_sunucu = ttk.Button(sag_butonlar, text=self.t("sunucu_ac"), command=self.sunucu_degistir)
        self.btn_sunucu.pack(side="left", padx=4)
        ttk.Button(sag_butonlar, text=self.t("tema_degistir"), command=self.tema_degistir).pack(side="left", padx=4)
        ttk.Button(sag_butonlar, text=self.t("dil_degistir"), command=self.dil_degistir).pack(side="left", padx=4)

        self.lbl_sunucu_bilgi = ttk.Label(self.ana, text="", font=("Consolas", 10, "bold"))
        self.lbl_sunucu_bilgi.pack(anchor="w", pady=(0, 5))

        gorev_frame = ttk.LabelFrame(self.ana, text=self.t("islemler"), padding=10)
        gorev_frame.pack(fill="x", pady=5)

        eski_secimler = {k: v.get() for k, v in self.vars.items()}
        self.vars.clear()

        for i, k in enumerate(self.GOREV_ANAHTARLARI):
            v = tk.BooleanVar(value=eski_secimler.get(k, True))
            self.vars[k] = v
            lbl = CEVIRILER[self.dil]["gorevler"][k]
            ttk.Checkbutton(gorev_frame, text=lbl, variable=v).grid(row=i // 2, column=i % 2, sticky="w", padx=10, pady=4)

        btn_frame = ttk.Frame(self.ana)
        btn_frame.pack(fill="x", pady=8)
        ttk.Button(btn_frame, text=self.t("tumunu_sec"), command=self.tumunu_sec).pack(side="left", padx=2)
        ttk.Button(btn_frame, text=self.t("temizle"), command=self.temizle).pack(side="left", padx=2)
        ttk.Checkbutton(btn_frame, text=self.t("kuru_calistir"), variable=self.dry_run).pack(side="left", padx=15)
        ttk.Checkbutton(btn_frame, text=self.t("oto_rapor"), variable=self.otomatik).pack(side="left", padx=5)

        self.calistir_btn = ttk.Button(self.ana, text=self.t("baslat"), command=self.baslat)
        self.calistir_btn.pack(fill="x", pady=8, ipady=4)

        self.progress = ttk.Progressbar(self.ana, mode="determinate")
        self.progress.pack(fill="x", pady=5)

        self.durum = ttk.Label(self.ana, text=self.t("hazir"))
        self.durum.pack(anchor="w")

        self.log = scrolledtext.ScrolledText(self.ana, height=18, font=("Consolas", 9), borderwidth=1, relief="flat")
        self.log.pack(fill="both", expand=True, pady=5)

        alt = ttk.Frame(self.ana)
        alt.pack(fill="x")
        ttk.Button(alt, text=self.t("rapor_ac"), command=self.rapor_ac).pack(side="right")

    def sunucu_degistir(self):
        if not self.sunucu_aktif:
            self.aktif_wifi = self.ag_bilgisi_al()
            alfabe = string.ascii_uppercase + string.digits
            with self.guvenlik_kilidi:
                self.guvenlik_kodu = "".join(secrets.choice(alfabe) for _ in range(6))
                self.hatali_giris = 0
                self.son_aktivite_zamani = time.time()
            ComarWebHandler.app_ref = self
            yerel_ip = yerel_ip_bul()
            try:
                self.httpd = ThreadingHTTPServer(("0.0.0.0", SUNUCU_PORT), ComarWebHandler)
                self.httpd.daemon_threads = True
                threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
                self.sunucu_aktif = True
                self.btn_sunucu.config(text=self.t("sunucu_kapat"))
                
                baglanti_url = f"http://{yerel_ip}:{SUNUCU_PORT}/"
                bilgi = f"🟢 Güvenli Wi-Fi Sunucu Aktif | IP: {yerel_ip} | Kod: [ {self.guvenlik_kodu} ]"
                self.lbl_sunucu_bilgi.config(text=bilgi, foreground="#00c853")
                self.yaz(f"\n🌐 {bilgi}")
                
                # Konsol QR Kod Üretimi
                if QR_KUTUPHANE_VAR:
                    self.yaz("\n📱 Telefonunuzla doğrudan bağlanmak için bu QR kodu tarayabilirsiniz:")
                    qr = qrcode.QRCode()
                    qr.add_data(baglanti_url)
                    qr.make(fit=True)
                    f = io.StringIO()
                    qr.print_ascii(out=f)
                    self.yaz(f.getvalue())
                else:
                    self.yaz(f"💡 Bağlantı Adresi: {baglanti_url}")

            except Exception as e:
                messagebox.showerror("Sunucu Hatası", "Sunucu başlatılamadı. Lütfen port kullanımını kontrol edin.")
        else:
            self.sunucu_kapat_otomatik()

    def tema_uygula(self):
        tm = TEMALAR[self.tema_adi]
        self.root.configure(bg=tm["bg"])
        self.style.configure("TFrame", background=tm["bg"])
        self.style.configure("TLabelframe", background=tm["bg"], foreground=tm["fg"])
        self.style.configure("TLabelframe.Label", background=tm["bg"], foreground=tm["accent"], font=("Segoe UI", 10, "bold"))
        self.style.configure("TLabel", background=tm["bg"], foreground=tm["fg"])
        self.style.configure("TCheckbutton", background=tm["bg"], foreground=tm["fg"])
        self.style.configure("TButton", padding=5)
        self.lbl_baslik.configure(foreground=tm["accent"])
        self.lbl_alt.configure(foreground=tm["sub_fg"])
        self.durum.configure(foreground=tm["sub_fg"])
        self.log.configure(bg=tm["log_bg"], fg=tm["log_fg"], insertbackground=tm["fg"])

    def tema_degistir(self):
        self.tema_adi = "light" if self.tema_adi == "dark" else "dark"
        self.tema_uygula()
        self.ayarlari_kaydet()

    def dil_degistir(self):
        self.dil = "EN" if self.dil == "TR" else "TR"
        self.ayarlari_kaydet()
        self.arayuz_kur()
        self.tema_uygula()

    def kapat(self):
        if self.calisiyor:
            if not messagebox.askyesno("Çomar", self.t("cikis_onay")):
                return
        if self.httpd:
            try:
                self.httpd.shutdown()
                self.httpd.server_close()
            except Exception:
                pass
        self.sunucu_aktif = False
        self.guvenlik_kodu = ""
        self.ayarlari_kaydet()
        self.root.destroy()

    def yaz(self, m):
        satirlar = str(m).splitlines() or [""]
        with self.durum_kilidi:
            self.log_satirlari.extend(satirlar)
            self.log_satirlari = self.log_satirlari[-500:]
        def _(metin=str(m)):
            try:
                self.log.insert("end", metin + "\n")
                self.log.see("end")
            except Exception:
                pass
        try:
            self.root.after(0, _)
        except Exception:
            pass

    def durum_guncelle(self, m):
        with self.durum_kilidi:
            self.son_durum_metni = str(m)
        try:
            self.root.after(0, lambda metin=m: self.durum.config(text=metin))
        except Exception:
            pass

    def tumunu_sec(self):
        for v in self.vars.values():
            v.set(True)

    def temizle(self):
        for v in self.vars.values():
            v.set(False)

    def uzaktan_baslat(self, secili):
        if self.calisiyor:
            return
        # Tk değişkenlerini arka plan iş parçacığından okumamak için başlangıçta kopyala.
        self.kuru_calistirma = bool(self.dry_run.get())
        self.otomatik_rapor_calistir = bool(self.otomatik.get())
        self.calisiyor = True
        self.calistir_btn.config(state="disabled")
        self.progress["maximum"] = len(secili)
        self.progress["value"] = 0
        self.sonuclar = {}
        threading.Thread(target=self.calistir, args=(secili,), daemon=True).start()

    def baslat(self):
        if self.calisiyor:
            return
        secili = [k for k, v in self.vars.items() if v.get()]
        if not secili:
            messagebox.showwarning("Çomar", self.t("uyari_secim"))
            return
        if not yonetici_mi():
            if ISLETIM_SISTEMI == "Windows":
                if messagebox.askyesno(self.t("yetki_baslik"), self.t("yetki_mesaj_win")):
                    yonetici_olarak_baslat()
                    self.root.destroy()
                return
            else:
                if not messagebox.askyesno(self.t("yetki_baslik"), self.t("yetki_mesaj_unix")):
                    return

        if not self.dry_run.get():
            onay = messagebox.askyesno(
                "Çomar - İşlem Onayı",
                "Kuru çalıştırma kapalı. Seçilen görevler gerçek dosya temizliği, sistem değişikliği veya paket güncellemesi yapabilir.\n\nDevam etmek istiyor musunuz?"
            )
            if not onay:
                return

        self.ayarlari_kaydet()
        self.log.delete("1.0", "end")
        with self.durum_kilidi:
            self.log_satirlari.clear()
        self.uzaktan_baslat(secili)

    def calistir(self, secili):
        try:
            for i, k in enumerate(secili):
                gorev_adi = CEVIRILER[self.dil]["gorevler"][k]
                self.durum_guncelle(f"{self.t('isleniyor')}: {gorev_adi} ({i + 1}/{len(secili)})")
                self.yaz(f"\n🐕 >>> [{gorev_adi}] başlıyor...")
                try:
                    self.sonuclar[k] = self.gorev(k)
                except Exception as e:
                    self.sonuclar[k] = ("HATA", str(e))
                
                durum_kod, detay = self.sonuclar[k]
                self.yaz(f">>> Durum: {durum_kod}")
                if detay.strip():
                    # Detaylı geri bildirimin log penceresine daha okunaklı basılması
                    for satir in detay.strip().splitlines()[:10]:  # Uzun çıkışları sınırla
                        self.yaz(f"    • {satir}")
                
                self.root.after(0, lambda v=i + 1: self.progress.configure(value=v))

            self.rapor_olustur()
            self.yaz(f"\n📄 Rapor arşivlendi: {self.rapor_yolu}")
            if self.otomatik_rapor_calistir:
                self.rapor_ac()
            self.durum_guncelle(self.t("tamamlandi"))
        except Exception:
            self.yaz("Kritik işlem hatası.")
        finally:
            self.calisiyor = False
            self.root.after(0, lambda: self.calistir_btn.config(state="normal"))

    def komut(self, cmd_list, timeout=3600):
        try:
            r = subprocess.run(cmd_list, capture_output=True, text=True, timeout=timeout, encoding="utf-8", errors="ignore", shell=False)
            return r.returncode, (r.stdout or "") + (r.stderr or "")
        except Exception as e:
            return -1, str(e)

    def gorev(self, k):
        metod = getattr(self, f"gorev_{k}", None)
        return metod() if metod else ("BILINMEYEN", "")

    def gorev_geri_yukleme(self):
        if self.kuru_calistirma:
            return ("ATLADI", "Kuru çalıştırma.")
        if ISLETIM_SISTEMI == "Windows":
            rc, out = self.komut(["powershell", "-NoProfile", "-Command", "Checkpoint-Computer -Description 'Comar_Bakim' -RestorePointType MODIFY_SETTINGS"], timeout=600)
            return ("OK" if rc == 0 else "HATA", out)
        elif ISLETIM_SISTEMI == "Darwin":
            rc, out = self.komut(["tmutil", "localsnapshot"], timeout=300)
            return ("OK" if rc == 0 else "HATA", out)
        return ("ATLADI", "Linux snapshot aracı atlandı.")

    def gorev_gecici_temizlik(self):
        """Yalnızca geçerli kullanıcının geçici klasöründeki öğeleri temizler."""
        hedef = tempfile.gettempdir()
        silinen = 0
        atlanan = 0
        if not os.path.isdir(hedef):
            return ("ATLADI", f"Geçici klasör bulunamadı: {hedef}")
        try:
            ogeler = os.listdir(hedef)
        except OSError as e:
            return ("HATA", f"Geçici klasör okunamadı: {e}")
        for oge in ogeler:
            tam = os.path.join(hedef, oge)
            try:
                # Unix sistemlerde ortak /tmp içindeki diğer kullanıcıların dosyalarına dokunma.
                if hasattr(os, "getuid") and os.stat(tam, follow_symlinks=False).st_uid != os.getuid():
                    atlanan += 1
                    continue
                if self.kuru_calistirma:
                    silinen += 1
                    continue
                if os.path.islink(tam) or os.path.isfile(tam):
                    os.unlink(tam)
                    silinen += 1
                elif os.path.isdir(tam):
                    shutil.rmtree(tam)
                    silinen += 1
            except (OSError, PermissionError):
                atlanan += 1
        durum = "ATLADI" if self.kuru_calistirma else "OK"
        eylem = "temizlenebilir öğe bulundu" if self.kuru_calistirma else "öğe temizlendi"
        return (durum, f"Kullanıcı geçici klasöründe {silinen} {eylem}; {atlanan} öğe izin/kullanım nedeniyle atlandı. Klasör: {hedef}")

    def gorev_tarayici_temizlik(self):
        home = os.path.expanduser("~")
        if ISLETIM_SISTEMI == "Windows":
            local = os.environ.get("LOCALAPPDATA", "")
            kokler = [os.path.join(local, "Google", "Chrome", "User Data"),
                      os.path.join(local, "Microsoft", "Edge", "User Data")]
        elif ISLETIM_SISTEMI == "Darwin":
            kokler = [os.path.join(home, "Library", "Caches", "Google", "Chrome"),
                      os.path.join(home, "Library", "Caches", "Microsoft", "Edge"),
                      os.path.join(home, "Library", "Caches", "Firefox")]
        else:
            kokler = [os.path.join(home, ".cache", "google-chrome"),
                      os.path.join(home, ".cache", "chromium"),
                      os.path.join(home, ".cache", "mozilla", "firefox")]

        hedefler = []
        for kok in kokler:
            if not os.path.isdir(kok):
                continue
            try:
                profiller = [os.path.join(kok, x) for x in os.listdir(kok) if os.path.isdir(os.path.join(kok, x))]
            except OSError:
                profiller = [kok]
            for profil in profiller:
                for ad in ("Cache", "Code Cache", "GPUCache", "cache2"):
                    aday = os.path.join(profil, ad)
                    if os.path.isdir(aday) and aday not in hedefler:
                        hedefler.append(aday)

        temizlenen = 0
        atlanan = 0
        for yol in hedefler:
            try:
                if self.kuru_calistirma:
                    temizlenen += 1
                else:
                    shutil.rmtree(yol)
                    temizlenen += 1
            except OSError:
                atlanan += 1
        if not hedefler:
            return ("ATLADI", "Desteklenen tarayıcılara ait bilinen önbellek klasörü bulunamadı.")
        return ("ATLADI" if self.kuru_calistirma else "OK",
                f"{temizlenen} önbellek klasörü {'temizlenmeye uygun bulundu' if self.kuru_calistirma else 'temizlendi'}; {atlanan} klasör kullanımda/erişilemez.")

    def gorev_dns_temizlik(self):
        if self.kuru_calistirma:
            return ("ATLADI", "Kuru çalıştırma.")
        if ISLETIM_SISTEMI == "Windows":
            rc, out = self.komut(["ipconfig", "/flushdns"], timeout=60)
            return ("OK" if rc == 0 else "HATA", out)
        elif ISLETIM_SISTEMI == "Darwin":
            rc, out = self.komut(["dscacheutil", "-flushcache"], timeout=60)
            return ("OK" if rc == 0 else "HATA", out)
        resolvectl = shutil.which("resolvectl")
        if resolvectl:
            rc, out = self.komut([resolvectl, "flush-caches"], timeout=60)
            return ("OK" if rc == 0 else "HATA", out)
        systemd_resolve = shutil.which("systemd-resolve")
        if systemd_resolve:
            rc, out = self.komut([systemd_resolve, "--flush-caches"], timeout=60)
            return ("OK" if rc == 0 else "HATA", out)
        return ("ATLADI", "Bu Linux sisteminde desteklenen DNS önbellek temizleme aracı bulunamadı.")

    def gorev_paket_guncelleme(self):
        if ISLETIM_SISTEMI == "Windows":
            if self.kuru_calistirma:
                _, out = self.komut(["winget", "upgrade"], timeout=180)
                return ("ATLADI", out[-1500:])
            rc, out = self.komut(["winget", "upgrade", "--all", "--silent", "--accept-package-agreements", "--accept-source-agreements"], timeout=3600)
            return ("OK" if rc == 0 else "HATA", out[-1500:])
        elif ISLETIM_SISTEMI == "Darwin":
            rc, out = self.komut(["brew", "outdated"] if self.kuru_calistirma else ["brew", "update"], timeout=1800)
            if self.kuru_calistirma:
                return ("ATLADI" if rc == 0 else "HATA", "Kuru çalıştırma; hiçbir paket güncellenmedi.\n" + out[-1500:])
            if rc != 0:
                return ("HATA", out[-1500:])
            rc, out2 = self.komut(["brew", "upgrade"], timeout=7200)
            return ("OK" if rc == 0 else "HATA", (out + "\n" + out2)[-2500:])
        apt_get = shutil.which("apt-get")
        dnf = shutil.which("dnf")
        pacman = shutil.which("pacman")
        zypper = shutil.which("zypper")
        if apt_get:
            if self.kuru_calistirma:
                rc, out = self.komut(["apt", "list", "--upgradable"], timeout=180)
                return ("ATLADI" if rc == 0 else "HATA", "Kuru çalıştırma; hiçbir paket güncellenmedi.\n" + out[-1500:])
            rc1, out1 = self.komut([apt_get, "update"], timeout=1800)
            if rc1 != 0:
                return ("HATA", "Paket listeleri yenilenemedi.\n" + out1[-1500:])
            rc2, out2 = self.komut([apt_get, "upgrade", "-y"], timeout=7200)
            return ("OK" if rc2 == 0 else "HATA", (out1 + "\n" + out2)[-3000:])
        if dnf:
            komut = [dnf, "check-update"] if self.kuru_calistirma else [dnf, "upgrade", "-y"]
        elif pacman:
            komut = [pacman, "-Qu"] if self.kuru_calistirma else [pacman, "-Syu", "--noconfirm"]
        elif zypper:
            komut = [zypper, "list-updates"] if self.kuru_calistirma else [zypper, "update", "-y"]
        else:
            return ("ATLADI", "Desteklenen paket yöneticisi (apt, dnf, pacman, zypper) bulunamadı.")
        rc, out = self.komut(komut, timeout=7200)
        if self.kuru_calistirma:
            return ("ATLADI" if rc in (0, 100) else "HATA", "Kuru çalıştırma; hiçbir paket güncellenmedi.\n" + out[-2000:])
        return ("OK" if rc == 0 else "HATA", out[-2000:])

    def gorev_sistem_onarim(self):
        if self.kuru_calistirma:
            return ("ATLADI", "Kuru çalıştırma.")
        if ISLETIM_SISTEMI == "Windows":
            rc1, o1 = self.komut(["Dism", "/Online", "/Cleanup-Image", "/RestoreHealth"], timeout=7200)
            rc2, o2 = self.komut(["sfc", "/scannow"], timeout=7200)
            durum = "OK" if rc1 == 0 and rc2 == 0 else "HATA"
            return (durum, f"DISM (kod {rc1}):\n{o1[-1000:]}\nSFC (kod {rc2}):\n{o2[-1000:]}")
        return ("ATLADI", "Bu işletim sisteminde otomatik sistem dosyası onarımı henüz desteklenmiyor; hiçbir değişiklik yapılmadı.")

    def gorev_sistem_bilgi(self):
        kok = os.path.abspath(os.sep)
        toplam, kullanilan, bos = shutil.disk_usage(kok)
        gb = 1024 ** 3
        ram_bilgi = "RAM bilgisi alınamadı."
        try:
            if ISLETIM_SISTEMI == "Windows":
                class MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                                ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                                ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                                ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                                ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
                stat = MEMORYSTATUSEX()
                stat.dwLength = ctypes.sizeof(stat)
                if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
                    ram_bilgi = f"RAM: Toplam {stat.ullTotalPhys/gb:.1f} GB | Kullanılabilir {stat.ullAvailPhys/gb:.1f} GB"
            else:
                sayfa = os.sysconf("SC_PAGE_SIZE")
                toplam_ram = os.sysconf("SC_PHYS_PAGES") * sayfa
                bos_ram = os.sysconf("SC_AVPHYS_PAGES") * sayfa
                ram_bilgi = f"RAM: Toplam {toplam_ram/gb:.1f} GB | Kullanılabilir {bos_ram/gb:.1f} GB"
        except Exception:
            pass
        bilgi_metni = (f"İşletim Sistemi: {platform.platform()}\nMimari: {platform.machine()}\n{ram_bilgi}\n"
                       f"Disk Alanı ({kok}) -> Toplam: {toplam/gb:.1f} GB | Kullanılan: {kullanilan/gb:.1f} GB | Boş: {bos/gb:.1f} GB")
        return ("OK", bilgi_metni)

    def gorev_baslangic(self):
        if ISLETIM_SISTEMI == "Windows":
            rc, out = self.komut(["powershell", "-NoProfile", "-Command", "Get-CimInstance Win32_StartupCommand | Select-Object Name, Command"], timeout=120)
            return ("OK" if rc == 0 else "HATA", out[:3000])
        if ISLETIM_SISTEMI == "Darwin":
            rc, out = self.komut(["launchctl", "list"], timeout=120)
        else:
            systemctl = shutil.which("systemctl")
            if not systemctl:
                return ("ATLADI", "systemctl bulunamadı; başlangıç servisleri listelenemedi.")
            rc, out = self.komut([systemctl, "list-unit-files", "--state=enabled", "--no-pager"], timeout=120)
        return ("OK" if rc == 0 else "ATLADI", out[:5000])

    def gorev_olay_gunlukleri(self):
        if ISLETIM_SISTEMI == "Windows":
            rc, out = self.komut(["wevtutil", "qe", "System", "/q:*[System[Level=1 or Level=2]]", "/c:5", "/f:text"], timeout=120)
            return ("OK" if rc == 0 else "ATLADI", out or "Kritik sistem hata günlüğü bulunamadı veya erişilemedi.")
        if ISLETIM_SISTEMI == "Darwin":
            rc, out = self.komut(["log", "show", "--last", "1h", "--predicate", 'messageType == "error"', "--style", "compact"], timeout=180)
        else:
            journalctl = shutil.which("journalctl")
            if not journalctl:
                return ("ATLADI", "journalctl bulunamadı; sistem hata günlükleri listelenemedi.")
            rc, out = self.komut([journalctl, "-p", "3", "-n", "20", "--no-pager"], timeout=120)
        return ("OK" if rc == 0 else "ATLADI", out[-5000:] or "Kayıt bulunamadı veya günlük erişimi desteklenmiyor.")

    def gorev_disk_saglik(self):
        if ISLETIM_SISTEMI == "Windows":
            rc, out = self.komut(["powershell", "-NoProfile", "-Command", "Get-PhysicalDisk | Select-Object FriendlyName, HealthStatus, OperationalStatus | Format-Table -AutoSize"], timeout=120)
            if rc != 0 or not out.strip():
                return ("ATLADI", out or "Disk sağlık bilgisi alınamadı; depolama sürücüsü veya izinler desteklemiyor olabilir.")
            return ("OK", out)
        smartctl = shutil.which("smartctl")
        if smartctl:
            rc, out = self.komut([smartctl, "--scan"], timeout=60)
            aygitlar = [satir.split()[0] for satir in out.splitlines() if satir.strip().startswith("/dev/")]
            if aygitlar:
                rc, sonuc = self.komut([smartctl, "-H", aygitlar[0]], timeout=120)
                return ("OK" if rc == 0 else "HATA", sonuc[-2000:])
            return ("ATLADI", "smartctl bulundu ancak denetlenebilir disk aygıtı belirlenemedi.\n" + out[-1000:])
        return ("ATLADI", "S.M.A.R.T. denetimi için smartmontools (smartctl) kurulu değil; sağlık durumu doğrulanamadı.")

    def rapor_olustur(self):
        renk = {"OK": "#34a853", "HATA": "#ea4335", "ATLADI": "#fbbc04", "BILINMEYEN": "#5f6368"}
        parcalar = [
            '<!DOCTYPE html><html lang="tr"><head><meta charset="UTF-8"><title>Çomar Arşiv Raporu</title><style>',
            'body{font-family:Segoe UI,sans-serif;background:#f0f2f5;padding:20px}.container{max-width:900px;margin:auto;background:#fff;padding:25px;border-radius:10px;box-shadow:0 4px 15px rgba(0,0,0,0.1)}',
            'pre{background:#1e1e1e;color:#d4d4d4;padding:12px;border-radius:6px;white-space:pre-wrap}.badge{padding:3px 8px;border-radius:10px;color:#fff;font-size:0.8em;margin-left:8px}',
            '</style></head><body><div class="container"><h1>🐕 Çomar Sistem Bakım Raporu</h1>',
            f'<p><b>Oluşturulma Tarihi:</b> {datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")}</p><hr>'
        ]
        for k, (durum, icerik) in self.sonuclar.items():
            guvenli = icerik.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            baslik = html.escape(CEVIRILER[self.dil]["gorevler"].get(k, k))
            guvenli_durum = html.escape(str(durum))
            parcalar.append(f'<h3>{baslik}<span class="badge" style="background:{renk.get(durum, "#555")}">{guvenli_durum}</span></h3><pre>{guvenli}</pre>')
        parcalar.append('</div></body></html>')
        
        with open(self.rapor_yolu, "w", encoding="utf-8") as f:
            f.write("".join(parcalar))

    def rapor_ac(self):
        if os.path.exists(self.rapor_yolu):
            if ISLETIM_SISTEMI == "Windows":
                os.startfile(self.rapor_yolu)
            elif ISLETIM_SISTEMI == "Darwin":
                subprocess.run(["open", self.rapor_yolu])
            else:
                subprocess.run(["xdg-open", self.rapor_yolu])
        else:
            messagebox.showinfo("Çomar", self.t("rapor_yok"))

if __name__ == "__main__":
    if ISLETIM_SISTEMI == "Windows" and not yonetici_mi():
        try:
            script = os.path.abspath(__file__)
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}"', None, 1)
            sys.exit(0)
        except Exception:
            pass
    root = tk.Tk()
    app = ComarUygulama(root)
    root.mainloop()