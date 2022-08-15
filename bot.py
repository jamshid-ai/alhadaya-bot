import logging
import re
import os
from dotenv import load_dotenv

load_dotenv()

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor


logging.basicConfig(level=logging.INFO)
API_TOKEN = os.getenv('API_TOKEN')
CHANNEL_ID=os.getenv('CHANNEL_ID')
bot = Bot(token=API_TOKEN)

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# States
class Form(StatesGroup):
    problem = State()  # Will be represented in storage as 'Form:name'
    phone = State()  # Will be represented in storage as 'Form:age'
    # gender = State()
    name = State()  # Will be represented in storage as 'Form:gender'

# to send channel
async def send_message(channel_id: int, text: str):
    await bot.send_message(channel_id, text)

leed_data = {
    'problem': 'problem',
    'phone': 'phone',
    'name': 'name',
    'username': ''
}

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    """
    Conversation's entry point
    """

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("🩺 Қандли диабет", "♨️ Ошқозон муаммоси")
    markup.add("🩸 Қон босими", "🚽 Қабзият муаммоси")

    # Set state
    await Form.problem.set()

    await bot.send_message(message.chat.id, text=f"""Ассалому алайкум 😊
⚜️ *ALHADAYA* маҳсулотларимизга қизиқиш билдирганингиз учун рахмат!""", parse_mode=ParseMode.MARKDOWN)
    await bot.send_message(message.chat.id, text="👩‍⚕️ *Сизни қайси муаммо кўпроқ безовта қиляпти?*👇", reply_markup=markup, parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(state=Form.problem)
async def process_name(message: types.Message, state: FSMContext):
    """
    Process user name
    """
    async with state.proxy() as data:
        data['problem'] = message.text
        leed_data['problem'] = message.text


    markup = types.ReplyKeyboardRemove()
    await Form.next()
    await bot.send_message(message.chat.id, text=f"👩‍⚕️ Тушунарли малакали мутахассисларимиз сиз билан боғланиб *{message.text}*га оид *БЕПУЛ* консультация ва ⚜️ *ALHADAYA*нинг фойдали хусусиятлари тўғрисида батафсил маълумот беришади 😊""", parse_mode=ParseMode.MARKDOWN)
    await bot.send_message(message.chat.id, text="""☺️ *Илтимос рақамингизни қолдиринг!*

Масалан: +998-90-123-45-67""", reply_markup=markup, parse_mode=ParseMode.MARKDOWN)

Pattern = re.compile("(0|91)?[3-9][0-9]{7}")
# validate phone number
@dp.message_handler(lambda message: not Pattern.match(message.text), state=Form.phone)
async def process_phone_invalid(message: types.Message):
    """
    If age is invalid
    """
    return await message.reply("Нотўғри рақам киритдингиз, қайтадан киритинг!")

@dp.message_handler(lambda message: Pattern.match(message.text), state=Form.phone)
async def process_phone(message: types.Message, state: FSMContext):
    # Update state and data
    await Form.next()
    await state.update_data(phone=message.text)
    async with state.proxy() as data:
        leed_data['phone'] = data['phone']
        

    await bot.send_message(message.chat.id, text="👤 *Исмингизни ҳам киритинг:*", parse_mode=ParseMode.MARKDOWN)
    

@dp.message_handler(lambda message: message.text in [], state=Form.name)
async def process_gender_invalid(message: types.Message):
    """
    In this example gender has to be one of: Male, Female, Other.
    """
    return await message.reply("Bad gender name. Choose your gender from the keyboard.")

@dp.message_handler(state=Form.name)
async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        leed_data['name'] = message.text
        leed_data['username'] = message.from_user.username

        
        await bot.send_message(
            message.chat.id, 
            text=f"""🎉 Табриклаймиз *{data['name']}* сиз *БЕПУЛ* консултацияга эга бўлдингиз. Тез орада сиз билан малакали мутахасиссимиз боғланади!

🧑‍💻 Қўшимча саволлар учун: *@Al_hadaya_3*""",
            parse_mode=ParseMode.MARKDOWN,
            
        )
        # await SendMessage(chat_id='@jamshid_files', text='Some content')
        await send_message(CHANNEL_ID, f"""Muammosi: {leed_data['problem']}
Ismi: {leed_data['name']}
Raqam: {leed_data['phone']}
Account: @{leed_data['username']}""")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)