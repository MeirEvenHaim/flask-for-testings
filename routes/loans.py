from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.loan import Loan, db
from models.book import Book
from models.user import User
from utils.logger import logger

loans_bp = Blueprint('loans', __name__)

@loans_bp.route('/loans', methods=['GET'])
@jwt_required()
def get_loans():
    loans = Loan.query.all()
    return jsonify([loan.to_dict() for loan in loans]), 200

@loans_bp.route('/loans/<int:loan_id>', methods=['GET'])
@jwt_required()
def get_loan(loan_id):
    loan = Loan.query.get(loan_id)
    if loan:
        return jsonify(loan.to_dict()), 200
    return jsonify({'message': 'Loan not found'}), 404

@loans_bp.route('/loans', methods=['POST'])
@jwt_required()
def create_loan():
    data = request.get_json()
    book = Book.query.get(data['book_id'])
    user = User.query.get(data['user_id'])
    if book is None or user is None:
        return jsonify({'message': 'Invalid book or user ID'}), 400
    
    new_loan = Loan(
        book_id=data['book_id'],
        user_id=data['user_id'],
        loan_date=data['loan_date'],
        return_status=data['return_status']
    )
    db.session.add(new_loan)
    db.session.commit()
    logger.info('New loan created for user {}: book {}'.format(user.username, book.title))
    return jsonify({'message': 'Loan created'}), 201

@loans_bp.route('/loans/<int:loan_id>', methods=['PUT'])
@jwt_required()
def update_loan(loan_id):
    data = request.get_json()
    loan = Loan.query.get(loan_id)
    if loan:
        loan.return_status = data.get('return_status', loan.return_status)
        db.session.commit()
        logger.info('Loan ID {} updated'.format(loan_id))
        return jsonify({'message': 'Loan updated'}), 200
    return jsonify({'message': 'Loan not found'}), 404

@loans_bp.route('/loans/<int:loan_id>', methods=['DELETE'])
@jwt_required()
def delete_loan(loan_id):
    loan = Loan.query.get(loan_id)
    if loan:
        db.session.delete(loan)
        db.session.commit()
        logger.info('Loan ID {} deleted'.format(loan_id))
        return jsonify({'message': 'Loan deleted'}), 200
    return jsonify({'message': 'Loan not found'}), 404
