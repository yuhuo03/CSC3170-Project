from database import db
from datetime import datetime, timedelta

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'patron' or 'librarian'
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    loans = db.relationship(
        'Loan',
        backref='user',
        cascade='all, delete-orphan',
        passive_deletes=True,
        lazy=True
    )
    holds = db.relationship(
        'Hold',
        backref='user',
        cascade='all, delete-orphan',
        passive_deletes=True,
        lazy=True
    )
    fines = db.relationship(
        'Fine',
        backref='user',
        cascade='all, delete-orphan',
        passive_deletes=True,
        lazy=True
    )

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'role': self.role,
            'email': self.email,
            'phone': self.phone
        }

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    copies_available = db.Column(db.Integer, nullable=False)
    total_copies = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(50), nullable=False)
    loans = db.relationship('Loan', backref='book', lazy=True)
    holds = db.relationship('Hold', backref='book', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'publisher': self.publisher,
            'publication_year': self.publication_year,
            'copies_available': self.copies_available,
            'total_copies': self.total_copies,
            'location': self.location
        }

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
        nullable=False
    )
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    loan_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime, nullable=True)


    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user': {
                'id': self.user.id,
                'name': self.user.name,
            },
            'book_id': self.book_id,
            'book_title': self.book.title,
            'due_date': self.due_date.isoformat(),
            'return_date': self.return_date.isoformat() if self.return_date else None,
        }

class Hold(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
        nullable=False
    )
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    hold_date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'hold_date': self.hold_date.isoformat(),
            'book_title': self.book.title
        }

class Fine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
        nullable=False
    )
    amount = db.Column(db.Float, nullable=False)
    paid = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user': {
                'id': self.user.id,
                'name': self.user.name,
            },
            'amount': float(self.amount),
            'description': self.description,
            'paid': self.paid,
        }
