import sib_api_v3_sdk
import os
from api import app
import requests

response=requests.get("https://products.litefluxent.com/products")
products=response.json()

order_products=[]

configuration=sib_api_v3_sdk.Configuration()
configuration.api_key["api-key"] = os.environ.get("SENDINBLUE_API_KEY")
api_instance=sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

def confirm_order(first_name, last_name, email, product_ids, order_id):
    for id in product_ids:
        id=int(id)
        order_products.append(products[id])
    
    subject="Order confirmation"
    sender={"name": app.app.config["SENDER_NAME"], "email": app.app.config["SENDER_EMAIL"]}
    email_content=f"""
    <p>Dear {first_name} {last_name},</p>
    <p>Your order with ID {order_id} has been successfully created</p>
    <p>We will inform you once the product is ready for delivery</p>
    {order_products}
    <b>NB:This is an system generated email. Please DO NOT reply to this email thread.</b>
    """

    to= [{"name": f"{first_name} {last_name}", "email": email}]

    send_email=sib_api_v3_sdk.SendSmtpEmail(to=to, html_content=email_content,sender=sender, subject=subject)

    api_instance.send_transac_email(send_email)