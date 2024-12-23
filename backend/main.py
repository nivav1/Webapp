from flask import Flask
from flask_cors import CORS
from sqlalchemy import inspect
from ytDownloader import yt_blueprint
from app import app as register_bp
from extensions import db, bcrypt
from sqlalchemy.exc import OperationalError
from otel_config import setup_otel

main_app = Flask(__name__)

setup_otel(main_app)

main_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://niv:niv123@db-service:5432/mydb'
main_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(main_app)
bcrypt.init_app(main_app)
CORS(main_app, expose_headers=["Content-Disposition",])

main_app.register_blueprint(register_bp, url_prefix='/api')

main_app.register_blueprint(yt_blueprint, url_prefix='/api/yt')


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
