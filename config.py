import re, os

id_pattern = re.compile(r'^.\d+$') 

API_ID = os.environ.get("API_ID", "23265307")

API_HASH = os.environ.get("API_HASH", "cc2b82ee80cabeba9a3408a6972d0ab2")

BOT_TOKEN = os.environ.get("BOT_TOKEN", "7183574921:AAG3RYF4JFMgNwhwUWNprqIFwNLqPoo9oW8") 

FORCE_SUB = os.environ.get("FORCE_SUB", "LazyDeveloper") 

DB_NAME = os.environ.get("DB_NAME","Cluster0")     

DB_URL = os.environ.get("DB_URL","mongodb+srv://lazytest:lazytest@cluster0.a0s61.mongodb.net/?retryWrites=true&w=majority")

FLOOD = int(os.environ.get("FLOOD", "10"))

START_PIC = os.environ.get("START_PIC", "https://i.ibb.co/NHdvRwk/missdevil.jpg")

ADMIN = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '5965340120 6126812037').split()]

# Bot_Username = "@LazyPrincessXBOT"
BOT_USERNAME = os.environ.get("BOT_USERNAME", "@MissDevil_RoBoT")
MAX_ACTIVE_TASKS = int(os.environ.get("MAX_ACTIVE_TASKS", "5"))
MAX_FORWARD = int(os.environ.get("MAX_FORWARD", "20"))
OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "LazyDeveloper")
PORT = os.environ.get('PORT', '8080')

Lazy_session = {}
Lazy_api_id ={}
Lazy_api_hash ={}

String_Session  = "None"

Permanent_4gb = "-100XXX"
