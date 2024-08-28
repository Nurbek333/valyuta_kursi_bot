import logging
import sys
import asyncio
import time
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from data import config
from menucommands.set_bot_commands import set_default_commands
from baza.sqlite import Database
from filters.admin import IsBotAdminFilter
from filters.check_sub_channel import IsCheckSubChannels
from states.reklama import Adverts
from keyboard_buttons import admin_keyboard
from keyboard import keyboard
from inline import currency_buttons, back_button
from api import get_crypto_prices
from baza.sqlite import Database
import sqlite3
from datetime import datetime
# from grafics import plot_historical_prices
from aiogram.types import InputFile
from davlat import get_currency_rate
ADMINS = config.ADMINS
TOKEN = config.BOT_TOKEN
CHANNELS = config.CHANNELS
is_bot_active = True
dp = Dispatcher(storage=MemoryStorage())
db = Database()



# @dp.message(F)
# async def photo_id(message: Message):
#     photo = message.photo[-1].file_id
#     print(photo)
#     await message.answer_photo(photo)

async def send_price_updates():
    while True:
        try:
            prices = get_crypto_prices()
            last_prices = db.get_last_prices()
            message = """
            📈 <b>Valyuta narxlaridagi o'zgarishlar:</b>\n
            """
            
            for symbol, data in prices.items():
                current_price = data['USD']
                previous_price = last_prices.get(symbol)
                
                if previous_price is None or previous_price != current_price:
                    price_diff = current_price - previous_price if previous_price else 0
                    change_symbol = "🔼" if price_diff > 0 else "🔽"
                    change_message = f"{change_symbol} {abs(price_diff):.2f} USD" if previous_price else ""
                    
                    message += f"💰 <b>{symbol}</b>: {current_price} USD {change_message}\n\n"
                    db.update_price(symbol, current_price)
            
            # Agar yangi ma'lumotlar bo'lsa, xabar yuboriladi
            if message != "📈 <b>Valyuta narxlaridagi o'zgarishlar:</b>\n":
                users = db.all_users_id()
                for user_id, in users:
                    await bot.send_message(user_id, message, parse_mode='HTML')
                    
        except Exception as e:
            print(f"Xato: {e}")
        
        await asyncio.sleep(86400)  # 24 soat kutish


@dp.message(CommandStart())
async def start_command(message: Message):
    full_name = message.from_user.full_name
    telegram_id = message.from_user.id
    try:
        if is_bot_active:
            # Bot ishlayotgan holatda
            db.add_user(full_name=full_name, telegram_id=telegram_id)  # Add user to the database
            await message.answer(text="""👋 **Salom! Xush kelibsiz!**

🌟 Bizning botimiz orqali siz quyidagi xizmatlardan foydalanishingiz mumkin:

1. **💵 Valyutalar** - Turli valyutalar bo'yicha ma'lumotlarni oling.
2. **🌍 Davlatlar haqida** - Davlatlar haqida qiziqarli ma'lumotlarni bilib oling.
3. **🌐 Bot tilini uzgartirish** - Bot tilini o'zgartiring.
4. **📊 Bot statistikasi** - Botning statistikasini ko'ring.

🔄 Agar siz orqaga qaytmoqchi bo'lsangiz, **Ortga** tugmasini bosing.

📝 Har qanday savollaringiz bo'lsa, **Yordam** tugmasini bosing yoki biz bilan bog'laning.

🎨 Bizning botimizni sinab ko'ring va uning imkoniyatlaridan foydalaning!

Yordam va qo'llanma uchun **/help** komandasi mavjud.

🌟 Yaxshi kun tilaymiz!

""", parse_mode="Markdown", reply_markup=keyboard)
        else:
            # Bot ishlamayotgan holatda
            await message.answer(text="""🛠️ Ta'mirlash: Bot ta'mirlash yoki xizmat ko'rsatish holatida. Iltimos, keyinroq qaytib ko'ring.""", parse_mode="Markdown")

    except Exception as e:
        if is_bot_active:
            # Xatolik yuzaga kelgan holatda bot ishlayotgan holatda
            await message.answer(text="""👋 **Salom! Xush kelibsiz!**

🌟 Bizning botimiz orqali siz quyidagi xizmatlardan foydalanishingiz mumkin:

1. **💵 Valyutalar** - Turli valyutalar bo'yicha ma'lumotlarni oling.
2. **🌍 Davlatlar haqida** - Davlatlar haqida qiziqarli ma'lumotlarni bilib oling.
3. **🌐 Bot tilini uzgartirish** - Bot tilini o'zgartiring.
4. **📊 Bot statistikasi** - Botning statistikasini ko'ring.

🔄 Agar siz orqaga qaytmoqchi bo'lsangiz, **Ortga** tugmasini bosing.

📝 Har qanday savollaringiz bo'lsa, **Yordam** tugmasini bosing yoki biz bilan bog'laning.

🎨 Bizning botimizni sinab ko'ring va uning imkoniyatlaridan foydalaning!

Yordam va qo'llanma uchun **/help** komandasi mavjud.

🌟 Yaxshi kun tilaymiz!

""", parse_mode="Markdown", reply_markup=keyboard)
        else:
            # Xatolik yuzaga kelgan holatda bot ishlamayotgan holatda
            await message.answer(text="""🛠️ **Ta'mirlash:** Bot ta'mirlash yoki xizmat ko'rsatish holatida. Iltimos, keyinroq qaytib ko'ring.""", parse_mode="Markdown")


