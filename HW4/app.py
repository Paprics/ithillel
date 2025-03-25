from flask import Flask
from webargs import fields, validate
from webargs.flaskparser import use_kwargs
from database_handler import execute_query

app = Flask(__name__)

@app.route('/order_price')
@use_kwargs({'country': fields.Str(validate=validate.Length(min=3), load_default=None)},
            location='query')
def order_price(country):
    if country:
        query = '''SELECT BillingCountry, SUM(Total) AS Suma, COUNT(*) AS Quality
                    FROM invoices
                    WHERE BillingCountry = ?
                    GROUP BY BillingCountry;'''
        return execute_query(query, (country,))
    else:
        query = '''SELECT BillingCountry, SUM(Total) AS Suma, COUNT(*) AS Quality
                    FROM invoices
                    GROUP BY BillingCountry;'''
        return execute_query(query)



@app.route('/info_about_track')
@use_kwargs({'trackid': fields.Int(validate=validate.Range(min=1, max=3503), load_default=1)},
            location='query')
def info_about_track(trackid):

    query = '''SELECT 
            tracks.TrackId, tracks.Name, tracks.Composer, tracks.Milliseconds, tracks.Bytes, tracks.UnitPrice,
            albums.Title, genres.Name, media_types.Name,
            artists.Name
            FROM tracks
            JOIN albums ON tracks.AlbumId = albums.AlbumId
            JOIN genres ON tracks.GenreId = genres.GenreId
            JOIN media_types ON tracks.MediaTypeId = media_types.MediaTypeId
            JOIN artists ON albums.ArtistId = artists.ArtistId
            WHERE tracks.TrackId = ?;'''

    return execute_query(query, (trackid,))

@app.route('/sound_time')
def get_all_sound_time():
    # http://127.0.0.1:5000/sound_time
    query = "SELECT (SUM(Milliseconds) / 3600000) 'Duration, hour' FROM tracks;"
    return f'<h1>🎶Playing time of all tracks - {execute_query(query)[0][0]} hours.</h1>'


@app.route('/')
def home_page():
    return f'''<h1>
        <a href="http://127.0.0.1:5000/order_price?country=USA" target="_blank">Sales by country</a><br>
        <a href="http://127.0.0.1:5000/info_about_track?trackid=3000" target="_blank">Info About Track</a><br>
        <a href="http://127.0.0.1:5000/sound_time" target="_blank">Playing time of all tracks</a>
    </h1>'''


if __name__ == '__main__':
    app.run(debug=True)