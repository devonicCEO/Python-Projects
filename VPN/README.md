# DEVONIC VPN

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

Terminal tabanlı, renkli arayüze sahip bir **otomatik ücretsiz proxy bağlantı aracı**.

> ⚠️ Bu proje teknik olarak tam bir sistem seviyesinde VPN tüneli oluşturmaz.
> HTTP/HTTPS proxy kullanarak IP değişimini simüle eder.

## Özellikler

- Ücretsiz proxy kaynaklarından otomatik liste çekme
- Çalışan proxy’yi test edip seçme
- Anlık VPN (proxy) IP görüntüleme
- Renkli ve kullanıcı dostu CLI menüsü
- Bağlantıyı başlat/durdur ve durum takibi

## Proje Yapısı

```bash
.
├── .gitignore
├── LICENSE
├── devonic_vpn.py
├── requirements.txt
└── README.md
```

## Gereksinimler

- Python 3.9+
- `requests`
- `colorama`

## Kurulum

```bash
# 1) Depoyu klonla
git clone https://github.com/devonicCEO/VPN.git
cd VPN

# 2) (Önerilen) Sanal ortam oluştur
python -m venv .venv

# 3) Sanal ortamı aktif et (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# 4) Bağımlılıkları kur
pip install -r requirements.txt
```

## Çalıştırma

```bash
python devonic_vpn.py
```

## Menü

- `1` → VPN (proxy) başlat
- `2` → VPN durdur
- `3` → Bilgi ekranı
- `0` → Çıkış

## Notlar

- Ücretsiz proxy’ler her zaman stabil olmayabilir.
- Bazı siteler proxy IP’lerini engelleyebilir.
- Yalnızca yasal ve etik kullanım için tasarlanmıştır.

## Katkı

Pull request’lere açıktır. Büyük değişiklikler için önce issue açmanız önerilir.

## Lisans

Bu proje **MIT License** ile lisanslanmıştır.
Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

Developed by **devonicCEO**
