import asyncio
from aiogram import Bot, types
API_TOKEN='5424762080:AAEN3Sgum5CG1hgSF9msxqwWXAuTAoTHzhM'
CHANNEL_ID=-1001192810784
 # it must be int, for example -1006666666666
bot= Bot(token= API_TOKEN, parse_mode=types.ParseMode.HTML)
async def send_message(channel_id: int, text: str):
    await bot.send_message(channel_id, text)
async def main():
    await send_message(CHANNEL_ID, '&lt;b &gt;Hello! &lt;/b &gt;')
if __name__== '__main__':
    asyncio.run (main())







# import logging

# import aiogram.utils.markdown as md
# from aiogram import Bot, Dispatcher, types
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters import Text
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.types import ParseMode
# from aiogram.utils import executor

# logging.basicConfig(level=logging.INFO)
# API_TOKEN = '5424762080:AAEN3Sgum5CG1hgSF9msxqwWXAuTAoTHzhM'


# bot = Bot(token=API_TOKEN)

# # For example use simple MemoryStorage for Dispatcher.
# storage = MemoryStorage()
# dp = Dispatcher(bot, storage=storage)


# # States
# class Form(StatesGroup):
#     name = State()  # Will be represented in storage as 'Form:name'
#     age = State()  # Will be represented in storage as 'Form:age'
#     gender = State()  # Will be represented in storage as 'Form:gender'


# @dp.message_handler(commands='start')
# async def cmd_start(message: types.Message):
#     """
#     Conversation's entry point
#     """
#     # Set state
#     await Form.name.set()

#     await message.reply(f"""Ассалому алайкум 😊
# ⚜️ {md.bold('ALHADAYA')} маҳсулотларимизга қизиқиш билдирганингиз учун рахмат!""")


# # You can use state '*' if you need to handle all states
# @dp.message_handler(state='*', commands='cancel')
# @dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
# async def cancel_handler(message: types.Message, state: FSMContext):
#     """
#     Allow user to cancel any action
#     """
#     current_state = await state.get_state()
#     if current_state is None:
#         return

#     logging.info('Cancelling state %r', current_state)
#     # Cancel state and inform user about it
#     await state.finish()
#     # And remove keyboard (just in case)
#     await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


# @dp.message_handler(state=Form.name)
# async def process_name(message: types.Message, state: FSMContext):
#     """
#     Process user name
#     """
#     async with state.proxy() as data:
#         data['name'] = message.text

#     await Form.next()
#     await message.reply("How old are you?")


# # Check age. Age gotta be digit
# @dp.message_handler(lambda message: not message.text.isdigit(), state=Form.age)
# async def process_age_invalid(message: types.Message):
#     """
#     If age is invalid
#     """
#     return await message.reply("Age gotta be a number.\nHow old are you? (digits only)")


# @dp.message_handler(lambda message: message.text.isdigit(), state=Form.age)
# async def process_age(message: types.Message, state: FSMContext):
#     # Update state and data
#     await Form.next()
#     await state.update_data(age=int(message.text))

#     # Configure ReplyKeyboardMarkup
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
#     markup.add("Male", "Female")
#     markup.add("Other")

#     await message.reply("What is your gender?", reply_markup=markup)


# @dp.message_handler(lambda message: message.text not in ["Male", "Female", "Other"], state=Form.gender)
# async def process_gender_invalid(message: types.Message):
#     """
#     In this example gender has to be one of: Male, Female, Other.
#     """
#     return await message.reply("Bad gender name. Choose your gender from the keyboard.")

# @dp.message_handler(state=Form.gender)
# async def process_gender(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['gender'] = message.text

#         # Remove keyboard
#         markup = types.ReplyKeyboardRemove()
#         print(data)
#         # And send message
#         await bot.send_message(
#             message.chat.id,
#             md.text(
#                 md.text('Hi! Nice to meet you,', md.bold(data['name'])),
#                 md.text('Age:', md.code(data['age'])),
#                 md.text('Gender:', data['gender']),
#                 sep='\n',
#             ),
#             reply_markup=markup,
#             parse_mode=ParseMode.MARKDOWN,
#         )

#     # Finish conversation
#     await state.finish()


# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)

