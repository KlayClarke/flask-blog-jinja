import requests
from post import Post
from flask import Flask, render_template


all_posts = requests.get(url="https://api.npoint.io/c790b4d5cab58020d391").json()
post_objects = []
for post in all_posts:
    individual_post = Post(post["id"], post["title"], post["subtitle"], post["body"])
    post_objects.append(individual_post)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", all_posts=all_posts)


@app.route("/post/<int:index>")
def get_post(index):
    requested_post = None
    for blog_post in post_objects:
        if blog_post.post_id == index:
            requested_post = blog_post
    return render_template("post.html", blog_post=requested_post)


if __name__ == "__main__":
    app.run(debug=True)
