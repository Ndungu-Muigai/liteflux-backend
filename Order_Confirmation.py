import sib_api_v3_sdk
import os
from api import app
import requests
from api.models import OrderProduct

configuration=sib_api_v3_sdk.Configuration()
configuration.api_key["api-key"] = os.environ.get("SENDINBLUE_API_KEY")
api_instance=sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

def confirm_order(first_name, last_name, email, order_id, new_order_id):
    # Fetching the order from the backend 
    order_response = requests.get(f"https://api.litefluxent.com/client/orders/{order_id}")
    order = order_response.json()

    # Getting the order's products if 'order_products' key exists
    order_products = order.get('order_products', [])

    # Initialize an empty list to store product details
    product_details = []

    # Mapping through the order products
    for order_product in order_products:
        # Fetching the product details from the products API
        product_response = requests.get(f"https://products.litefluxent.com/products/{order_product['product_id']}")
        product = product_response.json()
        product_details.append(product)

    subject = f"Order confirmation- {new_order_id}"
    sender = {"name": app.app.config["SENDER_NAME"], "email": app.app.config["SENDER_EMAIL"]}
    email_content = f"""
    <p>Dear {first_name} {last_name},</p>
    <p>Your order with ID {new_order_id} has been successfully created</p>
    <p>We will inform you once the product is ready for delivery</p>

    <table>
        <thead>
            <tr>
                <th>Product Image</th>
                <th>Product Name</th>
                <th>Quantity</th>
            </tr>
        </thead>
        <tbody>
            {''.join([f"<tr><td><img src='{product['image']}' alt={product['name']} width='100' height='100'></td><td>{product['name']}</td><td>{order_product['quantity']}</td></tr>" for order_product, product in zip(order_products, product_details)])}
        </tbody>
    </table>
    <b>NB: This is a system-generated email. Please DO NOT reply to this email thread.</b>
    """

    to = [{"name": f"{first_name} {last_name}", "email": email}]

    send_email = sib_api_v3_sdk.SendSmtpEmail(to=to, html_content=email_content, sender=sender, subject=subject)

    api_instance.send_transac_email(send_email)
