

def sms_body_template(name,product,tracking_id,tracking_link,invoice_link):
    body = """Hi {name}!, We welcome you to the world of Peepl. Your order {product} has/have been shipped. 
    \nTracking ID: {tracking_id}
    \nTracking link: https://www.xpressbees.com/track
    \nE-invoice:{invoice_link}""".format(name=name,product=product,tracking_id=tracking_id,invoice_link=invoice_link)
    return body

def email_body_template(name,product,tracking_id,tracking_link,invoice_link):
    body = """Hi {name}!, We welcome you to the world of Peepl. Your order {product} has/have been shipped. 
    \nTracking ID: {tracking_id}
    \nTracking link: https://www.xpressbees.com/track
    \nE-invoice:{invoice_link}""".format(name=name,product=product,tracking_id=tracking_id,invoice_link=invoice_link)
    return body