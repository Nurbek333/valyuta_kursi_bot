from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

currency_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=" 🇺🇸 Dollar", callback_data="usd"),
         InlineKeyboardButton(text=" 🇪🇺 Euro", callback_data="eur"),
         InlineKeyboardButton(text=" 🇷🇺 Rubl", callback_data="rub")],
        [InlineKeyboardButton(text=" 🇨🇳 Yuan", callback_data="cny"),
         InlineKeyboardButton(text=" 🇹🇲 Manat", callback_data="tmt"),
         InlineKeyboardButton(text=" 🇦🇪 Dirxam", callback_data="aed")],
        [InlineKeyboardButton(text=" 🇬🇧 Pound", callback_data="gbp"),
         InlineKeyboardButton(text=" 🇯🇵 Yen", callback_data="jpy"),
         InlineKeyboardButton(text=" 🇰🇷 Won", callback_data="krw")],
        [InlineKeyboardButton(text=" 🇸🇦 Riyal", callback_data="sar"),
         InlineKeyboardButton(text=" 🇨🇭 Frank", callback_data="chf"),
         InlineKeyboardButton(text=" 🇲🇾 Ringgit", callback_data="myr")],
        [InlineKeyboardButton(text=" 🇲🇽 Peso", callback_data="mxn"),
         InlineKeyboardButton(text=" 🇩🇰 Krone", callback_data="dkk"),
         InlineKeyboardButton(text=" 🇺🇦 Hryvnia", callback_data="uah")],
        [InlineKeyboardButton(text=" 🇵🇱 Zloty", callback_data="pln"),
         InlineKeyboardButton(text=" 🇮🇸 Krona", callback_data="isk"),
         InlineKeyboardButton(text=" 🇹🇷 Lira", callback_data="try")],
        [InlineKeyboardButton(text=" 🇰🇼 Dinar", callback_data="kwd"),
         InlineKeyboardButton(text=" 🇧🇩 Taka", callback_data="bdt"),
         InlineKeyboardButton(text=" 🇮🇩 Rupiah", callback_data="idr")],
        [InlineKeyboardButton(text=" 🇮🇱 Shekel", callback_data="ils"),
         InlineKeyboardButton(text=" 🇧🇬 Lev", callback_data="bgn")]
    ]
)

# Ortga tugmasi alohida
back_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Ortga", callback_data="back")]
    ]
)

# Yuqoridagi tugmalarni birga ishlatish uchun
def create_currency_keyboard():
    return currency_buttons.add(InlineKeyboardButton(text="🔙 Ortga", callback_data="back"))
    