@dp.message(IsCheckSubChannels())
async def kanalga_obuna(message: Message):
    text = ""
    inline_channel = InlineKeyboardBuilder()
    for index, channel in enumerate(CHANNELS):
        ChatInviteLink = await bot.create_chat_invite_link(channel)
        inline_channel.add(InlineKeyboardButton(text=f"{index+1}-kanal", url=ChatInviteLink.invite_link))
    inline_channel.adjust(1, repeat=True)
    button = inline_channel.as_markup()
    await message.answer(f"{text} kanallarga a'zo bo'ling", reply_markup=button)

@dp.message(Command("help"))
async def help_commands(message: Message):
    await message.answer("""🆘 **Yordam bo'limi** 

🤖 Bizning botimiz sizga quyidagi yordamni taqdim etadi:

1. **💵 Valyutalar**: Turli valyutalar haqida ma'lumotlarni olish uchun **Valyutalar** tugmasini bosing.

2. **🌍 Davlatlar haqida**: Davlatlar haqida qiziqarli ma'lumotlarni bilib olish uchun **Davlatlar haqida** tugmasini bosing.

3. **🌐 Bot tilini uzgartirish**: Botning tilini o'zgartirish uchun **Bot tilini uzgartirish** tugmasini bosing.

4. **📊 Bot statistikasi**: Botning statistikasi va faoliyatini ko'rish uchun **Bot statistikasi** tugmasini bosing.

🔄 **Ortga** qaytish uchun tugmalar yordamida boshqarishingiz mumkin.

💡 **Qo'shimcha yordam yoki savollar** bo'lsa:
- **📧 Bog'lanish**: [Sizning email yoki ijtimoiy tarmoqlaringiz]
- **📣 Yangiliklar**: Bot yangiliklarini kuzatib boring.

📘 **Qo'llanma**: Bizning botimizni to'liq o'rganish uchun **/about** komandasi mavjud.

Har qanday yordam yoki savol uchun biz bilan bog'laning!

🌟 Yordam va qo'llanma uchun sizga yordam berishga tayyormiz!

""", parse_mode="Markdown")

