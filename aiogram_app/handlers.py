from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
# Телеграм - библиотеки 
# Импорт состояний в Aiogram 3.1.1 (сложна) 

import aiohttp


# Подключение config-файла
from decouple import Config, RepositoryEnv
ENV_FILE = 'e.env'
config = Config(RepositoryEnv(ENV_FILE))

# Router - объект, описывающий команды
router = Router()

# Реакция на /start
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
"Запуск сообщения по команде /start. \n Commands: /create <IMYA> <FAMILIA> \n /read <ID> \n /update <ID> <IMYA> <FAMILIA>"
)

# Классы, чтобы усложнить реакцию
class Form1(StatesGroup):
    waiting_for_text = State()

class Form2(StatesGroup):
    waiting_for_text = State()

class Form3(StatesGroup):
    waiting_for_text = State()


# Реакция на /create
@router.message(Command('create'))
async def cmd_create(message: Message, state: FSMContext):
    await state.set_state(Form1.waiting_for_text)  # Устанавливаем состояние ожидания текста
    await message.reply("Введите запись, которую хотите создать:")


# Реакция после /create
@router.message()
async def process_text(message: Message, state: FSMContext):

 if await state.get_state() == str(Form1.waiting_for_text):
    words, params = message.text.split(" "), {"name": None, "surname": None, "birthday": None, "status": None}
    for i, param in enumerate(params.keys()):
        if words[i] != "-": params[key] = words[i]

    # Три строчки связи с API
    async with aiohttp.ClientSession() as session:
        async with session.post(config('API_ADDR'),params) as response:
            await message.answer(await response.json())
    await state.finish()

# Реакция на /read
@router.message(Command('read'))
async def cmd_read(message: Message, state: FSMContext):
    await state.set_state(Form2.waiting_for_text)   # Устанавливаем состояние ожидания текста
    await message.reply("Введите ID, которое хотите прочесть:")

# Реакция после /read
@router.message()
async def process_text(message: Message, state: FSMContext):

 if await state.get_state() == str(Form2.waiting_for_text):
    words, params = message.text.split(" "), {"page": None, "status": None}
    for i, param in enumerate(params.keys()):
        if words[i] != "-": params[key] = words[i]

    # Три строчки связи с API
    async with aiohttp.ClientSession() as session:
        async with session.get(config('API_ADDR')+'/'+params) as response:
            await message.answer(await response.json())
    await state.finish()

# Реакция на /update
@router.message(Command('update'))
async def cmd_update(message: Message, state: FSMContext):
    await state.set_state(Form3.waiting_for_text)   # Устанавливаем состояние ожидания текста
    await message.reply("Введите ID, которое хотите изменить с данными:")

# Реакция после /update
@router.message()
async def process_text(message: Message, state: FSMContext):

 if await state.get_state() == str(Form3.waiting_for_text):
    words, params = message.text.split(" "), {"id": None, "name": None, "surname": None, "birthday": None, "status": None}
    for i, param in enumerate(params.keys()):
        if words[i] != "-": params[key] = words[i]

    # Три строчки связи с API
    async with aiohttp.ClientSession() as session:
        async with session.put(config('API_ADDR'), params) as response:
            await message.answer(await response.json())
    await state.finish()
