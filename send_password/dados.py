import os
from dotenv import load_dotenv

load_dotenv()
senha_smtp = str(os.getenv('senha_smtp'))
email_smtp = str(os.getenv('email_smtp'))