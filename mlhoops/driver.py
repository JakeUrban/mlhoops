from flask import Flask
from mlhoops.config import config

app = Flask(__name__)
app.config.update(config)


@app.route('/')
def hello_world():
    return 'Hello World!'


def main():
    app.run()


if __name__ == '__main__':
    main()
