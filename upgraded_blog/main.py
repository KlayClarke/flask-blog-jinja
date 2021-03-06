import os
import smtplib
import requests
from flask import Flask, render_template, request

MY_EMAIL = os.environ.get('GMAIL_USERNAME')
MY_PASSWORD = os.environ.get('GMAIL_PASSWORD')

all_posts = requests.get(url='https://api.npoint.io/79848603f977d255ecf6').json()
post_objects = []
for post in all_posts:
    individual_post = post
    post_objects.append(individual_post)

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', post_objects=post_objects)


@app.route('/post/<int:index>')
def get_post(index):
    requested_post = None
    for blog_post in post_objects:
        if blog_post['id'] == index:
            requested_post = blog_post
    return render_template('post.html', blog_post=requested_post)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        return render_template('contact.html', message='Contact Me')
    elif request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        send_email(name=name, email=email, phone=phone, message=message)
        return render_template('contact.html', message='Message successfully sent!')


def send_email(name, email, phone, message):
    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=MY_EMAIL,
                            msg=f'Subject:Site Inquiry From {name}\n\n'
                                f'Email: {email}\n, '
                                f'Phone: {phone}\n, '
                                f'Message: {message}')


if __name__ == '__main__':
    app.run(debug=True)
