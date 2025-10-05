# seed.py

from app import app
from database import db
from models import User, Book, Loan, Fine
import bcrypt
from datetime import datetime, timedelta

with app.app_context():
    # Add sample librarian
    if not User.query.filter_by(username='librarian').first():
        hashed_password = bcrypt.hashpw('librarian123'.encode('utf-8'), bcrypt.gensalt())
        librarian = User(
            username='librarian',
            password=hashed_password.decode('utf-8'),
            name='Librarian',
            role='librarian',
            email='librarian@example.com',
            phone='1234567890'
        )
        db.session.add(librarian)

    # Add sample patrons
    if not User.query.filter_by(username='john_doe').first():
        hashed_password = bcrypt.hashpw('password123'.encode('utf-8'), bcrypt.gensalt())
        john_doe = User(
            username='john_doe',
            password=hashed_password.decode('utf-8'),
            name='John Doe',
            role='patron',
            email='john@example.com',
            phone='11111111111'
        )
        db.session.add(john_doe)

    if not User.query.filter_by(username='jane_smith').first():
        hashed_password = bcrypt.hashpw('password123'.encode('utf-8'), bcrypt.gensalt())
        jane_smith = User(
            username='jane_smith',
            password=hashed_password.decode('utf-8'),
            name='Jane Smith',
            role='patron',
            email='jane@example.com',
            phone='22222222222'
        )
        db.session.add(jane_smith)

    if not User.query.filter_by(username='alice_wong').first():
        hashed_password = bcrypt.hashpw('password123'.encode('utf-8'), bcrypt.gensalt())
        alice_wong = User(
            username='alice_wong',
            password=hashed_password.decode('utf-8'),
            name='Alice Wong',
            role='patron',
            email='alice@example.com',
            phone='33333333333'
        )
        db.session.add(alice_wong)

    # Add sample books
    if Book.query.count() == 0:
        books = [
            Book(
                title='The Great Gatsby',
                author='F. Scott Fitzgerald',
                isbn='9780743273565',
                publisher='Scribner',
                publication_year=1925,
                copies_available=3,
                total_copies=3,
                location='Shelf 3'
            ),
            Book(
                title='To Kill a Mockingbird',
                author='Harper Lee',
                isbn='9780060935467',
                publisher='J.B. Lippincott & Co.',
                publication_year=1960,
                copies_available=2,
                total_copies=2,
                location='Shelf 1'
            ),
            Book(
                title='1984',
                author='George Orwell',
                isbn='9780451524935',
                publisher='Secker & Warburg',
                publication_year=1949,
                copies_available=4,
                total_copies=4,
                location='Shelf 5'
            ),
            # Add more books
            Book(
                title='Pride and Prejudice',
                author='Jane Austen',
                isbn='9780141199078',
                publisher='T. Egerton',
                publication_year=1813,
                copies_available=5,
                total_copies=5,
                location='Shelf 2'
            ),
            Book(
                title='Moby-Dick',
                author='Herman Melville',
                isbn='9780142437247',
                publisher='Richard Bentley',
                publication_year=1851,
                copies_available=2,
                total_copies=2,
                location='Shelf 4'
            ),
            Book(
                title='War and Peace',
                author='Leo Tolstoy',
                isbn='9780199232765',
                publisher='The Russian Messenger',
                publication_year=1869,
                copies_available=3,
                total_copies=3,
                location='Shelf 6'
            ),
            # Additional books
            Book(
                title='The Catcher in the Rye',
                author='J.D. Salinger',
                isbn='9780316769488',
                publisher='Little, Brown and Company',
                publication_year=1951,
                copies_available=4,
                total_copies=4,
                location='Shelf 7'
            ),
            Book(
                title='The Hobbit',
                author='J.R.R. Tolkien',
                isbn='9780547928227',
                publisher='George Allen & Unwin',
                publication_year=1937,
                copies_available=5,
                total_copies=5,
                location='Shelf 8'
            ),
            Book(
                title='Brave New World',
                author='Aldous Huxley',
                isbn='9780060850524',
                publisher='Chatto & Windus',
                publication_year=1932,
                copies_available=3,
                total_copies=3,
                location='Shelf 9'
            ),
            Book(
                title='The Lord of the Rings',
                author='J.R.R. Tolkien',
                isbn='9780544003415',
                publisher='George Allen & Unwin',
                publication_year=1954,
                copies_available=2,
                total_copies=2,
                location='Shelf 10'
            ),
            Book(
                title='Jane Eyre',
                author='Charlotte Brontë',
                isbn='9780141441146',
                publisher='Smith, Elder & Co.',
                publication_year=1847,
                copies_available=4,
                total_copies=4,
                location='Shelf 11'
            ),
            Book(
                title='The Adventures of Huckleberry Finn',
                author='Mark Twain',
                isbn='9780486280615',
                publisher='Chatto & Windus / Charles L. Webster And Company',
                publication_year=1884,
                copies_available=3,
                total_copies=3,
                location='Shelf 12'
            ),
            Book(
                title='Crime and Punishment',
                author='Fyodor Dostoevsky',
                isbn='9780140449136',
                publisher='The Russian Messenger',
                publication_year=1866,
                copies_available=2,
                total_copies=2,
                location='Shelf 13'
            ),
            Book(
                title='The Odyssey',
                author='Homer',
                isbn='9780140268867',
                publisher='Ancient Greece',
                publication_year=-800,  # Approximate date
                copies_available=5,
                total_copies=5,
                location='Shelf 14'
            ),
            Book(
                title='The Brothers Karamazov',
                author='Fyodor Dostoevsky',
                isbn='9780374528379',
                publisher='The Russian Messenger',
                publication_year=1880,
                copies_available=3,
                total_copies=3,
                location='Shelf 15'
            ),
            Book(
                title='Wuthering Heights',
                author='Emily Brontë',
                isbn='9780141439556',
                publisher='Thomas Cautley Newby',
                publication_year=1847,
                copies_available=4,
                total_copies=4,
                location='Shelf 16'
            ),
            Book(
                title='Great Expectations',
                author='Charles Dickens',
                isbn='9780141439563',
                publisher='Chapman & Hall',
                publication_year=1861,
                copies_available=2,
                total_copies=2,
                location='Shelf 17'
            ),
            # You can add more books here following the same format
        ]
        db.session.add_all(books)
        db.session.commit()  # Commit to get book IDs

    # Get users and books from the database
    john_doe = User.query.filter_by(username='john_doe').first()
    jane_smith = User.query.filter_by(username='jane_smith').first()
    alice_wong = User.query.filter_by(username='alice_wong').first()

    # Update book variables to include new books
    gatsby = Book.query.filter_by(title='The Great Gatsby').first()
    mockingbird = Book.query.filter_by(title='To Kill a Mockingbird').first()
    nineteen_eighty_four = Book.query.filter_by(title='1984').first()
    pride_and_prejudice = Book.query.filter_by(title='Pride and Prejudice').first()
    moby_dick = Book.query.filter_by(title='Moby-Dick').first()
    the_catcher_in_the_rye = Book.query.filter_by(title='The Catcher in the Rye').first()
    the_hobbit = Book.query.filter_by(title='The Hobbit').first()
    brave_new_world = Book.query.filter_by(title='Brave New World').first()
    the_lord_of_the_rings = Book.query.filter_by(title='The Lord of the Rings').first()
    jane_eyre = Book.query.filter_by(title='Jane Eyre').first()
    huckleberry_finn = Book.query.filter_by(title='The Adventures of Huckleberry Finn').first()
    crime_and_punishment = Book.query.filter_by(title='Crime and Punishment').first()
    the_odyssey = Book.query.filter_by(title='The Odyssey').first()
    brothers_karamazov = Book.query.filter_by(title='The Brothers Karamazov').first()
    wuthering_heights = Book.query.filter_by(title='Wuthering Heights').first()
    great_expectations = Book.query.filter_by(title='Great Expectations').first()

    # Add sample loans, including overdue loans
    if Loan.query.count() == 0:
        loans = [
            # Non-overdue loan
            Loan(
                user_id=john_doe.id,
                book_id=gatsby.id,
                due_date=datetime.utcnow() + timedelta(days=7),
                return_date=None
            ),
            # Overdue loan
            Loan(
                user_id=jane_smith.id,
                book_id=mockingbird.id,
                due_date=datetime.utcnow() - timedelta(days=5),
                return_date=None
            ),
            # Returned loan
            Loan(
                user_id=alice_wong.id,
                book_id=nineteen_eighty_four.id,
                due_date=datetime.utcnow() - timedelta(days=10),
                return_date=datetime.utcnow() - timedelta(days=2)
            ),
            # Another overdue loan
            Loan(
                user_id=john_doe.id,
                book_id=pride_and_prejudice.id,
                due_date=datetime.utcnow() - timedelta(days=3),
                return_date=None
            ),
            # Additional loans
            Loan(
                user_id=jane_smith.id,
                book_id=the_hobbit.id,
                due_date=datetime.utcnow() + timedelta(days=10),
                return_date=None
            ),
            Loan(
                user_id=alice_wong.id,
                book_id=brave_new_world.id,
                due_date=datetime.utcnow() + timedelta(days=5),
                return_date=None
            ),
            Loan(
                user_id=john_doe.id,
                book_id=the_lord_of_the_rings.id,
                due_date=datetime.utcnow() + timedelta(days=14),
                return_date=None
            ),
            Loan(
                user_id=jane_smith.id,
                book_id=crime_and_punishment.id,
                due_date=datetime.utcnow() - timedelta(days=2),
                return_date=None
            ),
        ]
        # Adjust the book's copies_available
        for loan in loans:
            book = Book.query.get(loan.book_id)
            if loan.return_date is None:
                book.copies_available -= 1
        db.session.add_all(loans)
        db.session.commit()

    # Add sample fines, including unpaid fines
    if Fine.query.count() == 0:
        fines = [
            Fine(
                user_id=jane_smith.id,
                amount=5.00,
                description='Overdue fine for "To Kill a Mockingbird"',
                paid=False
            ),
            Fine(
                user_id=alice_wong.id,
                amount=2.50,
                description='Overdue fine for "1984"',
                paid=True
            ),
            Fine(
                user_id=john_doe.id,
                amount=3.00,
                description='Overdue fine for "Pride and Prejudice"',
                paid=False
            ),
            Fine(
                user_id=jane_smith.id,
                amount=4.00,
                description='Overdue fine for "Crime and Punishment"',
                paid=False
            ),
        ]
        db.session.add_all(fines)
        db.session.commit()

    print('Database seeded successfully!')
