import random
import string
from flask import Flask

app = Flask(__name__)


@app.route('/generate_password')
def generate_password(length=20):
    characters = string.ascii_letters + string.digits + string.punctuation

    while True:
        password = ''.join(random.choice(characters) for _ in range(length))

        # Используем all() для проверки всех условий
        if all([
            len(password) == length,  # Проверка длины пароля
            any(c.islower() for c in password),  # Наличие хотя бы одной строчной буквы
            any(c.isupper() for c in password),  # Наличие хотя бы одной заглавной буквы
            any(c.isdigit() for c in password),  # Наличие хотя бы одной цифры
            any(c in string.punctuation for c in password)  # Наличие хотя бы одного знака препинания
        ]):
            return f'<h1>{password}</h1>'


@app.route('/calculate_average')
def calculate_average():
    with open('hw.csv', encoding='utf-8') as f:
        file = f.readlines()
        file = file[1:]

        total_student = 0
        total_height = 0
        total_width = 0

        for row in file:
            row_split = row.split(',')
            total_height += float(row_split[1])
            total_width += float(row_split[2])
            total_student += 1

        return f'<h1>Average height of students - {round(total_height / total_student, 2)}<br>Average width of students - {round(total_width / total_student, 2)}</h1>'


if __name__ == '__main__':
    app.run(debug=True)
