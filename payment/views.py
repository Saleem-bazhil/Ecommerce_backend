from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .serializers import RazorpayOrderSerializer, TranscationModelSerializer
from .main import RazorpayClient


class RazorpayOrderAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RazorpayOrderSerializer(data=request.data)

        if serializer.is_valid():
            rz_client = RazorpayClient()

            order = rz_client.create_order(
                amount=serializer.validated_data["amount"],
                currency=serializer.validated_data["currency"]
            )

            return Response({
                "status_code": status.HTTP_201_CREATED,
                "message": "order created",
                "data": order
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "error": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class TransactionAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TranscationModelSerializer(data=request.data)

        if serializer.is_valid():
            rz_client = RazorpayClient()

            rz_client.verify_payment_signature(
                razorpay_order_id=serializer.validated_data["order_id"],
                razorpay_payment_id=serializer.validated_data["payment_id"],
                razorpay_signature=serializer.validated_data["signature"]
            )

            serializer.save()

            return Response({
                "status_code": status.HTTP_201_CREATED,
                "message": "transaction created"
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "error": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
