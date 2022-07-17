from flask import Flask, render_template, request, redirect, url_for
import json
from functions import returnBiases

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/", methods=['POST'])
def search_url():
    data = json.loads(request.data)
    print(data["url"])
    

    # use the url past from the frontend, get the result, and pass back to frontend
    result = returnBiases(data["url"])
    if (len(result) == 0):
        return json.dumps({'error': True})
    return json.dumps({'data': result})



if __name__ == "__main__":
    app.run(debug = True)