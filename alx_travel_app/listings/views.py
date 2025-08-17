from django.shortcuts import render

from listings.serializers import ListingSerializer, BookingSerializer, ReviewSerializer
from listings.models import Listing, Booking, Review, Payment


from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

import uuid
from django.conf import settings


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class PaymentViewSet(viewsets.ViewSet):

    @action(detail=True, methods=['post'], url_path='initiate')
    def initiate_payment(self, request, pk=None):
        try:
            booking = Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=404)

        tx_ref = str(uuid.uuid4())
        chapa_url = "https://api.chapa.co/v1/transaction/initialize"
        headers = {"Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"}

        payload = {
            "amount": str(booking.listing.price),
            "currency": "ETB",
            "email": booking.user + "@example.com",  # replace with real email
            "first_name": booking.user,
            "last_name": "Guest",
            "tx_ref": tx_ref,
            "callback_url": "http://localhost:8000/api/payments/verify/",
            "return_url": "http://localhost:8000/payment-success/",
            "customization": {
                "title": "Booking Payment",
                "description": "Pay for your listing"
            }
        }

        response = requests.post(chapa_url, json=payload, headers=headers)
        if response.status_code == 200:
            checkout_url = response.json()["data"]["checkout_url"]
            Payment.objects.create(
                booking=booking,
                amount=booking.listing.price,
                transaction_id=tx_ref,
                status="Pending"
            )
            return Response({"checkout_url": checkout_url})
        return Response({"error": "Payment initiation failed"}, status=400)

    @action(detail=False, methods=['get'], url_path='verify')
    def verify_payment(self, request):
        tx_ref = request.query_params.get("tx_ref")
        headers = {"Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"}
        url = f"https://api.chapa.co/v1/transaction/verify/{tx_ref}"

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()["data"]
            payment = Payment.objects.filter(transaction_id=tx_ref).first()
            if payment:
                payment.status = data["status"]
                payment.save()
                return Response({"status": data["status"]})
        return Response({"error": "Verification failed"}, status=400)
