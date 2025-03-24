from flask import Flask, render_template_string
from faker import Faker
import csv
import requests
from http import HTTPStatus
from webargs import fields, validate
from webargs.flaskparser import use_kwargs

app = Flask(__name__)
faker = Faker()


@app.route('/generate_students')
@use_kwargs({
    'quality': fields.Int(validate=validate.Range(min=1, max=1000), load_default=1)},
    location='query')
def generate_students(quality):

    list_students = []

    for _ in range(quality):
        student = [
            faker.first_name(),
            faker.last_name(),
            faker.email(domain='gmail.com'),
            faker.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True),
            faker.date_of_birth(minimum_age=18, maximum_age=60)]
        list_students.append(student)

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
@use_kwargs({
    'currency': fields.Str(validate=validate.Length(min=3), load_default='USD'),
    'convert': fields.Int(validate=validate.Range(min=1), load_default=1)},
    location='query')
def bitcoin_rate(currency, convert):

    url = f"https://bitpay.com/rates/BTC/{currency}"
    response = requests.get(url)

    if response.status_code != HTTPStatus.OK:
        return '<h1>Ошибка запроса!</h1>'

    rate = response.json().get('data', {}).get('rate')
    name = response.json().get('data', {}).get('name')

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
