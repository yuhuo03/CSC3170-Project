from flask import request, jsonify
from flask_restful import Resource
from models import User, Book, Loan, Hold, Fine
from database import db
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
import bcrypt
from datetime import datetime, timedelta
from sqlalchemy import or_
from marshmallow import Schema, fields, validate, ValidationError

class UserSchema(Schema):
    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, error='Username must be at least 3 characters long')
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=6, error='Password must be at least 6 characters long')
    )
    name = fields.Str(required=True, validate=validate.Length(min=3, error='Name must be at least 3 characters long'))
    email = fields.Email(required=True, error='Invalid email address')
    phone = fields.Str(
        required=True,
        validate=validate.Regexp(
            r'^\d{10,11}$',
            error='Phone number must be 10 or 11 digits long and contain only digits'
        )
    )
    
class BookSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, error='Title is required'))
    author = fields.Str(required=True, validate=validate.Length(min=1, error='Author is required'))
    isbn = fields.Str(required=True, validate=validate.Length(min=1, error='ISBN is required'))
    publisher = fields.Str(required=True, validate=validate.Length(min=1, error='Publisher is required'))
    publication_year = fields.Int(required=True, validate=validate.Range(min=0, error='Invalid publication year'))
    total_copies = fields.Int(required=True, validate=validate.Range(min=1, error='Total copies must be at least 1'))
    location = fields.Str(required=True, validate=validate.Length(min=1, error='Location is required'))
    
def initialize_routes(api):
    # User Authentication
    api.add_resource(Register, '/api/register')
    api.add_resource(Login, '/api/login')

    # Book Management
    api.add_resource(BookList, '/api/books')
    api.add_resource(BookDetail, '/api/books/<int:book_id>')

    # User Dashboard
    api.add_resource(UserDashboard, '/api/dashboard')

    # Holds and Loans
    api.add_resource(PlaceHold, '/api/hold/<int:book_id>')
    api.add_resource(BorrowBook, '/api/borrow/<int:book_id>')
    api.add_resource(ReturnBook, '/api/return/<int:loan_id>')

    # User Management
    api.add_resource(UserList, '/api/users')
    api.add_resource(UserDetail, '/api/users/<int:user_id>')

    # Fines
    api.add_resource(PayFine, '/api/payfine/<int:fine_id>')

    # Reports
    api.add_resource(GenerateReports, '/api/reports')

# User Authentication

class Register(Resource):
    def post(self):
        json_data = request.get_json()
        user_schema = UserSchema()
        try:
            data = user_schema.load(json_data)
        except ValidationError as err:
            return {'message': 'Validation errors', 'errors': err.messages}, 400
        
        # Check if username already exists
        if User.query.filter_by(username=data['username']).first():
            return {'message': 'Username already exists', 'errors': {'username': ['Username already exists']}}, 400
        
        # Hash the password
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        
        # Create new user
        new_user = User(
            username=data['username'],
            password=hashed_password.decode('utf-8'),
            name=data['name'],
            role='patron',
            email=data['email'],
            phone=data['phone']
        )
        
        # Save the user to the database
        db.session.add(new_user)
        db.session.commit()
        
        return {'message': 'User registered successfully'}, 201

class Login(Resource):
    def post(self):
        json_data = request.get_json()
        user_schema = UserSchema(only=['username', 'password'])
        try:
            data = user_schema.load(json_data)
        except ValidationError as err:
            return {'message': 'Validation errors', 'errors': err.messages}, 400
        user = User.query.filter_by(username=data['username']).first()
        if user and bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
            access_token = create_access_token(identity={'id': user.id, 'role': user.role})
            return {'token': access_token}, 200
        else:
            return {'message': 'Invalid credentials'}, 401

# Book Management

