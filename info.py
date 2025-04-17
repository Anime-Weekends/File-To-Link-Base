import re
from os import environ, getenv

id_pattern = re.compile(r'^.\d+$')

# Bot information
SESSION = environ.get('SESSION', 'Webavbot')
API_ID = int(environ.get('API_ID', '28744454'))
API_HASH = environ.get('API_HASH', 'debd37cef0ad1a1ce45d0be8e8c3c5e7')
BOT_TOKEN = environ.get('BOT_TOKEN', "7563428770:AAE0Dnp4OsIfJNhqiy0cYwyPT2prowRaR1w")
BOT_USERNAME = environ.get("BOT_USERNAME", 'File_To_Links_xRobot')  # without @

# Admins, Channels & Users
BIN_CHANNEL = int(environ.get("BIN_CHANNEL", '-1002599144576'))  # channel for file streaming
LOG_CHANNEL = int(environ.get("LOG_CHANNEL", '-1002510861342'))  # user logs
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '6429532957 6266529037').split()]
OWNER_USERNAME = environ.get("OWNER_USERNAME", 'RexySama')  # without @

# Bot display pics (at least one required)
PICS = (environ.get("PICS", "https://i.ibb.co/hxqp9gQk/photo-2025-04-03-11-00-42-7489040182323183640.jpg https://i.ibb.co/rK42qL4w/photo-2025-04-03-11-48-19-7489052453044748316.jpg")).split()

# Support & Channel links
CHANNEL = environ.get('CHANNEL', 'https://t.me/EmitingStars_Botz')
SUPPORT = environ.get('SUPPORT', 'https://t.me/+HZuPVe0l-F1mM2Jl')

# File limit settings
ENABLE_LIMIT = environ.get("ENABLE_LIMIT", False)  # True or False
RATE_LIMIT_TIMEOUT = int(environ.get("RATE_LIMIT_TIMEOUT", "600"))  # in seconds (10 min)
MAX_FILES = int(environ.get("MAX_FILES", "10"))  # Max files per user

# Banned channels/groups
BANNED_CHANNELS = [int(x) if id_pattern.search(x) else x for x in environ.get('BANNED_CHANNELS', '-1002410513772').split()]
BAN_CHNL = [int(x) if id_pattern.search(x) else x for x in environ.get('BAN_CHNL', '-1002410513772').split()]
BAN_ALERT = environ.get('BAN_ALERT', '<b><blockquote>Yᴏᴜʀ ᴀʀᴇ ʙᴀɴɴᴇᴅ ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ. Cᴏɴᴛᴀᴄᴛ [ᴏᴡɴᴇʀ](https://telegram.me/RexySamq) ᴛᴏ ʀᴇsᴏʟᴠᴇ ᴛʜᴇ ɪssᴜᴇ!!</blockquote></b>')

# MongoDB
DATABASE_URI = environ.get('DATABASE_URI', "mongodb+srv://soulmovies37:FwHMGCpSMCnVVmhw@cluster0.uyokx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DATABASE_NAME = environ.get('DATABASE_NAME', "EmitingStarsFilesToLink")

# Force Sub settings
AUTH_PICS = environ.get('AUTH_PICS', 'https://i.ibb.co/ycvH92F8/photo-2025-04-01-10-56-55-7488297041311825924.jpg')
AUTH_CHANNELS = list(map(str, environ.get("AUTH_CHANNELS", "-1002410513772").split()))
AUTH_CHANNEL = int(environ.get('AUTH_CHANNEL', '-1002410513772'))  # << Required for plugins/avbot.py
FSUB = environ.get("FSUB", True)

# Port configuration
PORT = int(getenv('PORT', '2626'))
NO_PORT = bool(getenv('NO_PORT', False))

# Ping settings
PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))  # 20 minutes
SLEEP_THRESHOLD = int(getenv('SLEEP_THRESHOLD', '60'))

# Streaming config
BIND_ADDRESS = str(getenv('WEB_SERVER_BIND_ADDRESS', '0.0.0.0'))
WORKERS = int(getenv('WORKERS', '4'))
MULTI_CLIENT = False
name = str(environ.get('name', 'avbotz'))

# Platform-specific (Heroku or Koyeb)
APP_NAME = None
if 'DYNO' in environ:
    ON_HEROKU = True
    APP_NAME = str(getenv('APP_NAME'))
else:
    ON_HEROKU = False

FQDN = str(getenv('FQDN', BIND_ADDRESS)) if not ON_HEROKU or getenv('FQDN', '') else APP_NAME + '.herokuapp.com'
HAS_SSL = bool(getenv('HAS_SSL', False))

if HAS_SSL:
    URL = "massive-davine-filestolinks-e43eee39.koyeb.app/"
else:
    URL = "massive-davine-filestolinks-e43eee39.koyeb.app/" if NO_PORT else f"http://cheerful-kimberlee-filetolink1286-a70f100b.koyeb.app:{PORT}"
