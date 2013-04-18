from flask import Flask, url_for
app = Flask(__name__)

@app.route("/")
def index():
    return "hello iMeidou"

if __name__ == "__main__":
    app.run()
