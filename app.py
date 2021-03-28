from flask import Flask, redirect, url_for, render_template
import requests as HTTP

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html')


def strip_accents(input_str):
    encoding = "utf-8"
    unicode_string = input_str.decode(encoding)
    nfkd_form = unicodedata.normalize('NFKD', unicode_string)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


def get_movies_by_genre(genreId):
    movies_list = []
    count = [1,2]
    for i in count:
        url = 'http://api.themoviedb.org/3/discover/movie?api_key=9a2f7f6b764b2fc742b1428446b00a73&sort_by=popularity.desc&page='+str(i)+'&with_genres=' + str(
            genreId)
        resp = HTTP.get(url)
        data = resp.json()
        for item in data['results']:
            movies_list.append(item)

    return movies_list


@app.route('/movies/<type>')
def face(type):
    movies_list = get_movies_by_genre(type)
    movies_dictionary = []
    for movie in movies_list:
        if movie['poster_path'] :
            logo = 'https://image.tmdb.org/t/p/original' + movie['poster_path']
        else:
            logo = '../static/default-movie.jpg'
        title = movie['title']
        overview = movie['overview']
        release_date = movie['release_date']
        id = movie['id']
        rating = movie['vote_average']
        adult = movie['adult']
        movies_dictionary.append({
            "logo" : logo,
            "title":title,
            "overview": overview,
            "release_date":release_date,
            "id" : id,
            "rating" : rating,
            "adult" : adult
        })

    return render_template('happy.html', content=movies_dictionary)

if __name__ == '__main__':
    app.run()