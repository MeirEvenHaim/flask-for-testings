from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    published_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<Book {self.title}>"
