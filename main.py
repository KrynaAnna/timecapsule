import os
from datetime import date, datetime, timedelta

from flask import Flask, redirect, render_template, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy


# Set directory for uploaded images
current_dir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(current_dir, 'static', 'customer')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '8BYkEfBA1O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# Set up database
instance_folder = os.path.join(app.root_path, 'instance')
db_file_path = os.path.join(instance_folder, 'data.db')

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_file_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Define the Data model
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    recipient = db.Column(db.String(80), nullable=False)
    date_past = db.Column(db.Date, default=date.today())
    date_future = db.Column(db.Date, nullable=False)
    body = db.Column(db.String(1000), nullable=False)
    img_url = db.Column(db.String(300), nullable=True)


# Create the tables
with app.app_context():
    db.create_all()

    @app.route("/", methods=['GET', 'POST'])
    def home():
        if request.method == "POST":
            new_item = Data(
                name=request.form.get('name'),
                recipient=request.form.get('email'),
                date_past=date.today(),
                date_future=datetime.strptime(
                    request.form.get('date'), '%Y-%m-%d'),
                body=request.form.get('text')
            )

            db.session.add(new_item)
            db.session.commit()

            img_url = request.files["file"]
            if img_url:
                img_end = img_url.filename.split('.')[1]
                img_name = f'{new_item.id}.{img_end}'
                img_url.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], img_name))
                item = Data.query.get(new_item.id)
                item.img_url = img_name

            db.session.commit()
            db.session.rollback()
            return redirect("/success")

        today = date.today()
        tomorrow = today + timedelta(days=1)

        return render_template("index.html", date_today=today, tomorrow=tomorrow)

    @app.route("/success")
    def success():
        return render_template("success.html")

if __name__ == '__main__':
    app.run(debug=False, port=80)
