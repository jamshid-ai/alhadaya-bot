import logging
import phonenumbers
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

class Form(StatesGroup):
    problem = State()
    phone = State()
    name = State()

API_TOKEN = '5424762080:AAEN3Sgum5CG1hgSF9msxqwWXAuTAoTHzhM'
my_string_number = "+99890 123-45-67"
my_number = phonenumbers.parse(my_string_number)
print(my_number)
print(phonenumbers.is_possible_number(my_number))


button1 = types.KeyboardButton("🩺 Қандли диабет")
button2 = types.KeyboardButton("♨️ Ошқозон муаммоси")
button3 = types.KeyboardButton("🩸 Қон босими")
button4 = types.KeyboardButton("🚽 Қабзият муаммоси")

keyboard1 = types.ReplyKeyboardMarkup(keyboard=[[button1, button2],[button3, button4]],resize_keyboard=True, one_time_keyboard=True) #.add(button1).add(button2).add(button3).add(button4)

button7 = types.KeyboardButton("Telefon", request_contact=True)
keyboard2 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button7)
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage= MemoryStorage())
data = {
    'problem': '',
    'name': 'Doe',
    'telephone': 901234567,
    'username': 'username'
}

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):

    await message.reply("""Ассалому алайкум 😊! 	

"ALHADAYA" mahsulotlarimizga qiziqish bildirganingiz uchun rahmat!

Sizni qaysi muammo ko’proq bezovta qilyapti?""", reply_markup=keyboard1)



@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    print(message)

    if message.text == '📌 Юрак-қон томир касаллиги' or message.text == '📌 Қандли диабет' or message.text == '📌 Жинсий касалликлар' or message.text == '📌 Ошқозон хазм тизими' or message.text == '📌 Сурункали касалликлар' or message.text == '📌 Инфаркт ва инсульт касаллиги':
        data['problem'] = message.text
        print(data['problem'])
        await message.answer(f"Tushunarli malakali mutaxasislarimiz siz bilan bog’lanib {message.text} oid bepul konsultatsiya va “ALHADAYA”ning foydali hususiyatlari tog’risida batafsil  ma’lumot berishadi!")

        await message.answer('Telefon raqamingizni qoldiring!\n\nMasalan: +998 90 123-45-67', reply_markup=keyboard2)
        await Form.phone.set()


@dp.message_handler(state= Form.phone, content_types= types.ContentTypes.CONTACT)
async def get_telephone_number(message: types.Message, state: FSMContext):
    user_telephone_num= message.contact.phone_number
    await message.reply(f"Your phone number: {user_telephone_num}")
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp)