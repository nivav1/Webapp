from flask import Flask
from flask_cors import CORS
from sqlalchemy import inspect
from ytDownloader import yt_blueprint
from app import app as core_app
from extensions import db, bcrypt
from sqlalchemy.exc import OperationalError
import os

main_app = Flask(__name__)

db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')

main_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{db_username}:{db_password}@db-service:5432/mydb'
main_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(main_app)
bcrypt.init_app(main_app)
CORS(main_app, expose_headers=["Content-Disposition",])

main_app.register_blueprint(core_app, url_prefix='/')

main_app.register_blueprint(yt_blueprint, url_prefix='/yt')


def initialize_database():
    with main_app.app_context():
        try:
            tables = inspect(db.engine).get_table_names()
            if not tables:
                print("No tables found. Creating tables...")
                db.create_all()
                print("Tables created.")
            else:
                print("Tables already exist. Skipping creation.")
        except OperationalError:
            print("Database connection failed."
                  " Ensure the database server is running.")


initialize_database()

if __name__ == "__main__":
    pass
    # main_app.run(debug=True)
