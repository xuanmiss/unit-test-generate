from flask import Flask
from unit_generate import unit_api

app = Flask(__name__)
app.register_blueprint(unit_api, url_prefix="/unit-test")


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
