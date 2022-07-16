from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/", methods=['POST'])
def search_url():
    data = json.loads(request.data)
    print(data["url"])
    

    # use the url past from the frontend, get the result, and pass back to frontend
    items = [
        {'id': 1, 'title': "article1", 'url': "xxxx.com", 'reliability': "left", 'politicalLeaning': "xxxxx"},
        {'id': 2, 'title': "article2", 'url': "xxxx.com", 'reliability': "right", 'politicalLeaning': "xxxxx"},
        {'id': 3, 'title': "article3", 'url': "xxxx.com", 'reliability': "80", 'politicalLeaning': "xxxxx"},
        {'id': 4, 'title': "article4", 'url': "xxxx.com", 'reliability': "80%", 'politicalLeaning': "xxxxx"}
    ]
    
    return json.dumps({'data': items})



if __name__ == "__main__":
    app.run(debug = True)