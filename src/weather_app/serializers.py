from rest_framework import serializers

from .models import Weather, Statistics


class WeatherSerializers(serializers.ModelSerializer):
    station_name = serializers.SerializerMethodField()

    class Meta:
        model = Weather
        fields = ("date", "max_temp", "min_temp", "precipitation", "station_name", "modified")

    @staticmethod
    def get_station_name(obj):
        return obj.station.name


class StatisticsSerializers(serializers.ModelSerializer):
    station_name = serializers.SerializerMethodField()

    class Meta:
        model = Statistics
        fields = ("year", "total_acc_ppt", "avg_min_temp", "avg_max_temp", "station_name", "modified")

    @staticmethod
    def get_station_name(obj):
        return obj.station.name

