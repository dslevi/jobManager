import os

# Config file, put all your keys and passwords and whatnot in here
DB_URI = os.environ.get("DATABASE_URL", "sqlite:///jobManager.db")
SECRET_KEY = "this should be a secret"
UPLOADS_DEFAULT_DEST = "./static/"
