import sib_api_v3_sdk
import os
from api import app
import requests
from api.models import OrderProduct

configuration=sib_api_v3_sdk.Configuration()
configuration.api_key["api-key"] = os.environ.get("SENDINBLUE_API_KEY")
api_instance=sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

def confirm_order(first_name, last_name, email, order_id):
    products_response=requests.get("https://products.litefluxent.com/products")
    products=products_response.json()

    order_products=[]

    order_response=requests.get(f"https://api.litefluxent.com/client/orders/{order_id}")

    subject="Order confirmation"
    sender={"name": app.app.config["SENDER_NAME"], "email": app.app.config["SENDER_EMAIL"]}
    email_content=f"""
    <p>Dear {first_name} {last_name},</p>
    <p>Your order with ID {order_id} has been successfully created</p>
    {order_response}
    <p>We will inform you once the product is ready for delivery</p>
    <b>NB:This is an system generated email. Please DO NOT reply to this email thread.</b>
    """

    to= [{"name": f"{first_name} {last_name}", "email": email}]

    send_email=sib_api_v3_sdk.SendSmtpEmail(to=to, html_content=email_content,sender=sender, subject=subject)

    api_instance.send_transac_email(send_email)