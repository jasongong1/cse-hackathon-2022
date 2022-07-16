from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():

    items = [
        {'id': 1, 'title': "article1", 'url': "xxxx.com", 'reliablity': "80%", 'political leaning': "xxxxx"},
        {'id': 2, 'title': "article2", 'url': "xxxx.com", 'reliablity': "80%", 'political leaning': "xxxxx"},
        {'id': 3, 'title': "article3", 'url': "xxxx.com", 'reliablity': "80%", 'political leaning': "xxxxx"},
        {'id': 4, 'title': "article4", 'url': "xxxx.com", 'reliablity': "80%", 'political leaning': "xxxxx"}
    ]

    return render_template('index.html', items=items)

@app.route("/about/<username>")
def about_page(username):
    return f'<h1>About page with the user name: {username}</h1>'

if __name__ == "__main__":
    app.run(debug = True)