# Devonic - Hand Gesture Volume Control

Windows için kamera ile el hareketlerinden ses kontrolü yapan bir Python uygulaması.

## Özellikler

- Kamera üzerinden el algılama (MediaPipe)
- Başparmak + orta parmak iki kez temas edince ses kontrol modu aç/kapat
- Ses kontrol modu açıkken başparmak + işaret parmağı mesafesi ile ses ayarı
- Gerçek zamanlı ekran göstergeleri

## Gereksinimler

- Windows 10/11
- Kamera
- Ses çıkış cihazı (hoparlör/kulaklık)

## Kurulum

```bash
pip install -r requirements.txt
```

## Çalıştırma

```bash
python devonic.py
```

## Kullanım

- Mod aç/kapat: Başparmak + orta parmak 2 kez temas
- Ses ayarı: Başparmak + işaret parmağı mesafesi
- Çıkış: `q` veya `ESC`

## Notlar

- Ses kontrolü için varsayılan Windows ses cihazı kullanılır.
- Eğer ses değişmiyorsa, Windows’ta varsayılan çıkış cihazını kontrol edin.

## Lisans

MIT
