import boto3 
import boto3.session
from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_cors import CORS
from werkzeug.utils import secure_filename
import uuid
from api.models import db, Order, Product, Admins, ProductImage
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from schema import AdminSchema, OrderSchema, ProductSchema
from datetime import timedelta
from Admin_creation import send_admin_credentials
from AutoGenerations.password import random_password
import os
import io

app = Flask(__name__)
# Initialize JWT
jwt = JWTManager(app)

# Importing the configurations
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "default_secret_key")
app.config["JWT_SECRET_KEY"] = app.config["SECRET_KEY"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://default:L2HzhlpSWwm9@ep-super-dawn-a4t58lz4.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require"

# Email sender configuration
app.config["SENDER_NAME"] = "Liteflux Enterprises"
app.config["SENDER_EMAIL"] = "info@litefluxent.com"
migrate = Migrate(app, db)
db.init_app(app)
CORS(app)

# Define DigitalOcean S3 bucket settings
AWS_ACCESS_KEY_ID =os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY =os.getenv("AWS_SECRET_ACCESS_KEY")
S3_REGION_NAME = "nyc3"
S3_BUCKET_NAME = "liteflux-product-images"
S3_ENDPOINT_URL='https://nyc3.digitaloceanspaces.com'
S3_BASE_URL = f"https://{S3_BUCKET_NAME}.{S3_REGION_NAME}.digitaloceanspaces.com/"

# session=session.Session()

# client=session.client( "s3",
#     region_name=S3_REGION_NAME,
#     aws_access_key_id=AWS_ACCESS_KEY_ID,
#     aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
#     endpoint_url='https://nyc3.digitaloceanspaces.com',
# )

session=boto3.session.Session()
s3_client=session.client("s3",region_name="nyc3",endpoint_url=S3_ENDPOINT_URL, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
@app.route("/")
def index():
    return {"message": "Welcome to the API"}

@app.route("/admin", methods=["POST"])
def admin_login():
    email = request.json["email"]
    password = request.json["password"]

    admin = Admins.query.filter(Admins.email == email).first()

    if not admin:
        return jsonify({"error": "No user exists with the given email"}), 404

    if admin.password != password:
        return jsonify({"error": "Incorrect Password"}), 404

    access_token = create_access_token(identity=admin.email)
    return make_response(jsonify(
        {
            "success": "Login successful",
            "access_token": access_token
        }), 200)

@app.route("/admin/dashboard", methods=["GET"])
@jwt_required()
def admin_dashboard():
    email = get_jwt_identity()
    admin = Admins.query.filter_by(email=email).first()
    if not admin:
        return jsonify({"error": "No user exists with the given email"}), 404
    
    admin_details = AdminSchema(only=("first_name", "last_name")).dump(admin)
    return make_response(jsonify(admin_details))

@app.route("/admin/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    products_data = ProductSchema(many=True).dump(products)
    return jsonify(products_data), 200

@app.route("/admin/products", methods=["POST"])
@jwt_required()
def add_product():
    email = get_jwt_identity()

    if not email:
        return make_response(jsonify({"error": "Kindly login to continue"}), 400)

    product_name = request.form["product_name"]
    product_description = request.form["product_description"]
    product_price = float(request.form["product_price"])
    product_quantity = int(request.form["product_quantity"])

    existing_product = Product.query.filter_by(name=product_name).first()
    if existing_product:
        return jsonify({"error": "Product already exists"}), 400

    # List to store image URLs to be added to the product
    image_urls = []

    # Getting the images from the form
    images = request.files.getlist("product_images")

    # Declaring the upload folder (using /tmp for writable space in cloud environments)
    upload_folder = "/tmp"

    # Looping through the images and saving them to the upload location
    for image in images:
        image_name = secure_filename(image.filename)
        unique_image_name = str(uuid.uuid1()) + "_" + image_name

        # Uploading the image locally
        image_path = os.path.join(upload_folder, unique_image_name)
        image.save(image_path)

        # Uploading the image to the S3 bucket
        try:
            # with open(image,"rb") as data:
            s3_client.Bucket(S3_BUCKET_NAME).put_object(Key=unique_image_name,Body=image_path)
            # s3_client.upload_fileobj(image_path, S3_BUCKET_NAME, unique_image_name)
            image_urls.append({"image_name": unique_image_name, "image_url": f"{S3_BASE_URL}{unique_image_name}"})
        except Exception as e:
            return make_response(jsonify({"error": f"Error uploading image to Digital Ocean: {e}"}), 404)

    try:
        new_product = Product(
            stock_quantity=product_quantity,
            name=product_name,
            description=product_description,
            price=product_price
        )
        db.session.add(new_product)
        db.session.commit()

        # Now add the images to the ProductImage table
        for img in image_urls:
            product_image = ProductImage(
                image_name=img["image_name"],
                image_url=img["image_url"],
                product_id=new_product.id
            )
            db.session.add(product_image)

        db.session.commit()  # Commit changes to the database after all images are uploaded successfully
        return make_response(jsonify({"success": "Product added successfully!"}), 201)
    except Exception as e:
        # Rollback the database transaction if an error occurs
        db.session.rollback()
        print(f"Error adding product to the database: {e}")
        return make_response(jsonify({"error": "Error adding product to the database. Try again later."}), 500)

@app.route("/admin/products/<int:product_id>", methods=["GET", "POST"])
@jwt_required()
def product_by_id(product_id):
    email = get_jwt_identity()

    if request.method == "GET":
        product = Product.query.filter_by(id=product_id).first()
        product_data = ProductSchema().dump(product)
        return jsonify(product_data)

    if request.method == "POST":
        product_images = ProductImage.query.filter_by(product_id=product_id).all()
        
        for image in product_images:            
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image.url))
            db.session.delete(image)

        product = Product.query.filter_by(id=product_id).first()

        product_name = request.form["product_name"]
        product_description = request.form["product_description"]
        product_price = float(request.form["product_price"])
        product_quantity = int(request.form["product_quantity"])
        images = request.files.getlist("product_images")

        for image in images:
            image_file_name = secure_filename(image.filename)
            unique_file_name = str(uuid.uuid1()) + "_" + image_file_name
            image.save(os.path.join(f"{app.config['UPLOAD_FOLDER']}", unique_file_name))
            image = ProductImage(product_id=product_id, url=unique_file_name)
            db.session.add(image)

        product.name = product_name
        product.description = product_description
        product.price = product_price
        product.stock_quantity = product_quantity

        db.session.commit()

        return jsonify({"success": "Product updated successfully!"}), 200

@app.route("/admin/orders", methods=["GET"])
@jwt_required()
def orders():
    email = get_jwt_identity()
    orders = Order.query.all()
    orders_details = OrderSchema(only=("id", "first_name", "last_name", "delivery_address", "status")).dump(orders, many=True)
    return make_response(jsonify(orders_details))

@app.route("/admin/orders/<int:order_id>", methods=["GET", "POST"])
@jwt_required()
def order_by_id(order_id):
    email = get_jwt_identity()

    if request.method == "GET":
        order = Order.query.filter_by(id=order_id).first()
        order_details = OrderSchema().dump(order)
        return make_response(jsonify(order_details))

    if request.method == "POST":
        status = request.json.get("status")

        order = Order.query.filter_by(id=order_id).first()

        if not order:
            return jsonify({"error": "The order being updated doesn't exist"}), 404
        
        order.status = status
        db.session.commit()

        return jsonify({"success": "Order updated successfully"}), 200

@app.route("/admin/all-admins", methods=["GET", "POST"])
@jwt_required()
def all_admins():
    email = get_jwt_identity()

    if request.method == "GET":
        admins = Admins.query.all()
        admins_details = AdminSchema().dump(admins, many=True)
        return make_response(jsonify(admins_details), 200)

    if request.method == "POST":
        first_name = request.json["first_name"]
        last_name = request.json["last_name"]
        email = request.json["email"]
        phone_number = request.json["phone"]

        admin = Admins.query.filter(Admins.email == email).first()

        if admin:
            return jsonify({"error": "An account with the given email already exists"}), 400
        
        password = random_password()
        new_admin = Admins(first_name=first_name, email=email, phone=phone_number, last_name=last_name, password=password)

        send_admin_credentials(last_name=last_name, email=email, first_name=first_name, password=password)
        db.session.add(new_admin)
        db.session.commit()

        return make_response(jsonify({"success": "Account created successfully"}), 201)

@app.route("/admin/delete-admin/<int:admin_id>", methods=["DELETE"])
@jwt_required()
def delete_admin(admin_id):
    email = get_jwt_identity()
    
    admin = Admins.query.filter_by(id=admin_id).first()

    if admin:
        db.session.delete(admin)
        db.session.commit()
        return jsonify({"success": "Account deleted successfully"}), 200
    else:
        return jsonify({"error": "Account could not be found"}), 404

@app.route("/admin/profile", methods=["GET", "POST"])
@jwt_required()
def profile():
    email = get_jwt_identity()

    if request.method == "GET":
        admin = Admins.query.filter_by(email=email).first()

        if not admin:
            return jsonify({"error": "Account could not be found!"}), 404
        
        admin_details = AdminSchema().dump(admin)
        return make_response(jsonify(admin_details))

    if request.method == "POST":
        admin = Admins.query.filter_by(email=email).first()

        if not admin:
            return jsonify({"error": "The admin does not exist!"}), 404
        
        new_password = request.json["new_password"]
        confirm_password = request.json["confirm_password"]

        if new_password != confirm_password:
            return jsonify({"error": "The passwords do not match"}), 400
        
        elif new_password == admin.password:
            return jsonify({"error": "The new password cannot be the same as the old password"}), 400
        
        admin.password = new_password
        db.session.commit()

        return jsonify({"success": "Password updated successfully"}), 200

@app.route("/admin/logout", methods=["GET"])
@jwt_required()
def logout():
    return jsonify({"success": "Logged out successfully"}), 200

if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