@dp.message(Command("about"))
async def about_commands(message: Message):
    await message.answer("""📜 **About bo'limi**

👋 **Salom!** Bizning botimiz haqidagi asosiy ma'lumotlar:

**🔧 Bot Nomi**: [Bot nomi]
**🎯 Maqsad**: [Bot maqsadi, masalan, valyutalar bo'yicha ma'lumotlar taqdim etish, davlatlar haqida qiziqarli faktlarni taqdim etish]
**💼 Muallif**: [Sizning ismingiz yoki kompaniya nomi]

🔍 **Botning Imkoniyatlari:**
- **💵 Valyutalar**: Har xil valyutalar bo'yicha kurslar va ma'lumotlar.
- **🌍 Davlatlar haqida**: Davlatlar haqidagi qiziqarli ma'lumotlar.
- **🌐 Bot tilini uzgartirish**: Botning tilini o'zgartirish imkoniyati.
- **📊 Bot statistikasi**: Botning ishlash statistikasi va tahlili.

📩 **Bog'lanish**: Agar sizda qo'shimcha savollar yoki fikrlar bo'lsa, biz bilan bog'laning:
- **📧 Email**: [Sizning email]
- **🌐 Ijtimoiy tarmoqlar**: [Sizning ijtimoiy tarmoqlar profilingiz]

⚙️ **Qo'shimcha Ma'lumotlar:**
- **📘 Qo'llanma**: Botdan qanday foydalanishni o'rganish uchun **/help** komandasi mavjud.

🌟 Botimizdan foydalanayotganingiz uchun rahmat! Yordam va qo'llanmalar uchun biz doimo tayyormiz.

🔄 **Orqaga qaytish** uchun **Ortga** tugmasini bosing.

""", parse_mode="Markdown")

@dp.message(Command("admin"), IsBotAdminFilter(ADMINS))
async def is_admin(message: Message):
    await message.answer(text="Admin menu", reply_markup=admin_keyboard.admin_button)

@dp.message(F.text == "👥 Foydalanuvchilar soni", IsBotAdminFilter(ADMINS))
async def users_count(message: Message):
    counts = db.count_users()
    text = f"Botimizda {counts[0]} ta foydalanuvchi bor"
    await message.answer(text=text, parse_mode=ParseMode.HTML)

@dp.message(F.text == "📢 Reklama yuborish", IsBotAdminFilter(ADMINS))
async def advert_dp(message: Message, state: FSMContext):
    await state.set_state(Adverts.adverts)
    await message.answer(text="Reklama yuborishingiz mumkin!", parse_mode=ParseMode.HTML)

@dp.message(Adverts.adverts)
async def send_advert(message: Message, state: FSMContext):
    message_id = message.message_id
    from_chat_id = message.from_user.id
    users = db.all_users_id()
    count = 0
    for user in users:
        try:
            await bot.copy_message(chat_id=user[0], from_chat_id=from_chat_id, message_id=message_id)
            count += 1
        except Exception as e:
            logging.exception(f"Foydalanuvchiga reklama yuborishda xatolik: {user[0]}", e)
        time.sleep(0.01)
    
    await message.answer(f"Reklama {count} ta foydalanuvchiga yuborildi", parse_mode=ParseMode.HTML)
    await state.clear()

# <<< ------------------------------------------------------------------------------------------------------------------------------------------>>>

# <<< ------------------------------------------------------------------------------------------------------------------------------------------>>>

@dp.message(F.text == "🌍 Davlat Valyutalari kursi")
async def location_exit(message:Message):
    # Saqlanadigan xabarni yuborish
    photo = "https://telegra.ph/file/e8e2976230063c92f0b4a.jpg"
    await message.answer_photo(photo=photo,
       caption="<b>Siz qaysi valyuta bo'yicha bilmoqchi bulsangiz usha valyuta ustiga bosib bilib olishingiz mumkin! Bu yerda 24 xil valyular haqida malumotlar bor.</b>", 
        reply_markup=currency_buttons, 
        parse_mode="HTML"
    )
    


# Callback funksiyalari
@dp.callback_query(F.data == "usd")
async def usd_kurs(callback: CallbackQuery):
    rate = get_currency_rate("USD")
    await callback.message.answer(
        f"🇺🇸 Dollar: 1 USD = {rate} UZS",
        reply_markup=back_button
    )
    await callback.message.delete()

@dp.callback_query(F.data == "eur")
async def eur_kurs(callback: CallbackQuery):
    rate = get_currency_rate("EUR")
    await callback.message.answer(
        f"🇪🇺 Euro: 1 EUR = {rate} UZS",
        reply_markup=back_button
    )
    await callback.message.delete()

@dp.callback_query(F.data == "rub")
async def rub_kurs(callback: CallbackQuery):
    rate = get_currency_rate("RUB")
    await callback.message.answer(
        f"🇷🇺 Rubl: 1 RUB = {rate} UZS",
        reply_markup=back_button
    )
    await callback.message.delete()

