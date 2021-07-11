from flask import Flask

# blueprint import
from blueprints.tweets.tweets import tweetsData
from blueprints.btc.btc import btcData


def create_app(app):
    # register blueprint
    app.register_blueprint(tweetsData)
    app.register_blueprint(btcData)

    return app


if __name__ == "__main__":
    app = Flask(__name__)
    create_app(app).run(host="0.0.0.0", debug=False, port=9000)
