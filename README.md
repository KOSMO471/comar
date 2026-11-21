 <div align="center">

# 🐕 ÇOMAR
### Akıllı Sistem Bakım Asistanı
**Smart System Maintenance Assistant**

[![GitHub](https://img.shields.io/badge/GitHub-KOSMO471%2Fcomar-181717?style=for-the-badge&logo=github)](https://github.com/KOSMO471/comar)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-854836?style=for-the-badge)](https://github.com/KOSMO471/comar)
[![License](https://img.shields.io/badge/License-MIT-FFB22C?style=for-the-badge)](LICENSE)

**Bilgisayarınızın sadık dostu Çomar ile sisteminiz hep temiz, düzenli ve güvende!**

*Keep your system clean, organized, and secure with your loyal companion, Comar!*

[🌐 Web Sitesi](https://kosmo471.github.io/comar/) • [📥 Kaynak Kod](https://github.com/KOSMO471/comar) • [🐛 Hata Bildir](https://github.com/KOSMO471/comar/issues)

</div>

---

## 📌 İçindekiler / Table of Contents

- [🇹🇷 Türkçe](#-türkçe)
  - [Çomar Nedir?](#-çomar-nedir)
  - [Özellikler](#-özellikler)
  - [Kurulum](#-kurulum)
  - [Kullanım](#-kullanım)
  - [Uzaktan Kontrol](#-uzaktan-kontrol)
  - [Güvenlik](#-güvenlik-uyarısı)
- [🇬🇧 English](#-english)
  - [What is Comar?](#-what-is-comar)
  - [Features](#-features)
  - [Installation](#-installation)
  - [Usage](#-usage)
  - [Remote Control](#-remote-control)
  - [Security](#-security-notice)
- [📄 Lisans / License](#-lisans--license)
- [🤝 Katkıda Bulunma / Contributing](#-katkıda-bulunma--contributing)

---

# 🇹🇷 Türkçe

## 🐕 Çomar Nedir?

**Çomar**, bilgisayarınızın bakımını kolaylaştırmak için geliştirilmiş açık kaynaklı bir sistem bakım asistanıdır.

Windows, macOS ve Linux işletim sistemlerini hedefleyen Çomar; gereksiz dosyaların temizlenmesine, sistem bakım işlemlerine ve uygulama güncellemelerinin yönetilmesine yardımcı olur.

Üstelik yerel web sunucusu sayesinde bilgisayarınızı aynı ağdaki telefonunuzdan da kontrol edebilirsiniz.

**Çomar'ın amacı:** Karmaşık sistem bakım işlemlerini daha kolay ve erişilebilir hâle getirmek.

## ✨ Özellikler

| Özellik | Açıklama |
|---|---|
| 🖥️ Çapraz Platform | Windows, macOS ve Linux desteği |
| 🧹 Geçici Dosya Temizliği | TEMP ve önbellek dosyalarının temizlenmesi |
| 🌐 Tarayıcı Temizliği | Tarayıcı önbelleklerinin temizlenmesi |
| 🔄 DNS Temizliği | DNS önbelleğinin temizlenmesi |
| 📦 Paket Güncelleme | `winget`, `brew` ve `apt` gibi paket yöneticileriyle güncelleme |
| 🛠️ Sistem Bakımı | Sistem onarım ve bakım işlemleri |
| 📊 Sistem Bilgileri | Bilgisayarın sistem bilgilerini görüntüleme |
| 🚀 Başlangıç Yönetimi | Başlangıç uygulamalarını yönetmeye yönelik işlemler |
| 📋 Olay Günlükleri | Sistem günlükleriyle ilgili işlemler |
| 💽 Disk Sağlığı | Disk sağlığıyla ilgili kontroller |
| 📱 Uzaktan Kontrol | Yerel web paneli üzerinden telefonla yönetim |
| 🌓 Koyu / Açık Tema | Modern ve göz yormayan arayüz |

## 🚀 Kurulum

### Gereksinimler

- Python 3
- İnternet bağlantısı (güncelleme ve çevrim içi işlemler için)
- Desteklenen bir işletim sistemi

### 1. Depoyu klonlayın

```bash
git clone https://github.com/KOSMO471/comar.git
```

### 2. Proje klasörüne girin

```bash
cd comar
```

### 3. Çomar'ı çalıştırın

```bash
python Comar.py
```

Linux ve macOS sistemlerinde bazı bakım işlemleri için yönetici izinleri gerekebilir. Yalnızca ihtiyaç duyduğunuzda ve çalıştırılan işlemleri anladığınızda uygun yetkilerle çalıştırın.

## 🎮 Kullanım

1. Çomar uygulamasını başlatın.
2. Ana ekrandaki bakım seçeneklerini inceleyin.
3. Gerçekleştirmek istediğiniz işlemleri seçin.
4. İşlemleri başlatın ve ekrandaki sonuçları takip edin.

**Not:** İşletim sistemine ve kullanıcı izinlerine bağlı olarak bazı işlemler çalışmayabilir veya ek yetki isteyebilir.

## 📱 Uzaktan Kontrol

Çomar, yerel web sunucusu üzerinden telefonla kontrol edilebilir.

### Nasıl çalışır?

1. Bilgisayarınızda Çomar'ı başlatın.
2. Uygulamadaki yerel sunucu özelliğini açın.
3. Oluşturulan güvenlik kodunu alın.
4. Telefonunuzu bilgisayarınızla aynı Wi-Fi ağına bağlayın.
5. Web panelini açın ve güvenlik kodunu girin.
6. Desteklenen bakım işlemlerini telefonunuzdan yönetin.

**Önemli:** Uzaktan kontrol için bilgisayardaki yerel sunucunun çalışır durumda olması gerekir. Bu özellik, yerel ağ üzerinden erişim mantığıyla çalışır.

## 🔐 Güvenlik Uyarısı

Çomar, sistem üzerinde değişiklik yapabilen bakım işlemleri içerir.

- Bilmediğiniz işlemleri çalıştırmayın.
- Önemli dosyalarınızı düzenli olarak yedekleyin.
- Güvenlik kodunuzu başkalarıyla paylaşmayın.
- Yerel sunucuyu güvenmediğiniz ağlarda kullanmayın.
- Yönetici izinlerini yalnızca gerektiğinde verin.

---

# 🇬🇧 English

## 🐕 What is Comar?

**Comar** is an open-source system maintenance assistant designed to make computer maintenance easier.

Targeting Windows, macOS, and Linux, Comar helps users clean unnecessary files, perform system maintenance tasks, and manage application updates.

It also provides a local web server that allows you to control supported functions from your phone over the same local network.

**Comar's goal:** Making system maintenance easier and more accessible.

## ✨ Features

| Feature | Description |
|---|---|
| 🖥️ Cross-Platform | Windows, macOS, and Linux support |
| 🧹 Temporary File Cleanup | Cleans TEMP and cache files |
| 🌐 Browser Cleanup | Cleans browser cache |
| 🔄 DNS Cleanup | Clears DNS cache |
| 📦 Package Updates | Updates applications using `winget`, `brew`, and `apt` |
| 🛠️ System Maintenance | System repair and maintenance tasks |
| 📊 System Information | Displays system information |
| 🚀 Startup Management | Tools for managing startup applications |
| 📋 Event Logs | System log-related operations |
| 💽 Disk Health | Disk health-related checks |
| 📱 Remote Control | Phone control through a local web panel |
| 🌓 Dark / Light Theme | Modern, eye-friendly interface |

## 🚀 Installation

### Requirements

- Python 3
- Internet connection (for updates and online operations)
- A supported operating system

### 1. Clone the repository

```bash
git clone https://github.com/KOSMO471/comar.git
```

### 2. Open the project directory

```bash
cd comar
```

### 3. Run Comar

```bash
python Comar.py
```

On Linux and macOS, some maintenance tasks may require administrator privileges. Use elevated permissions only when necessary and when you understand the operation being performed.

## 🎮 Usage

1. Launch Comar.
2. Explore the available maintenance options.
3. Select the tasks you want to perform.
4. Start the tasks and follow the results displayed on the screen.

**Note:** Some operations may require additional permissions or may not be available on every operating system.

## 📱 Remote Control

Comar can be controlled from a phone through its local web server.

### How does it work?

1. Launch Comar on your computer.
2. Enable the local server feature.
3. Obtain the generated security code.
4. Connect your phone to the same Wi-Fi network as your computer.
5. Open the web panel and enter the security code.
6. Manage supported maintenance tasks from your phone.

**Important:** The local server must remain active while using remote control. This feature is designed to work over your local network.

## 🔐 Security Notice

Comar includes maintenance operations that can modify your system.

- Do not run operations you do not understand.
- Back up important files regularly.
- Never share your security code with untrusted people.
- Avoid using the local server on untrusted networks.
- Grant administrator privileges only when necessary.

---

## 🤝 Katkıda Bulunma / Contributing

Çomar'ı geliştirmeye katkıda bulunmak isterseniz katkılarınızı bekliyoruz!

If you would like to contribute to Comar, contributions are welcome!

1. Depoyu fork edin / Fork the repository.
2. Yeni bir branch oluşturun / Create a new branch.
3. Değişikliklerinizi yapın / Make your changes.
4. Pull Request gönderin / Submit a Pull Request.

Hata bildirimleri ve özellik önerileri için:

[GitHub Issues](https://github.com/KOSMO471/comar/issues)

---

## 📄 Lisans / License

Bu proje **MIT Lisansı** ile lisanslanmıştır.

This project is licensed under the **MIT License**.

Detaylar için [LICENSE](LICENSE) dosyasına bakabilirsiniz.

---

<div align="center">

### 🐕 Çomar ile bilgisayarınız emin ellerde!

**Your computer is in good paws with Comar!**

Geliştirici / Developer: **Mehmet Fatih Yıldırım**

[⭐ GitHub'da projeye yıldız ver](https://github.com/KOSMO471/comar)

</div>