@dp.callback_query(F.data == "cny")
async def cny_kurs(callback: CallbackQuery):
    rate = get_currency_rate("CNY")
    await callback.message.answer(
        f"🇨🇳 Yuan: 1 CNY = {rate} UZS",
        reply_markup=back_button
    )
    await callback.message.delete()

@dp.callback_query(F.data == "tmt")
async def tmt_kurs(callback: CallbackQuery):
    rate = get_currency_rate("TMT")
    await callback.message.answer(
        f"🇹🇲 Manat: 1 TMT = {rate} UZS",
        reply_markup=back_button
    )
    await callback.message.delete()

@dp.callback_query(F.data == "aed")
async def aed_kurs(callback: CallbackQuery):
    rate = get_currency_rate("AED")
    await callback.message.answer(
        f"🇦🇪 Dirxam: 1 AED = {rate} UZS",
        reply_markup=back_button
    )
    await callback.message.delete()

@dp.callback_query(F.data == "gbp")
async def gbp_kurs(callback: CallbackQuery):
    rate = get_currency_rate("GBP")
    await callback.message.answer(
        f"🇬🇧 Pound: 1 GBP = {rate} UZS",
        reply_markup=back_button
    )
    await callback.message.delete()

@dp.callback_query(F.data == "jpy")
async def jpy_kurs(callback: CallbackQuery):
    rate = get_currency_rate("JPY")
    await callback.message.answer(
        f"🇯🇵 Yen: 1 JPY = {rate} UZS",
        reply_markup=back_button
    )
    await callback.message.delete()

@dp.callback_query(F.data == "krw")
async def krw_kurs(callback: CallbackQuery):
    rate = get_currency_rate("KRW")
    await callback.message.answer(
        f"🇰🇷 Won: 1 KRW = {rate} UZS",
        reply_markup=back_button
    )
    await callback.message.delete()

@dp.callback_query(F.data == "sar")
async def sar_kurs(callback: CallbackQuery):
    rate = get_currency_rate("SAR")
    await callback.message.answer(
        f"🇸🇦 Riyal: 1 SAR = {rate} UZS",
        reply_markup=back_button
    )
    await callback.message.delete()

@dp.callback_query(F.data == "chf")
async def chf_kurs(callback: CallbackQuery):
    rate = get_currency_rate("CHF")
    await callback.message.answer(
        f"🇨🇭 Frank: 1 CHF = {rate} UZS",
        reply_markup=back_button
    )
    await callback.message.delete()

@dp.callback_query(F.data == "myr")
async def myr_kurs(callback: CallbackQuery):
    rate = get_currency_rate("MYR")
    await callback.message.answer(
        f"🇲🇾 Ringgit: 1 MYR = {rate} UZS",
        reply_markup=back_button
    )
    await callback.message.delete()

@dp.callback_query(F.data == "mxn")
async def mxn_kurs(callback: CallbackQuery):
    rate = get_currency_rate("MXN")
    await callback.message.answer(
        f"🇲🇽 Peso: 1 MXN = {rate} UZS",
        reply_markup=back_button
    )
    await callback.message.delete()

@dp.callback_query(F.data == "dkk")
async def dkk_kurs(callback: CallbackQuery):
    rate = get_currency_rate("DKK")
    await callback.message.answer(
        f"🇩🇰 Krone: 1 DKK = {rate} UZS",
        reply_markup=back_button
    )
    await callback.message.delete()

@dp.callback_query(F.data == "uah")
async def uah_kurs(callback: CallbackQuery):
    rate = get_currency_rate("UAH")
    await callback.message.answer(
        f"🇺🇦 Hryvnia: 1 UAH = {rate} UZS",
        reply_markup=back_button
    )
    await callback.message.delete()

@dp.callback_query(F.data == "pln")
async def pln_kurs(callback: CallbackQuery):
    rate = get_currency_rate("PLN")
    await callback.message.answer(
        f"🇵🇱 Zloty: 1 PLN = {rate} UZS",
        reply_markup=back_button
    )
    await callback.message.delete()

