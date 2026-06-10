# DevonicCEObot

Telegram üzerinden sinyal ve günlük özet paylaşımı yapan basit bir bot.

## Güvenlik Notu (Önemli)

Bu proje public olduğu için **token, kullanıcı kimlikleri ve kanal bilgisi kesinlikle koda yazılmamalıdır**.

Eğer daha önce token paylaştıysan:

1. BotFather üzerinden token'ı hemen yenile.
2. Eski token'ı iptal et.
3. Yeni token'ı sadece `.env` içinde sakla.

## Kurulum

1. Python 3.10+ kur.
2. Paketleri yükle:
   ```bash
   pip install python-telegram-bot python-dotenv nest-asyncio
   ```
3. `.env.example` dosyasını kopyala ve `.env` oluştur:
   ```bash
   copy .env.example .env
   ```
4. `.env` içini doldur:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHANNEL_ID`
   - `ALLOWED_USER_IDS` (virgülle ayrılmış Telegram user id listesi)

## Çalıştırma

```bash
python Bot.py
```

## Komutlar

- `/start`
- `/help`
- `/signal PARITE YON GIRIS SL TP1 TP2 BORSA Aciklama`
- `/summary IslemSayisi TP SL OncekiBakiye SuankiBakiye Kar`

## Örnek `.env`

```env
TELEGRAM_BOT_TOKEN=123456:YOUR_NEW_TOKEN
TELEGRAM_CHANNEL_ID=@your_channel
ALLOWED_USER_IDS=111111111,222222222
```

## Lisans

Bu proje [MIT License](LICENSE) ile lisanslanmıştır.
