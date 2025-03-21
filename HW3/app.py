from flask import Flask, render_template_string, request
from faker import Faker
import csv
import requests as rqvsts
from http import HTTPStatus
from webargs import fields, validate
from webargs.flaskparser import use_args

app = Flask(__name__)
faker = Faker()

# dictionary validate parameters
user_args = {
    'quality': fields.Int(validate=validate.Range(min=1, max=1000), load_default=1),
    'currency': fields.Str(validate=validate.Length(min=3), load_default='USD'),
    'convert': fields.Int(validate=validate.Range(min=1), load_default=1)
}


@app.route('/generate_students')
@use_args(user_args, location='query')  # accepts validated parameters dictionary, location
def generate_students(args):

    # http://127.0.0.1:5000/generate_students?quality=100

    list_students = []

    # Generate list of students
    for _ in range(int(args['quality'])):
        first_name = faker.first_name()
        last_name = faker.last_name()
        email = faker.email(domain='gmail.com')
        password = faker.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
        birthday = faker.date_of_birth(minimum_age=18, maximum_age=60)
        student = [first_name, last_name, email, password, birthday]
        list_students.append(student)

    # Save list of students to CSV file
    with open('students.csv', 'w', newline='') as file:
        headers = ['first_name', 'last_name', 'email', 'password', 'birthday']
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(list_students)

    template = '''<h3>List of {{ students | length }} students:</h3>
        <ol>
            {% for student in students %}
                <li>{{ student | join(' ') }}</li>
            {% endfor %}
        </ol>
        '''

    return render_template_string(template, students=list_students)


@app.route('/bitcoin_rate')
@use_args(user_args, location='query')
def bitcoin_rate(args):

    # http://127.0.0.1:5000/bitcoin_rate?currency=UAH&convert=100

    currency = args['currency']
    convert = args['convert']

    url = f"https://bitpay.com/rates/BTC/{currency}"
    response = rqvsts.get(url)

    if response.status_code != HTTPStatus.OK:
        return '<h1>Ошибка запроса!</h1>'

    rate = response.json()['data']['rate']
    name = response.json()['data']['name']

    return (f"<h1>Обменять - {convert} {name} на Bitcoin</h1><br>"
            f"<h2>Курс - {rate} {currency}</h2><br>"
            f"<h2>Вы получите - {convert / rate:.8f}  BTC</h2>")


@app.route('/')
def home_page():
    return """
        <h1><a href="http://127.0.0.1:5000/generate_students?quality=100" target="_blank">Сгенерировать студентов</a><br>
        <a href="http://127.0.0.1:5000/bitcoin_rate?currency=UAH&convert=100" target="_blank">Обмен валют</a></h1>
    """


if __name__ == '__main__':
    app.run(debug=True)