class BookList(Resource):
    @jwt_required()
    def get(self):
        search = request.args.get('search', '')
        books = Book.query.filter(
            or_(
                Book.title.ilike(f'%{search}%'),
                Book.author.ilike(f'%{search}%')
            )
        ).all()
        return jsonify([book.to_dict() for book in books])

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if current_user['role'] != 'librarian':
            return {'message': 'Access denied'}, 403

        json_data = request.get_json()
        book_schema = BookSchema()
        try:
            data = book_schema.load(json_data)
        except ValidationError as err:
            return {'message': 'Validation errors', 'errors': err.messages}, 400
        
        if Book.query.filter_by(isbn=data['isbn']).first():
            return {'message': 'Book with this ISBN already exists'}, 400

        new_book = Book(
            title=data['title'],
            author=data['author'],
            isbn=data['isbn'],
            publisher=data['publisher'],
            publication_year=data['publication_year'],
            copies_available=data['total_copies'],
            total_copies=data['total_copies'],
            location=data['location']
        )
        db.session.add(new_book)
        db.session.commit()

        return {'message': 'Book added successfully'}, 201

class BookDetail(Resource):
    @jwt_required()
    def get(self, book_id):
        book = Book.query.get(book_id)
        if book:
            return jsonify(book.to_dict())
        else:
            return {'message': 'Book not found'}, 404

    @jwt_required()
    def put(self, book_id):
        current_user = get_jwt_identity()
        if current_user['role'] != 'librarian':
            return {'message': 'Access denied'}, 403

        book = Book.query.get(book_id)
        if not book:
            return {'message': 'Book not found'}, 404

        json_data = request.get_json()
        book_schema = BookSchema()
        try:
            data = book_schema.load(json_data)
        except ValidationError as err:
            return {'message': 'Validation errors', 'errors': err.messages}, 400

        # Update book fields
        book.title = data['title']
        book.author = data['author']
        book.isbn = data['isbn']
        book.publisher = data['publisher']
        book.publication_year = data['publication_year']
        book.total_copies = data['total_copies']
        book.location = data['location']

        # Adjust copies_available if total_copies changed
        difference = data['total_copies'] - book.total_copies
        book.copies_available += difference

        db.session.commit()

        return {'message': 'Book updated successfully'}, 200

    @jwt_required()
    def delete(self, book_id):
        current_user = get_jwt_identity()
        if current_user['role'] != 'librarian':
            return {'message': 'Access denied'}, 403

        book = Book.query.get(book_id)
        if not book:
            return {'message': 'Book not found'}, 404

        db.session.delete(book)
        db.session.commit()
        return {'message': 'Book deleted successfully'}, 200

# User Dashboard

