# from flask import Blueprint, request, jsonify
# from ..models import Food
# from ..db import db

# food_bp = Blueprint('food', __name__)

# @food_bp.route('', methods=['POST'])
# def create_food():
#     data = request.json
#     new_food = Food(
#         name=data['name'],
#         calories=data['calories'],
#         proteins=data['proteins'],
#         fats=data['fats'],
#         carbs=data['carbs']
#     )
#     db.session.add(new_food)
#     db.session.commit()
#     return jsonify({'message': 'Food added successfully!'}), 201

# @food_bp.route('', methods=['GET'])
# def get_foods():
#     foods = Food.query.all()
#     return jsonify([{
#         'id': food.id,
#         'name': food.name,
#         'calories': food.calories,
#         'proteins': food.proteins,
#         'fats': food.fats,
#         'carbs': food.carbs
#     } for food in foods])