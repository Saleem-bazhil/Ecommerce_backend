import razorpay
from django.conf import settings
from rest_framework.serializers import ValidationError
from rest_framework import status


class RazorpayClient:
    def __init__(self):
        if not settings.RAZORPAY_KEY_ID or not settings.RAZORPAY_KEY_SECRET:
            raise ValidationError(
                {
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": "Razorpay keys not configured"
                }
            )

        self.client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

    def create_order(self, amount, currency="INR"):
        try:
            data = {
                "amount": int(float(amount) * 100),  # ✅ paise
                "currency": currency,
                "payment_capture": 1,
            }

            return self.client.order.create(data=data)

        except Exception as e:
            raise ValidationError(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": str(e)
                }
            )

    def verify_payment_signature(self, razorpay_order_id, razorpay_payment_id, razorpay_signature):
        try:
            return self.client.utility.verify_payment_signature(
                {
                    "razorpay_order_id": razorpay_order_id,
                    "razorpay_payment_id": razorpay_payment_id,
                    "razorpay_signature": razorpay_signature,
                }
            )

        except Exception as e:
            raise ValidationError(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": str(e)
                }
            )
