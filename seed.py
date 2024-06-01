from api.app import app
from api.models import Admins, db, Product, ProductImage, Order, OrderProduct

if __name__ == "__main__":
    with app.app_context():
        print("Seed file")

        new_admin = Admins(first_name="Samuel", last_name="Muigai", email="muigaisam65@gmail.com", phone="+254707251073", password="abc1234")
        db.session.add(new_admin)
        db.session.commit()

        # Uncomment the following lines to add more seed data as needed
        # product = Product.query.filter_by(id=1).first()

        # new_order = Order(first_name="Wairimu", last_name="Muigai", delivery_address="Kiambu town", amount=1000, email="test@test.com", phone="254745416760")

        # db.session.add(new_order)
        # db.session.commit()

        # new_order_product = OrderProduct(order_id=new_order.id, product=product, quantity=2)
        # db.session.add(new_order_product)

        # Admins.query.delete()
        # ProductImage.query.delete()
        # Order.query.delete()
        # OrderProduct.query.delete()
        # Product.query.delete()
        db.session.commit()
