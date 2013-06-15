from flask import Flask, url_for, render_template, request
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/wb_callback")
def weibo_callback():
    return render_template("weibo_callback.html")


if __name__ == "__main__":
    #app.debug = True
    app.run()
