from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.book import Book, db
from utils.logger import logger

books_bp = Blueprint('books', __name__)

@books_bp.route('/books', methods=['GET'])
@jwt_required()
def get_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books]), 200

@books_bp.route('/books/<int:book_id>', methods=['GET'])
@jwt_required()
def get_book(book_id):
    book = Book.query.get(book_id)
    if book:
        return jsonify(book.to_dict()), 200
    return jsonify({'message': 'Book not found'}), 404

@books_bp.route('/books', methods=['POST'])
@jwt_required()
def create_book():
    data = request.get_json()
    new_book = Book(
        title=data['title'],
        author=data['author'],
        publish_date=data['publish_date'],
        image=data.get('image'),
        borrow_length=data['borrow_length']
    )
    db.session.add(new_book)
    db.session.commit()
    logger.info('New book created: {}'.format(new_book.title))
    return jsonify({'message': 'Book created'}), 201

@books_bp.route('/books/<int:book_id>', methods=['PUT'])
@jwt_required()
def update_book(book_id):
    data = request.get_json()
    book = Book.query.get(book_id)
    if book:
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.publish_date = data.get('publish_date', book.publish_date)
        book.image = data.get('image', book.image)
        book.borrow_length = data.get('borrow_length', book.borrow_length)
        db.session.commit()
        logger.info('Book {} updated'.format(book.title))
        return jsonify({'message': 'Book updated'}), 200
    return jsonify({'message': 'Book not found'}), 404

@books_bp.route('/books/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        logger.info('Book {} deleted'.format(book.title))
        return jsonify({'message': 'Book deleted'}), 200
    return jsonify({'message': 'Book not found'}), 404
