from listings.models import Listing, Booking, Review, Payment
from rest_framework import serializers

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'  

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['created_at']  # Assuming you want to prevent modification of created_at field


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['payment_date']  # Assuming you want to prevent modification of payment_date field
        extra_kwargs = {
            'transaction_id': {'validators': []}  # Assuming you want to allow custom transaction IDs
        }       