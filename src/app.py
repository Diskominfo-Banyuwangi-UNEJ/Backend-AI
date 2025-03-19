from flask import Flask
from routes.user_bp import user_bp

app = Flask(__name__)
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run()
