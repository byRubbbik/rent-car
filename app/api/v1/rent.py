from flask import request, jsonify
from flask_cors import cross_origin

from app import app, db
from app.models import Car, UserRent


@app.route('/api/v1/add_car', methods=['POST'])
@cross_origin() 
def add_book():
    data = request.json
    if not data or 'brand' not in data or 'price' not in data or 'photo_path' not in data:
        return jsonify({"error": "Invalid data"}), 400

    new_car = Car(
        brand=data['brand'],
        price=data['price'],
        photo_path=data['photo_path']
    )

    db.session.add(new_car)
    db.session.commit()
    
    return jsonify({"message": "Car successfully", "car": str(new_car)}), 201


@app.route("/api/v1/add_rent", methods=["POST"])
@cross_origin()
def add_rent():
    data = request.json
    if not data or 'user_id' not in data or 'car_id':
        return jsonify({"error": "Invalid data"}), 400

    new_rent = UserRent(
        user_id=data['user_id'],
        car_id=data["car_id"]
    )
    try:
        db.session.add(new_rent)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Internal Server Error"}), 500

    return jsonify({"message": "Rent successfully", "rent": str(new_rent)}), 201
