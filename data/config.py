from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()


# Telegram Bot
BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
CHANNEL_ID = env.int("CHANNEL_ID")


# Qiwi
QIWI_P2P_TOKEN = env.str("QIWI_P2P_TOKEN")
QIWI_TOKEN = env.str("QIWI_TOKEN")
QIWI_NUMBER = env.str("QIWI_NUMBER")