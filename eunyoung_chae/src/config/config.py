import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("TEST_USER_EMAIL")
PW = os.getenv("TEST_USER_PW")