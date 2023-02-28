from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter

from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

# from django.db.models import F
# from rest_framework.response import Response
# from rest_framework.mixins import ListModelMixin
# from rest_framework.viewsets import GenericViewSet

from .models import Weather, Statistics
from .serializers import WeatherSerializers, StatisticsSerializers


# Model Mixins based Class views

# def get_page_limits(page, page_size):
#     return page * page_size - page_size, page * page_size
#
#
# class WeatherViewSet(GenericViewSet, ListModelMixin):
#     queryset = Weather.objects.all()
#     serializer_class = WeatherSerializers
#
#     def list(self, request, *args, **kwargs):
#         try:
#             date = request.GET.get("date", "")
#             station = request.GET.get("station", "")
#             page = int(request.GET.get("page", 1))
#             page_size = int(request.GET.get("page_size", 10))
#             first, last = get_page_limits(page, page_size)
#             queryset = Weather.objects.all()
#             if station:
#                 queryset = queryset.filter(station__name=station)
#             if date:
#                 queryset = queryset.filter(date=date)
#
#             queryset = queryset.order_by('-date')
#             total = queryset.count()
#             result = queryset[first:last].annotate(station_name=F('station__name')).values(
#                 'date', 'station_name', 'max_temp', 'min_temp', 'precipitation', 'modified'
#             )
#             return Response({"page": page, "page_size": page_size, "total": total, "result": result}, status=200)
#         except Exception as error:
#             return Response({"message": error}, status=400)
#
#
# class StatsViewSet(GenericViewSet, ListModelMixin):
#     queryset = Statistics.objects.all()
#     serializer_class = StatisticsSerializers
#
#     def list(self, request, *args, **kwargs):
#         try:
#             year = request.GET.get("year", "")
#             station = request.GET.get("station", "")
#             page = int(request.GET.get("page", 1))
#             page_size = int(request.GET.get("page_size", 10))
#             first, last = get_page_limits(page, page_size)
#             queryset = Statistics.objects.all()
#             if station:
#                 queryset = queryset.filter(station__name=station)
#             if year:
#                 queryset = queryset.filter(year=year)
#
#             queryset = queryset.order_by('-year')
#             total = queryset.count()
#             result = queryset[first:last].annotate(station_name=F('station__name')).values(
#                 'year', 'station_name', 'avg_max_temp', 'avg_min_temp', 'total_acc_ppt', 'modified'
#             )
#             return Response({"page": page, "page_size": page_size, "total": total, "result": result}, status=200)
#         except Exception as error:
#             return Response({"message": error}, status=400)


# APIView based class views

class WeatherList(ListAPIView):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializers
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering = ('-date',)
    filterset_fields = ["date", "station__name"]


class StatsList(ListAPIView):
    queryset = Statistics.objects.all()
    serializer_class = StatisticsSerializers
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering = ('-year',)
    filterset_fields = ["year", "station__name"]
