from flask import Flask

# blueprint import
from blueprints.sentimentData.views import sentimentData


def create_app(app):
    # register blueprint
    app.register_blueprint(sentimentData)

    return app


if __name__ == "__main__":
    app = Flask(__name__)
    create_app(app).run(debug=True, port=9000)
