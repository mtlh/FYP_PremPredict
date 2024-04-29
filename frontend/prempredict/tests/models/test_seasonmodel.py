import uuid
from django.test import TestCase
from prempredict.models import PremSeasonInfo
from datetime import date
from django.utils import timezone

class PremSeasonInfoCRUDTest(TestCase):
    def setUp(self):
        self.season = PremSeasonInfo.objects.create(active=False,currentMatchday=10,winner="Manchester City",startDate=date(2023, 8, 15),endDate=date(2024, 5, 22))

    def test_create_season(self):
        # Create a season
        created_season = PremSeasonInfo.objects.create(active=True,currentMatchday=5,winner="Liverpool",startDate=date(2022, 8, 10),endDate=date(2023, 5, 20))
        self.assertIsNotNone(created_season.id)

    def test_default_values(self):
        # Create a season without specifying certain attributes
        season = PremSeasonInfo.objects.create()
        self.assertEqual(season.active, False)
        self.assertEqual(season.currentMatchday, 1)  # Default value
        self.assertEqual(season.winner, "null")  # Default value
        # Get the current datetime with timezone information
        current_datetime = timezone.now()
        # Assuming 'season' is your object with a 'startDate' and 'endDate' field
        self.assertEqual(season.startDate.day, current_datetime.day)  # Check the day
        self.assertEqual(season.startDate.month, current_datetime.month)  # Check the month
        self.assertEqual(season.startDate.year, current_datetime.year)  # Check the year
        self.assertEqual(season.endDate.day, current_datetime.day)  # Check the day
        self.assertEqual(season.endDate.month, current_datetime.month)  # Check the month
        self.assertEqual(season.endDate.year, current_datetime.year)  # Check the year

    def test_primary_key(self):
        # Retrieve the object from the database
        retrieved_obj = PremSeasonInfo.objects.get(id=self.season.id)
        # Check the type of the UUID field
        self.assertIsInstance(retrieved_obj.id, uuid.UUID)

    def test_select_season(self):
        # Select (retrieve) a season
        retrieved_season = PremSeasonInfo.objects.get(id=self.season.id)
        self.assertEqual(retrieved_season.id, self.season.id)

    def test_update_season(self):
        # Update a season
        updated_season = PremSeasonInfo.objects.get(id=self.season.id)
        updated_season.active = True
        updated_season.save()

        # Retrieve the updated season
        retrieved_season = PremSeasonInfo.objects.get(id=self.season.id)
        self.assertTrue(retrieved_season.active)

    def test_delete_season(self):
        # Delete a season
        PremSeasonInfo.objects.filter(id=self.season.id).delete()

        # Attempt to retrieve the deleted season
        with self.assertRaises(PremSeasonInfo.DoesNotExist):
            PremSeasonInfo.objects.get(id=self.season.id)