@dp.callback_query(F.data == "isk")
async def isk_kurs(callback: CallbackQuery):
    rate = get_currency_rate("ISK")
    await callback.message.answer(
        f"🇮🇸 Krona: 1 ISK = {rate} UZS",
        reply_markup=back_button
    )
    await callback.message.delete()

@dp.callback_query(F.data == "try")
async def try_kurs(callback: CallbackQuery):
    rate = get_currency_rate("TRY")
    await callback.message.answer(
        f"🇹🇷 Lira: 1 TRY = {rate} UZS",
        reply_markup=back_button
    )
    await callback.message.delete()

@dp.callback_query(F.data == "kwd")
async def kwd_kurs(callback: CallbackQuery):
    rate = get_currency_rate("KWD")
    await callback.message.answer(
        f"🇰🇼 Dinar: 1 KWD = {rate} UZS",
        reply_markup=back_button
    )
    await callback.message.delete()

@dp.callback_query(F.data == "bdt")
async def bdt_kurs(callback: CallbackQuery):
    rate = get_currency_rate("BDT")
    await callback.message.answer(
        f"🇧🇩 Taka: 1 BDT = {rate} UZS",
        reply_markup=back_button
    )
    await callback.message.delete()

@dp.callback_query(F.data == "idr")
async def idr_kurs(callback: CallbackQuery):
    rate = get_currency_rate("IDR")
    await callback.message.answer(
        f"🇮🇩 Rupiah: 1 IDR = {rate} UZS",
        reply_markup=back_button
    )
    await callback.message.delete()

@dp.callback_query(F.data == "ils")
async def ils_kurs(callback: CallbackQuery):
    rate = get_currency_rate("ILS")
    await callback.message.answer(
        f"🇮🇱 Shekel: 1 ILS = {rate} UZS",
        reply_markup=back_button
    )
    await callback.message.delete()

@dp.callback_query(F.data == "bgn")
async def bgn_kurs(callback: CallbackQuery):
    rate = get_currency_rate("BGN")
    await callback.message.answer(
        f"🇧🇬 Lev: 1 BGN = {rate} UZS",
        reply_markup=back_button
    )
    await callback.message.delete()


@dp.callback_query(F.data == "back")
async def process_callback_back(callback:CallbackQuery):
    # Oldingi xabarni qaytarish
    await callback.message.edit_text(
            "<b>Siz qaysi valyuta bo'yicha bilmoqchi bulsangiz usha valyuta ustiga bosib bilib olishingiz mumkin! Bu yerda 24 xil valyular haqida malumotlar bor.</b>",
        parse_mode="HTML"
    )
    # Tugmani qaytarish
    await callback.message.edit_reply_markup(reply_markup=currency_buttons)
# <<<<---------------------------------------------------------------------------------------------------------------------------------------->>>>

# "Krypto" tugmasi bosilganda
@dp.message(F.text == "💎 Kriptovalyutalar kursi")
async def send_crypto_prices(message: Message):
    prices = get_crypto_prices()
    photo = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQROWaSA_9Is9WevWZDRDl3apvNICPhDV6RYfHSNzitOPBav0Q_WwbrNtOh6Zm_mYg9IWc&usqp=CAU"
    response_message = (
        f"💰 Bitcoin (BTC): {prices['BTC']['USD']} USD\n\n"
        f"💎 Ethereum (ETH): {prices['ETH']['USD']} USD\n\n"
        f"🚀 Ripple (XRP): {prices['XRP']['USD']} USD\n\n"
        f"🔗 Litecoin (LTC): {prices['LTC']['USD']} USD\n\n"
        f"💸 Bitcoin Cash (BCH): {prices['BCH']['USD']} USD\n\n"
        f"🌟 Cardano (ADA): {prices['ADA']['USD']} USD\n\n"
        f"🔗 Polkadot (DOT): {prices['DOT']['USD']} USD\n\n"
        f"✨ Stellar (XLM): {prices['XLM']['USD']} USD\n\n"
        f"🔍 Chainlink (LINK): {prices['LINK']['USD']} USD\n\n"
        f"🐕 Dogecoin (DOGE): {prices['DOGE']['USD']} USD\n\n"
        f"📦 TONCoin (TON): {prices['TON']['USD']} USD\n\n"
        f"🧩 NotCoin (NOT): {prices['NOT']['USD']} USD\n\n"
        f"🔶 TRON (TRX): {prices['TRX']['USD']} USD\n\n"
        f"⚡ Solana (SOL): {prices['SOL']['USD']} USD\n\n"
        f"🔄 Uniswap (UNI): {prices['UNI']['USD']} USD\n\n"
        f"📊 Aave (AAVE): {prices['AAVE']['USD']} USD\n\n"
        f"🔷 Polygon (MATIC): {prices['MATIC']['USD']} USD\n\n"
        f"🔗 VeChain (VET): {prices['VET']['USD']} USD"
    )
    
    await message.answer_photo(photo=photo, caption=response_message, reply_markup=keyboard)


