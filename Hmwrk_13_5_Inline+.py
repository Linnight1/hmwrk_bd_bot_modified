import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import crud_functions
import botik
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text="Рассчитать")
button2 = KeyboardButton(text="Купить")
button_reg = KeyboardButton(text="Регистрация")
kb.row(button, button2, button_reg)

api = "5412904149:AAGXoOUqrWssdivh_vpHqVINY1jA1bYxYD8"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb_2 = InlineKeyboardMarkup()
button3 = InlineKeyboardButton(text="Рассчитать норму калорий", callback_data='calories')
button4 = InlineKeyboardButton(text="Формулы расчета", callback_data='formulas')
kb_2.row(button3, button4)
catalog_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Product1", callback_data="product_buying")],
        [InlineKeyboardButton(text="Product2", callback_data="product_buying")],
        [InlineKeyboardButton(text="Product3", callback_data="product_buying")],
        [InlineKeyboardButton(text="Product4", callback_data="product_buying")]
    ]
)
class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = 1000

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
@dp.message_handler(commands=["start"])
async def start(message):
    await message.answer("Привет! Я бот, помогающий твоему здоровью.", reply_markup=kb)
@dp.message_handler(text=["Купить"])
async def get_buying_list(message):
    with open("../Lib/Bot/img1.jpg", "rb") as img:
        await message.answer_photo(img, crud_functions.get_all_products(1))
    with open("../Lib/Bot/img2.jpg", "rb") as img:
        await message.answer_photo(img, crud_functions.get_all_products(2))
    with open("../Lib/Bot/img3.jpg", "rb") as img:
        await message.answer_photo(img, crud_functions.get_all_products(3))
    with open("../Lib/Bot/img4.jpg", "rb") as img:
        await message.answer_photo(img, crud_functions.get_all_products(4), reply_markup=catalog_kb)

@dp.message_handler(text="Регистрация")
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()
@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    await message.answer("Введите имя пользователя (только латинский алфавит):")

    if crud_functions.is_included(message.text) == True:
        # state = message.text
        await state.update_data(first=message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()
    else:
        await message.answer("Пользователь существует, введите другое имя")
        await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    # state = message.text
    await state.update_data(second=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    # state = message.text
    await state.update_data(third=message.text)
    data = await state.get_data()
    crud_functions.add_user(data['first'], data['second'], data['third'])
    await message.answer("Регистрация успешно пройдена.", reply_markup=catalog_kb)
    await state.finish()


@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer("Введите свой возраст")
    await UserState.age.set()
@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(first=message.text)
    await message.answer("Введите свой рост")
    await UserState.growth.set()
@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(second=message.text)
    await message.answer("Введите свой вес")
    await UserState.weight.set()
@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(third=message.text)
    data = await state.get_data()
    await message.answer(f"Ваша норма калорий: {float(data['third']) * 10 + 6.25 * float(data['second']) - 5 * float(data['first']) - 161}")
    await state.finish()
@dp.message_handler(text="Рассчитать")
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb_2)
@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer("10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161")
    await call.answer()
@dp.callback_query_handler(text=['product_buying'])
async def send_confirm_message(call):
    await call.message.answer("Вы успешно купили продукт!")
    await call.answer()




if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)