class UserDashboard(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.get(current_user['id'])

        loans = [loan.to_dict() for loan in user.loans if not loan.return_date]
        fines = [fine.to_dict() for fine in user.fines if not fine.paid]

        return {
            'user': user.to_dict(),
            'loans': loans,
            'fines': fines
        }, 200

# Holds and Loans

class PlaceHold(Resource):
    @jwt_required()
    def post(self, book_id):
        current_user = get_jwt_identity()
        user = User.query.get(current_user['id'])
        book = Book.query.get(book_id)

        if not book:
            return {'message': 'Book not found'}, 404

        existing_hold = Hold.query.filter_by(user_id=user.id, book_id=book.id).first()
        if existing_hold:
            return {'message': 'You already have a hold on this book'}, 400

        new_hold = Hold(user_id=user.id, book_id=book.id)
        db.session.add(new_hold)
        db.session.commit()

        return {'message': 'Hold placed successfully'}, 200

class BorrowBook(Resource):
    @jwt_required()
    def post(self, book_id):
        current_user = get_jwt_identity()
        user = User.query.get(current_user['id'])
        book = Book.query.get(book_id)

        if not book:
            return {'message': 'Book not found'}, 404

        if book.copies_available <= 0:
            return {'message': 'No copies available'}, 400

        existing_loan = Loan.query.filter_by(user_id=user.id, book_id=book.id, return_date=None).first()
        if existing_loan:
            return {'message': 'You have already borrowed this book'}, 400

        book.copies_available -= 1

        new_loan = Loan(
            user_id=user.id,
            book_id=book.id,
            due_date=datetime.utcnow() + timedelta(days=14)
        )
        db.session.add(new_loan)
        db.session.commit()

        return {'message': 'Book borrowed successfully'}, 200

class ReturnBook(Resource):
    @jwt_required()
    def post(self, loan_id):
        current_user = get_jwt_identity()
        user = User.query.get(current_user['id'])
        loan = Loan.query.get(loan_id)

        if not loan or loan.user_id != user.id or loan.return_date:
            return {'message': 'Invalid loan record'}, 400

        loan.return_date = datetime.utcnow()
        loan.book.copies_available += 1

        if loan.return_date > loan.due_date:
            days_overdue = (loan.return_date - loan.due_date).days
            fine_amount = days_overdue * 0.5  # $0.5 per day
            new_fine = Fine(
                user_id=user.id,
                amount=fine_amount,
                description=f'Overdue fine for "{loan.book.title}"'
            )
            db.session.add(new_fine)

        db.session.commit()

        return {'message': 'Book returned successfully'}, 200

# Fines

class PayFine(Resource):
    @jwt_required()
    def post(self, fine_id):
        current_user = get_jwt_identity()
        user = User.query.get(current_user['id'])
        fine = Fine.query.get(fine_id)

        if not fine or fine.user_id != user.id or fine.paid:
            return {'message': 'Invalid fine record'}, 400

        fine.paid = True
        db.session.commit()

        return {'message': 'Fine paid successfully'}, 200


    

# Reports
class GenerateReports(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        if current_user['role'] != 'librarian':
            return {'message': '权限不足'}, 403

        # total books
        total_books = Book.query.count()

        # total loans
        total_loans = Loan.query.count()

        # total fines
        total_fines = db.session.query(db.func.sum(Fine.amount)).filter(Fine.paid == True).scalar() or 0

        # overdue loans
        overdue_loans = Loan.query.filter(
            Loan.return_date == None,
            Loan.due_date < datetime.utcnow()
        ).all()
        overdue_loans_list = [loan.to_dict() for loan in overdue_loans]

        # unpaid fines
        unpaid_fines = Fine.query.filter_by(paid=False).all()
        unpaid_fines_list = [fine.to_dict() for fine in unpaid_fines]

        # most popular books
        most_popular_books = db.session.query(
            Book.title,
            db.func.count(Loan.id).label('borrow_count')
        ).join(Loan).group_by(Book.id).order_by(db.desc('borrow_count')).limit(5).all()
        most_popular_books_list = [{'title': title, 'count': count} for title, count in most_popular_books]

        report = {
            'total_books': total_books,
            'total_loans': total_loans,
            'total_fines': total_fines,
            'overdue_loans': overdue_loans_list,
            'unpaid_fines': unpaid_fines_list,
            'most_popular_books': most_popular_books_list,
        }

        return report, 200

# User Management
class UserList(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        if current_user['role'] != 'librarian':
            return {'message': 'Insufficient permissions'}, 403

        users = User.query.filter(User.role != 'librarian').all()
        return jsonify([user.to_dict() for user in users])

class UserDetail(Resource):
    @jwt_required()
    def get(self, user_id):
        current_user = get_jwt_identity()
        if current_user['role'] != 'librarian':
            return {'message': 'Insufficient permissions'}, 403

        user = User.query.get(user_id)
        if user:
            return jsonify(user.to_dict())
        else:
            return {'message': 'User not found'}, 404

    @jwt_required()
    def put(self, user_id):
        current_user = get_jwt_identity()
        if current_user['role'] != 'librarian':
            return {'message': 'Insufficient permissions'}, 403

        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        data = request.get_json()
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.phone = data.get('phone', user.phone)
        db.session.commit()

        return {'message': 'User information updated successfully'}, 200

    @jwt_required()
    def delete(self, user_id):
        current_user = get_jwt_identity()
        if current_user['role'] != 'librarian':
            return {'message': 'Insufficient permissions'}, 403

        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}, 200