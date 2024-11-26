from app import db, app
from app.models import Car


def add_db(brand, price, photo_path):
    car = Car(brand=brand, price=price, photo_path=photo_path)
    with app.app_context():
        try:
            db.session.add(car)
            db.session.commit()
            print("succefull")
        except Exception:
            db.session.rollback()
            print("error")

def main():
    cars = {
        1: {
            "brand": "Ford Mustang VI",
            "price": 21,
            "photo_path": "images/cars/mustang.png"
        },
        2: {
            "brand": "Mercedes-AMG С43",
            "price": 11,
            "photo_path": "images/cars/mersedesc.png"
        }
    }
    for j in range(15):
        for i in cars:
            add_db(brand=cars[i]["brand"], price=cars[i]["price"], photo_path=cars[i]["photo_path"])
    
if __name__ == "__main__":
    main()
