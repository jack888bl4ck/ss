import logging
import json
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from fastapi import FastAPI, Request

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
WEB_APP_URL = "https://your-vps-ip-or-domain/webapp/"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Webhook API (FastAPI)
app = FastAPI()

@app.post("/order_update")
async def order_update(request: Request):
    data = await request.json()
    order_id = data.get("order_id")
    status = data.get("status")
    user_id = data.get("user_id")

    status_messages = {
        "accepted": "🚀 Your order has been accepted!",
        "on_the_way": "🚗 Your order is on the way!",
        "arrived": "📍 Your driver has arrived!",
        "delivered": "✅ Your order has been delivered!"
    }
    
    if status in status_messages:
        await bot.send_message(user_id, status_messages[status])

    return {"status": "ok"}

# Start Command with Web App Button
@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Open Shop", web_app=WebAppInfo(url=WEB_APP_URL)),
        InlineKeyboardButton("Play Roulette", callback_data="roulette"),
        InlineKeyboardButton("Referral Leaderboard", web_app=WebAppInfo(url=WEB_APP_URL + "leaderboard.html"))
    )
    await message.answer("Welcome to Smokey Malones!", reply_markup=keyboard)

# Roulette Game
@dp.callback_query_handler(lambda call: call.data == "roulette")
async def roulette_game(call: types.CallbackQuery):
    user_id = call.from_user.id
    number = random.randint(1, 100)
    
    if number == 1:
        await bot.send_message(user_id, "🎉 You won €50 store credit!")
    else:
        await bot.send_message(user_id, "❌ You lost! Try again!")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
        