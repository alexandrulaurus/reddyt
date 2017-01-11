from flask import Flask

app = Flask(__name__)

@app.route("/")
def main():
    return "This is a flask server running in Docker. Hi!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
