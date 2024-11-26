from flask import request, jsonify
from flask_cors import cross_origin
from flask_login import current_user

from app import app, db
from app.models import UserRent


@app.route("/api/v1/add_rent", methods=["POST"])
@cross_origin()
def add_rent():
    data = request.json

    if not data or 'car_id' not in data:
        return jsonify({"error": "Invalid data"}), 400

    new_rent = UserRent(
        user_id=current_user.id,
        car_id=data["car_id"]
    )
    try:
        db.session.add(new_rent)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Internal Server Error"}), 500

    return jsonify({"message": "Rent successfully", "rent": str(new_rent)}), 201


@app.route("/api/v1/stop_rent", methods=["POST"])
def stop_rent():
    data = request.json
    car = UserRent.query.get(data['rent_id'])

    if not data or 'rent_id' not in data:
        return jsonify({"error": "Invalid data"}), 400
    
    try:
        db.session.delete(car)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Internal Server Error"}), 500

    return jsonify({"message": "UnRent successfully", "rent": "Отсутствует данная аренда"}), 201
