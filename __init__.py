from flask import Flask, render_template, request, url_for, redirect

import recommend as model

app = Flask(__name__)

@app.route('/', methods = ["GET"])
def homepage():
    return render_template("index.html")

@app.route('/movies/', methods = ["GET"])
def movies():
    return render_template("movies.html")

@app.route('/aboutus/')
def aboutus():
    return render_template("aboutus.html")

@app.route('/result/', methods =["GET","POST"])
def result(premovie):
    return render_template("result.html",premovie = premovie)

@app.route('/movies/', methods = ["GET", "POST"])
def GET_page():
    if request.method == "POST":
        attempted_userid = int(request.form['userid'])
        attempted_number = int(request.form['number'])
        premovie = model.recommend_movie(attempted_userid, attempted_number)
        return render_template("result.html", premovie=premovie)

if __name__ == "__main__":
    app.run(debug = True,host='0.0.0.0',port= 8000,passthrough_errors=True)
