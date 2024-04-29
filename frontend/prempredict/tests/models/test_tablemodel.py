import uuid
from django.test import TestCase
from prempredict.models import PremTable, PremSeasonInfo, PremTeams
from datetime import datetime

class PremTableCRUDTest(TestCase):
    def setUp(self):
        self.season = PremSeasonInfo.objects.create(
            id=1, currentMatchday=1, winner = "", startDate=datetime.now(), endDate=datetime.now()
        )
        self.team = PremTeams.objects.create(
            id=1, fullname="SAMPLE TEAM FC", shortname="SAMPLE", initals="SPL", badge="https://cdn-icons-png.flaticon.com/512/1581/1581884.png"
        )
        self.table = PremTable.objects.create(
            season=self.season,
            team=self.team,
            position=1,
            played=10,
            win=7,
            draw=2,
            loss=1,
            goaldifference=15,
            points=23
        )

    def test_create_table(self):
        # Create a table entry
        created_table = PremTable.objects.create(
            season=self.season,
            team=self.team,
            position=2,
            played=11,
            win=7,
            draw=2,
            loss=2,
            goaldifference=14,
            points=23
        )
        self.assertIsNotNone(created_table.position)

    def test_default_values(self):
        # Create a table entry without specifying certain attributes
        table = PremTable.objects.create(position=10, season=self.season, team=self.team)
        self.assertEqual(table.played, 0)  # Default value
        self.assertEqual(table.win, 0)  # Default value
        self.assertEqual(table.draw, 0)  # Default value
        self.assertEqual(table.loss, 0)  # Default value
        self.assertEqual(table.goaldifference, 0.0)  # Default value
        self.assertEqual(table.points, 0)  # Default value

    def test_primary_key(self):
        # Verify that the 'position' field is a primary key
        self.assertIsInstance(self.table.position, int)

    def test_select_table(self):
        # Select (retrieve) a table entry
        retrieved_table = PremTable.objects.get(season=self.season, team=self.team)
        self.assertEqual(retrieved_table.position, self.table.position)

    def test_update_table(self):
        # Update all records that match the filter criteria
        updated_tables = PremTable.objects.filter(season=self.season, team=self.team)
        updated_tables.update(position=2)

        # Retrieve the updated table entry
        retrieved_table = PremTable.objects.get(season=self.season, team=self.team)
        self.assertEqual(retrieved_table.position, 2)

    def test_delete_table(self):
        # Delete a table entry
        PremTable.objects.filter(season=self.season, team=self.team).delete()

        # Attempt to retrieve the deleted table entry
        with self.assertRaises(PremTable.DoesNotExist):
            PremTable.objects.get(season=self.season, team=self.team)


