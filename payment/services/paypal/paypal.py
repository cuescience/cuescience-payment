from payment.models import PayPalPayment
import paypalrestsdk
from django.conf import settings

__author__ = 'pirat'


class Transaction(object):
    def __init__(self, total=0, item_list=None):
        self.item_list = item_list or []
        self.total = total

    def to_dict(self):
        item_list_dict = {"items": list([item.to_dict() for item in self.item_list])}

        result = {
            "transactions": [{
                                 "item_list": item_list_dict,
                                 "amount": {
                                     "total": "{0}".format(self.total),
                                     "currency": "EUR"
                                 }
                             }]
        }

        return result


class Item(object):
    def __init__(self, name, price, quantity, currency, sku=""):
        self.sku = sku
        self.name = name
        self.price = price
        self.quantity = quantity
        self.currency = currency

    def to_dict(self):
        result = {
            "sku": self.sku,
            "name": self.name,
            "price": "{0}".format(self.price),
            "quantity": self.quantity,
            "currency": self.currency
        }
        return result


class CreatePaymentResult(object):
    def __init__(self, paypal_payment_db, payment):
        self.paypal_payment_db = paypal_payment_db
        self.payment = payment


class PayPalService(object):
    def __init__(self, currency="EUR"):
        self.currency = currency
        self.client_id = settings.PAYPAL_CLIENT_ID
        self.client_secret = settings.PAYPAL_CLIENT_SECRET

    def configure(self):
        paypalrestsdk.configure({
            "mode": settings.PAYPAL_API_MODE,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        })

    def create_payment(self, transaction, domain, next="/"):

        paypal_payment = PayPalPayment()
        paypal_payment.save()

        result_dict = {
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": "http://{0}/payment/{1}/success/?next={2}".format(domain, paypal_payment.pk, next),
                "cancel_url": "http://{0}/payment/{1}/cancel/?next={2}".format(domain, paypal_payment.pk, next),
            },
        }
        result_dict.update(transaction.to_dict())
        self.configure()

        print result_dict

        payment = paypalrestsdk.Payment(result_dict)
        payment.create()
        if not payment.error:
            paypal_payment.paypal_payment_id = payment.id
            for link in payment.links:
                if link.method == "REDIRECT":
                    paypal_payment.approval_url = link.href
        paypal_payment.save()

        return CreatePaymentResult(paypal_payment, payment)

    def execute_payment(self, payment_id, payer_id):
        self.configure()
        payment = paypalrestsdk.Payment.find(payment_id)
        payment.execute({"payer_id": payer_id})
        return payment
