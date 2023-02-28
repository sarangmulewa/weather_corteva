from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from weather_app.models import Statistics, Weather, Station


class WeatherTestCase(APITestCase):
    """
    Test Weather Endpoints
    """

    def setUp(self):
        super().setUp()
        self.station = Station.objects.create(name="USC00110072")
        self.weather = Weather.objects.create(
            station=self.station, date="20141235", max_temp=-122, min_temp=-217, precipitation=12
        )

    def test_get_weather(self):
        response = self.client.get(reverse("weather-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 1)
        self.assertEqual(response.data["count"], 1)


class StatsTestCase(APITestCase):
    """
    Test Stats Endpoints
    """

    def setUp(self):
        super().setUp()
        self.station = Station.objects.create(name="USC00110072")
        self.stats = Statistics.objects.create(
            year='2022-01-01',
            station=self.station,
            avg_max_temp=20.0,
            avg_min_temp=30.0,
            total_acc_ppt=10.0
        )

    def test_get_stats(self):
        response = self.client.get(reverse("stats-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 1)
        self.assertEqual(response.data["count"], 1)
