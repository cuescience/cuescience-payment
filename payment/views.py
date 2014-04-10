from payment.models import PayPalPayment
from payment.services.paypal import paypal

__author__ = 'i.bauer'

from django.shortcuts import redirect


paypal_service = paypal.PayPalService()


def success_view(request, payment_id):
    paypal_payment = PayPalPayment.objects.get(pk=payment_id)
    payer_id = request.GET.get("PayerID", None)
    if not payer_id:
        raise Exception
    payment = paypal_service.execute_payment(paypal_payment.paypal_payment_id, payer_id)
    if not payment.error:
        paypal_payment.approved = True
        paypal_payment.save()

    return redirect("/")


def cancel_view(request, payment_id):
    paypal_payment = PayPalPayment.objects.get(pk=payment_id)
    payer_id = request.GET.get("PayerID", None)
    paypal_payment.status = "canceled"
    paypal_payment.save()

    return redirect("/")