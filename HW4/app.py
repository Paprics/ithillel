from flask import Flask
from webargs import fields, validate
from webargs.flaskparser import use_kwargs
from execute_query import execute_query

app = Flask(__name__)

@app.route('/order_price')
@use_kwargs({'country': fields.Str(validate=validate.Length(min=3), load_default=None)},
            location='query')
def order_price(country):
    # http://127.0.0.1:5000/order_price?country=USA
    # http://127.0.0.1:5000/order_price

    if country:
        query = f'''SELECT customers.Country, SUM(invoices.Total) AS TotalSales
                            FROM customers
                            JOIN invoices ON customers.CustomerId = invoices.CustomerId
                            WHERE  customers.Country = "{country}";'''

    else:
        query = f'''SELECT customers.Country, SUM(invoices.Total) AS Total
                            FROM customers
                            JOIN invoices ON customers.CustomerId = invoices.CustomerId
                            GROUP BY customers.Country
                            ORDER BY customers.Country;'''

    return execute_query(query=query)


@app.route('/info_about_track')
@use_kwargs({'trackid': fields.Int(validate=validate.Range(min=1, max=3503), load_default=1)},
            location='query')
def info_about_track(trackid):
    # http://127.0.0.1:5000/info_about_track
    # http://127.0.0.1:5000/info_about_track?trackid=3000

    query = f'''SELECT tracks.Name AS Track_name, 
       albums.Title AS Album, 
       artists.Name AS Artist, 
       genres.Name AS Genre,
       (tracks.Milliseconds / 1000) AS "Duration sec", 
       tracks.UnitPrice AS Price
        FROM tracks
        INNER JOIN albums ON tracks.AlbumId = albums.AlbumId
        INNER JOIN artists ON artists.ArtistId = albums.ArtistId
        INNER JOIN genres ON genres.GenreId = tracks.GenreId
        INNER JOIN playlist_track ON playlist_track.TrackId = tracks.TrackId
        INNER JOIN playlists ON playlists.PlaylistId = playlist_track.PlaylistId
        WHERE tracks.TrackId = {trackid};'''

    return execute_query(query)

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