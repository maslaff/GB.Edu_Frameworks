"""
Создать форму для регистрации пользователей на сайте. 
Форма должна содержать поля "Имя", "Фамилия", "Email", 
"Пароль" и кнопку "Зарегистрироваться". 
При отправке формы данные должны сохраняться в базе 
данных, а пароль должен быть зашифрован.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=True, nullable=False)
