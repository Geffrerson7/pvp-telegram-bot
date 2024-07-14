import os
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.environ.get("TOKEN")
DEVELOPER_CHAT_ID = os.environ.get("DEVELOPER_CHAT_ID")
DEBUG = os.environ.get("DEBUG")
BOTHOST = os.environ.get("BOTHOST")
ADMIN = os.environ.get("ADMIN")
SUPPORT = os.environ.get("SUPPORT")
CHAT_ID = os.environ.get("CHAT_ID")
PERIOD = os.environ.get("PERIOD")
USER_1 = os.environ.get("USER_1")
USER_2 = os.environ.get("USER_2")
USER_3 = os.environ.get("USER_3")
MESSAGE_THREAD_ID = os.environ.get("MESSAGE_THREAD_ID")