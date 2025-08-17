# listings/management/commands/seed.py
from decimal import Decimal
from datetime import date, timedelta
import random
from django.core.management.base import BaseCommand
from django.db import transaction
from listings.models import Listing, Booking, Review  

TITLES = [
    "Cozy Studio Near CBD", "Beachfront Apartment", "Mountain Cabin Retreat",
    "Modern Loft in City Center", "Lake House Getaway", "Country Cottage",
]
DESC_SNIPPETS = [
    "Fast Wi-Fi, great views.", "Quiet neighborhood, close to transit.",
    "Fully equipped kitchen.", "Walk to shops and restaurants.",
    "Ideal for remote work.", "Family-friendly space.",
]
USER_NAMES = [
    "Kimani", "Achieng", "Mwangi", "Otieno", "Wanjiru",
    "Abdi", "Kiptoo", "Mutiso", "Wambui", "Chebet",
]

def rand_price():
    # 1,000.00 to 20,000.00
    return Decimal(f"{random.randint(1000, 20000)}.00")

def rand_desc():
    return " ".join(random.sample(DESC_SNIPPETS, k=random.randint(2, 4)))

def rand_user():
    return random.choice(USER_NAMES)

class Command(BaseCommand):
    help = "Seed the database with demo Listings, Bookings, and Reviews."

    def add_arguments(self, parser):
        parser.add_argument("--listings", type=int, default=15, help="How many listings to create")
        parser.add_argument("--purge", action="store_true", help="Delete existing data first")

    @transaction.atomic
    def handle(self, *args, **opts):
        if opts["purge"]:
            self.stdout.write("Purging existing Reviews, Bookings, Listings…")
            Review.objects.all().delete()
            Booking.objects.all().delete()
            Listing.objects.all().delete()

        n_listings = opts["listings"]
        created_listings = 0
        created_bookings = 0
        created_reviews = 0

        for _ in range(n_listings):
            title = random.choice(TITLES) + f" #{random.randint(100, 999)}"
            listing = Listing.objects.create(
                title=title,
                description=rand_desc(),
                price=rand_price(),
            )
            created_listings += 1

            # Reviews: 1–5 per listing
            for _ in range(random.randint(1, 5)):
                Review.objects.create(
                    listing=listing,
                    user=rand_user(),
                    rating=random.randint(1, 5),
                    comment=random.choice(["", rand_desc()]),
                )
                created_reviews += 1

            # Bookings: 0–3 per listing (non-overlapping, future dates)
            start = date.today() + timedelta(days=random.randint(1, 45))
            for _ in range(random.randint(0, 3)):
                length = random.randint(1, 10)
                end = start + timedelta(days=length)
                Booking.objects.create(
                    listing=listing,
                    user=rand_user(),
                    start_date=start,
                    end_date=end,
                )
                created_bookings += 1
                # next window after a small gap
                start = end + timedelta(days=random.randint(1, 7))

        self.stdout.write(self.style.SUCCESS(
            f"Seed complete: {created_listings} listings, "
            f"{created_bookings} bookings, {created_reviews} reviews."
        ))
