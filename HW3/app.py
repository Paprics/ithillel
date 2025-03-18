from flask import Flask, render_template_string, request
from faker import Faker
from jinja2 import escape
import csv
import requests as rqvsts
from http import HTTPStatus

app = Flask(__name__)
faker = Faker()

@app.route('/generate_students')
def generate_students():

    # http://127.0.0.1:5000/generate_students?quality=100

    list_students = []


    quality_students = min(int(request.args.get('quality', '1')), 1000)

    # Generate list of students
    for _ in range(int(quality_students)):
        first_name = faker.first_name()
        last_name = faker.last_name()
        email = faker.email(domain='gmail.com')
        password = faker.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
        birthday = faker.date_of_birth(minimum_age=18, maximum_age=60)
        student = [first_name, last_name, email, password, birthday]
        list_students.append(student)

    # pprint(list_students)

    # Save list of students to CSV file
    with open('students.csv', 'w', newline='') as file:
        headers = ['first_name', 'last_name', 'email', 'password', 'birthday']
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(list_students)

    template = escape('''<h3>List of students:</h3>
        <ol>
            {% for student in students %}
                <li>{{ student | join(' ') }}</li>
            {% endfor %}
        </ol>
        ''')

    return render_template_string(template, students=list_students)


@app.route('/bitcoin_rate')
def get_bitcoin_value():

    # http://127.0.0.1:5000/bitcoin_rate?currency=UAH&convert=100

    currency = request.args.get('currency', 'USD')
    convert = request.args.get('convert', '1')

    url = "https://bitpay.com/api/rates"
    response = rqvsts.get(url)

    if response.status_code != HTTPStatus.OK:
        return '<h1>Ошибка запроса!</h1>'

    # print(response.json())

    for crns in response.json():
        if crns['code'] == currency:
            rate = float(crns.get("rate", 0))
            amount = float(convert)
            result = amount / rate

            return (f'<h1>Обменять - {amount} {currency} на Bitcoin</h1><br>'
                    f'<h2>Курс - {rate} {currency}</h2><br>'
                    f'<h2>Вы получите - {result:.8f} BTC</h2>')



if __name__ == '__main__':
    app.run(debug=True)
