from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import RazorpayOrderSerializer, TranscationModelSerializer
from .main import RazorpayClient


class RazorpayOrderAPIView(APIView):
    """Create Razorpay order"""

    def post(self, request):
        serializer = RazorpayOrderSerializer(data=request.data)

        if serializer.is_valid():
            rz_client = RazorpayClient()  # ✅ MOVE HERE

            order_response = rz_client.create_order(
                amount=serializer.validated_data["amount"],
                currency=serializer.validated_data["currency"]
            )

            return Response(
                {
                    "status_code": status.HTTP_201_CREATED,
                    "message": "order created",
                    "data": order_response
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "bad request",
                "error": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class TransactionAPIView(APIView):
    """Verify payment & save transaction"""

    def post(self, request):
        serializer = TranscationModelSerializer(data=request.data)

        if serializer.is_valid():
            rz_client = RazorpayClient()  # ✅ MOVE HERE

            rz_client.verify_payment_signature(
                razorpay_payment_id=serializer.validated_data["payment_id"],
                razorpay_order_id=serializer.validated_data["order_id"],
                razorpay_signature=serializer.validated_data["signature"]
            )

            serializer.save()

            return Response(
                {
                    "status_code": status.HTTP_201_CREATED,
                    "message": "transaction created"
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "bad request",
                "error": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
