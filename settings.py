from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Инициализируем приложение Flask
app = Flask(__name__, template_folder='templates')

# Создаем DSN для СУБД
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

# Обязательно для flask делать секретный ключ
app.secret_key = "werewrwrkfgjksdgjkkdfsfdsffs"

# Создаем объект для работы с SQLAlchemy
db = SQLAlchemy(app)
