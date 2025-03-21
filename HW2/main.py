import random
import string
from flask import Flask

app = Flask(__name__)


@app.route('/generate_password')
def generate_password():

    # http://127.0.0.1:5000/generate_password

    characters = string.ascii_letters + string.digits + string.punctuation

    length = random.randint(10, 20)

    while True:
        password = ''.join(random.choice(characters) for _ in range(length))


        if all([
            len(password) == length,
            any(c.islower() for c in password),
            any(c.isupper() for c in password),
            any(c.isdigit() for c in password),
            any(c in string.punctuation for c in password)
        ]):
            return f'<h1>Password - {password}</h1>'


@app.route('/calculate_average')
def calculate_average():

    # http://127.0.0.1:5000/calculate_average

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
