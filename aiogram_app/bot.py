from handlers import router

from aiogram import Bot, Dispatcher,types 
from aiogram.fsm.storage.memory import MemoryStorage
# Телеграм - библиотека

from decouple import Config, RepositoryEnv
ENV_FILE = 'e.env'
config = Config(RepositoryEnv(ENV_FILE))
# Подключение config-файла

async def main():

 bot = Bot(token=config('TOKEN'))
 commands = [
        types.BotCommand(command='/start', description='Начать взаимодействие с ботом'),
        types.BotCommand(command='/create', description='Запись данных'),
        types.BotCommand(command='/read', description='Чтение данных'),
    ]
 await bot.set_my_commands(commands)
 # Бот + подсказки

 dp = Dispatcher(storage=MemoryStorage()) # Объект обработки сообщений

 # Основной процесс
 dp.include_router(router)
 await bot.delete_webhook(drop_pending_updates=True)
 await dp.start_polling(bot)
