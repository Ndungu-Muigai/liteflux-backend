import sib_api_v3_sdk
import os
from api import app
import requests
from api.models import OrderProduct

configuration=sib_api_v3_sdk.Configuration()
configuration.api_key["api-key"] = os.environ.get("SENDINBLUE_API_KEY")
api_instance=sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

def confirm_order(first_name, last_name, email, order_id):
    # Fetching the order from the backend 
    order_response = requests.get(f"https://api.litefluxent.com/client/orders/{order_id}")
    order = order_response.json()

    # Ensure 'order_products' is available in the order dictionary
    order_products = order.get('order_products', [])

    # Initialize product details list
    product_details_list = []

    # Mapping through the order products
    for order_product in order_products:
        product_id = order_product.get('id')
        if product_id:
            # Fetching the product details from the products API
            product_response = requests.get(f"https://products.litefluxent.com/products/{product_id}")
            product = product_response.json()
            product_details_list.append(product)

    subject = "Order confirmation"
    sender = {"name": app.config["SENDER_NAME"], "email": app.config["SENDER_EMAIL"]}

    # Create the product summary table rows
    product_summary_rows = "".join(
        f"<tr><td>{product.get('name')}</td><td>{product.get('quantity')}</td><td>{product.get('price')}</td></tr>"
        for product in product_details_list
    )

    email_content = f"""
    <p>Dear {first_name} {last_name},</p>
    <p>Your order with ID {order_id} has been successfully created</p>
    <p>We will inform you once the product is ready for delivery</p>

    <table>
        <thead>
            <tr>
                <th colspan='3'>Product summary</th>
            </tr>
        </thead>
        <tbody>
            {product_summary_rows}
        </tbody>
    </table>
    <b>NB: This is a system generated email. Please DO NOT reply to this email thread.</b>
    """

    to = [{"name": f"{first_name} {last_name}", "email": email}]
    send_email = sib_api_v3_sdk.SendSmtpEmail(to=to, html_content=email_content, sender=sender, subject=subject)

    api_instance.send_transac_email(send_email)