@dp.message(Command('stop'))
async def on_stop(message:Message):
    user_id = message.from_user.id
    db.remove_user(user_id)
    await message.answer("Valyuta narxlaridagi o'zgarishlar xabari yuborilmaydi.")



class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db
        self.create_table_bot_info()

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_bot_info(self):
        sql = """
        CREATE TABLE IF NOT EXISTS BotInfo(
        start_time TEXT
        );
        """
        self.execute(sql, commit=True)
        # Agar `BotInfo` jadvali bo'sh bo'lsa, botning ishga tushgan vaqtini qo'shing
        if not self.execute("SELECT * FROM BotInfo;", fetchone=True):
            self.execute("INSERT INTO BotInfo (start_time) VALUES (?);", parameters=(datetime.now().isoformat(),), commit=True)

    def get_bot_start_time(self):
        return self.execute("SELECT start_time FROM BotInfo;", fetchone=True)[0]

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

db = Database()

async def get_bot_statistics():
    total_users = db.count_users()[0]
    bot_start_time = db.get_bot_start_time()
    start_time = datetime.fromisoformat(bot_start_time)
    uptime = datetime.now() - start_time
    days_uptime = uptime.days
    
    # Uptime formatlash
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted_uptime = f"{days_uptime} kun, {hours} soat, {minutes} daqiqa, {seconds} soniya"
    
    error_count = 0  # Bu qiymatni haqiqiy xatoliklar bilan almashtiring

    return {
        "total_users": total_users,
        "error_count": error_count,
        "uptime": formatted_uptime,
        "days_uptime": days_uptime
    }

@dp.message(F.text == "📊 Bot statistikasini ko'rsatish")
async def show_bot_statistics(message: Message):
    stats = await get_bot_statistics()
    
    response = (
        f"👥 *Jami foydalanuvchilar:* {stats['total_users']}\n\n"
        f"⚠️ *Bot xatoliklari:* {stats['error_count']}\n\n"
        f"⏳ *Bot ishga tushgan vaqt:* {stats['uptime']}\n\n"
        f"📅 *Kunlar soni:* {stats['days_uptime']}"
    )
    
    # Rasmning URL manzili
    photo_url = "https://static3.tgstat.ru/channels/_0/7a/7a13404ed6199848a0dd561a94567e60.jpg"
    
    # Rasmni yuborish
    await message.answer_photo(photo=photo_url, caption=response, parse_mode='Markdown')


# <<< ------------------------------------------------------------------------------------------------------------------------------------------>>>
@dp.startup()
async def on_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=int(admin), text="✅ Bot ishga tushdi")
            asyncio.create_task(send_price_updates())
        except Exception as err:
            logging.exception(err)

@dp.shutdown()
async def off_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=int(admin), text="⚠️ Bot ishdan to'xtadi!")
        except Exception as err:
            logging.exception(err)

def setup_middlewares(dispatcher: Dispatcher, bot: Bot) -> None:
    from middlewares.throttling import ThrottlingMiddleware
    dispatcher.message.middleware(ThrottlingMiddleware(slow_mode_delay=0.5))

async def main() -> None:
    global bot, db
    bot = Bot(TOKEN)
    db = Database(path_to_db="main.db")
    await set_default_commands(bot)
    setup_middlewares(dispatcher=dp, bot=bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
