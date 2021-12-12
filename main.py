import datetime
import requests
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    current_year = datetime.date.today().year
    return render_template('index.html', year=current_year)


@app.route('/guess/<name>')
def guess(name):
    age_request = requests.get(url=f'https://api.agify.io/?name={name}')
    age_json = age_request.json()
    age_prediction = age_json['age']
    gender_request = requests.get(url=f'https://api.genderize.io/?name={name}')
    gender_json = gender_request.json()
    gender_prediction = gender_json['gender']
    return render_template('predictions.html', name=name.title(), predicted_age=age_prediction,
                           predicted_gender=gender_prediction)


@app.route('/blog')
def blog():
    blog_response = requests.get(url='https://api.npoint.io/c790b4d5cab58020d391')
    all_posts = blog_response.json()
    return render_template('blog.html', all_posts=all_posts)


if __name__ == '__main__':
    app.run(debug=True)
