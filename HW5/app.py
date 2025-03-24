from flask import Flask, render_template_string
from webargs import fields
from webargs.flaskparser import use_kwargs
from execute_query import execute_query

app = Flask(__name__)
@app.route('/stats_by_city')
@use_kwargs({
    'genre': fields.Str(load_default=None)
}, location='query')
def stats_by_city(genre):

    list_genres = tuple(genre[0] for genre in execute_query('SELECT name FROM genres'))

    if not genre or genre not in list_genres:
        template = '''<h1>Select a genre from the list</h1><br>
        {% for genre in list_genres %}
        ✅<a href="http://127.0.0.1:5000/stats_by_city?genre={{ genre }}">{{ genre }}</a><br>
        {% endfor %}'''
        return render_template_string(template, list_genres=list_genres)

    query = f'''SELECT customers.Country, customers.City, COUNT(*) max
                FROM customers
                JOIN invoices USING (CustomerId)
                JOIN invoice_items USING (InvoiceId)
                JOIN tracks USING (TrackId)
                JOIN genres USING (GenreId)
                WHERE genres.Name = '{genre}'
                GROUP BY customers.City
                ORDER BY max DESC
                LIMIT 1;'''

    resp = execute_query(query)

    return f'''<h1>The biggest like {genre} in {resp[0][1]} ({resp[0][0]}).<br>
    More than {resp[0][2]} residents have already purchased it.</h1>''' if len(resp) > 0 else '<h1>No data available</h1>'

@app.route('/index')
@app.route('/')
def home_page():
    return '<h1><a href="http://127.0.0.1:5000/stats_by_city?genre=#">Statistic of genre</a></h1>'


if __name__ == '__main__':
    app.run(debug=True)
