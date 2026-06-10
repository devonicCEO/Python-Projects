import logging
import os

import nest_asyncio
from dotenv import load_dotenv
from telegram import BotCommand, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

nest_asyncio.apply()
load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "")

_izinli_kisiler_raw = os.getenv("ALLOWED_USER_IDS", "")
IZINLI_KISILER = {
    int(user_id.strip())
    for user_id in _izinli_kisiler_raw.split(",")
    if user_id.strip().isdigit()
}


COMMANDS = [
    BotCommand("start", "Botu başlat"),
    BotCommand("signal", "Sinyal gönder"),
    BotCommand("help", "Yardım"),
    BotCommand("summary", "Get a summary of signals"),
]


def izin_var_mi(user_id: int) -> bool:
    return user_id in IZINLI_KISILER


def normalize_number(value: str) -> str:
    return value.replace(",", ".")


def validate_direction(direction: str) -> bool:
    return direction.upper() in {"LONG", "SHORT"}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return

    if not izin_var_mi(update.effective_user.id):
        await update.message.reply_text("❌ Yetkin yok!")
        return

    await update.message.reply_text(
        "🚀 **HOŞ GELDİN!**\n\n"
        "📊 Sinyal göndermek için:\n"
        "`/signal PARİTE YÖN GİRİŞ SL TP1 TP2 BORSA Açıklama`\n\n"
        "Yardım için: `/help`",
        parse_mode="Markdown",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return

    if not izin_var_mi(update.effective_user.id):
        await update.message.reply_text("❌ Yetkin yok!")
        return

    await update.message.reply_text(
        "📋 **KOMUTLAR**\n\n"
        "/start → Botu başlat\n"
        "/signal → Sinyal gönder\n"
        "/summary → Günlük özet gönder\n"
        "/help → Bu mesaj\n\n"
        "**Örnek:**\n"
        "`/signal BTCUSDT LONG 60000 59000 62000 63000 Binance Güçlü destek seviyesi`\n\n"
        "`/summary İşlem Sayısı TP SL ÖncekiBakiye ŞuankiBakiye Kâr`\n\n",
        parse_mode="Markdown",
    )


async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return

    user_id = update.effective_user.id
    if not izin_var_mi(user_id):
        await update.message.reply_text("❌ Yetkin yok!")
        return

    if len(context.args) < 6:
        await update.message.reply_text(
            "❌ Kullanım: `/summary İşlem Sayısı TP SL ÖncekiBakiye ŞuankiBakiye Kâr`",
            parse_mode="Markdown",
        )
        return

    islem, tp, sl, cash1, cash2, summary_text = context.args
    cash1 = normalize_number(cash1)
    cash2 = normalize_number(cash2)
    summary_text = normalize_number(summary_text)

    mesaj = f"""
👑**Bu günün Özeti**👑

📊**İşlem Sayısı:** `{islem}`
📈**TP sayısı:** `{tp}`
📉**SL sayısı:** `{sl}`
💵**Önceki Bakiye:** `{cash1}`$
💸**Şuanki Bakiye:** `{cash2}`$
🥳**Bu Günkü Kâr:** +`{summary_text}`$
""".strip()

    await context.bot.send_message(chat_id=CHANNEL_ID, text=mesaj, parse_mode="Markdown")
    await update.message.reply_text("✅ Summary kanala gönderildi!")


async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return

    user_id = update.effective_user.id
    if not izin_var_mi(user_id):
        await update.message.reply_text("❌ Yetkin yok!")
        return

    if len(context.args) < 8:
        await update.message.reply_text(
            "❌ Kullanım: `/signal PARİTE YÖN GİRİŞ SL TP1 TP2 BORSA Açıklama`",
            parse_mode="Markdown",
        )
        return

    parite, yon, giris, sl, tp1, tp2, borsa, *aciklama = context.args
    aciklama_text = " ".join(aciklama)

    if not validate_direction(yon):
        await update.message.reply_text("❌ Yön sadece LONG veya SHORT olabilir.")
        return

    giris = normalize_number(giris)
    sl = normalize_number(sl)
    tp1 = normalize_number(tp1)
    tp2 = normalize_number(tp2)

    mesaj = f"""
🚨 **YENİ SİNYAL** 🚨

📊 **Parite:** `{parite}`
📈 **Yön:** `{yon.upper()}`
🎯 **Giriş:** `{giris}`
🛑 **SL:** `{sl}`
💰 **TP1:** `{tp1}`
💰 **TP2:** `{tp2}`
🏦 **Borsa:** `{borsa} {aciklama_text}`

⚡ Fiyat giriş noktasına geldiğinde işlem aç!
""".strip()

    await context.bot.send_message(chat_id=CHANNEL_ID, text=mesaj, parse_mode="Markdown")
    await update.message.reply_text("✅ Sinyal kanala gönderildi!")


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    await update.message.reply_text(
        "❓ **Bilinmeyen komut!**\n"
        "Yardım için: `/help`",
        parse_mode="Markdown",
    )


async def set_commands(application: Application):
    await application.bot.set_my_commands(COMMANDS)


def main():
    if not TOKEN or not CHANNEL_ID:
        logger.error("HATA: TELEGRAM_BOT_TOKEN veya TELEGRAM_CHANNEL_ID eksik.")
        return

    if not IZINLI_KISILER:
        logger.error("HATA: ALLOWED_USER_IDS ayarı eksik veya geçersiz.")
        return

    app = Application.builder().token(TOKEN).post_init(set_commands).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("summary", summary))
    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    logger.info("Bot çalışıyor...")
    app.run_polling()


if __name__ == "__main__":
    main()
