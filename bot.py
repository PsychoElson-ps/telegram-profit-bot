import asyncio
import random
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8790178667:AAH-wPrIwB5JoLvmfoN0RuE3jpyHZyletBo"

TARGET_CHAT_ID = -1003701424800   # ← замени на реальный после получения

# Списки для рандома
WORKERS = [
    "#драглирик", "#sunshine", "#malboros", "#aferist09", "#cr7men7ali7y",
    "#caratel", "#apxangel_ebawit", "#clou6y", "#душевнобольной", "#dopex",
    "#paranoic", "#в666ор95", "#xanax", "#gtruser", "#mellsher", "#soulmycry", "#jokke",
    "#playboy", "#phenix", "#астер", "#W1ZARD", "#shah", "#skymyname", "#royalty", "#royalty","#workout",
    "#антидиллер",  "#drainedgod", "#аристократ", "#лирика", "#ключиотиномарки", 
    "#vivien", "#goyard", "#Skipper", "#садuзм", "#Christopher", "#Amnesia", "#MoonLight", "#narkozavisem",
    "#lsd","#lover", "#tired", "#некрофос" "#axe", "#нахаслюнаиномарку", "#swaggawork", "#loyalty", "#shiper"
    "#тобоюболею", "#xMaDx", "#crul", "#avangard"
    # ... добавь остальные сам или позже
]

COUNTRIES = [
    "🇬🇧 Великобритания 🇬🇧",
    "🇸🇪 Швеция 🇸🇪",
    "🇨🇭 Швейцария 🇨🇭",
    "🇦🇪 ОАЭ 🇦🇪",
    "🇨🇦 Канада 🇨🇦",
    "🇳🇿 Новая Зеландия 🇳🇿",
    "🇭🇺 Венгрия 🇭🇺",
    "🇬🇷 Греция 🇬🇷",
    "🇧🇪 Бельгия 🇧🇪",
    "🇫🇷 Франция 🇫🇷",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот живой! Пока просто проверка.")

async def getid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Chat ID этого чата: {chat_id}")

async def post_profit(context: ContextTypes.DEFAULT_TYPE):
    worker = random.choice(WORKERS)
    
    # Доля воркера: смещение в сторону меньших сумм
    # 70% шанс < 1000, 20% 1000–1500, 10% >1500
    r = random.random()
    if r < 0.70:
        amount = random.uniform(60.99, 999.99)
    elif r < 0.90:
        amount = random.uniform(1000, 1499.99)
    else:
        amount = random.uniform(1500, 2000.99)
    
    dollars = f"{amount:.2f}$"
    
    country = random.choice(COUNTRIES)
    
    text = (
        "НОВЫЙ ПРОФИТ\n\n"
        f"Воркер: {worker}\n"
        f"Доля воркера: {dollars}\n"
        f"Страна: {country}\n\n"
        "За выводом к MORPH[](https://t.me/decimate_admin)"
    )
    
    try:
        await context.bot.send_message(
            chat_id=TARGET_CHAT_ID,
            text=text,
            disable_web_page_preview=True
        )
        print(f"[{datetime.now()}] Сообщение отправлено: {worker} | {dollars}")
    except Exception as e:
        print(f"Ошибка отправки: {e}")

async def schedule_posts(context: ContextTypes.DEFAULT_TYPE):
    # Запускаем первый пост через 1–10 минут после старта
    delay = random.randint(60, 600)
    context.job_queue.run_once(post_profit, delay, name="first_post")
    
    # Затем каждые 30–180 минут
    while True:
        interval = random.randint(1800, 10800)  # 30 мин – 3 часа в секундах
        await asyncio.sleep(interval)
        await post_profit(context)

def main():
    app = (
    Application.builder()
    .token(TOKEN)
    .get_updates_read_timeout(30.0)     # таймаут чтения обновлений (было read_timeout)
    .get_updates_write_timeout(30.0)    # таймаут записи
    .get_updates_connect_timeout(30.0)  # таймаут соединения
    .get_updates_pool_timeout(30.0)     # таймаут пула
    .build()
)

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("getid", getid))

    # Запускаем фоновую задачу расписания
    app.job_queue.run_once(schedule_posts, 5, name="scheduler_starter")

    print("Бот запущен... (нажми Ctrl+C чтобы остановить)")
    app.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
        timeout=30.0,
        bootstrap_retries=-1
    )

if __name__ == '__main__':
    main()