import os
import sys
import time
import glob
import logging
import pandas as pd
from pathlib import Path

from django.db.models import Avg, Sum
from django.db.models.functions import Substr
from django.core.management.base import BaseCommand

from weather_app.models import Station, Weather, Statistics

os.makedirs(os.path.dirname("logs/info.log"), exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    handlers=[logging.FileHandler("logs/info.log"), logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)
logger.setLevel("INFO")


class Command(BaseCommand):
    help = 'Data Ingestion'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path', type=str, default='wx_data', help='Path to the directory containing weather data files'
        )

    def import_weather(self, path):
        """ This function is used to import & save wx_data into the Database """

        try:
            # Reading all files in path directory
            file_list = glob.glob(f"{path}/*.txt")
            weather = list()
            weather_records_dfs = []
            for file in file_list:
                # Creating or Fetching Station object
                station, created = Station.objects.get_or_create(name=Path(file).stem)
                station_id = station.id

                # Created DataFrame of CSV file
                df = pd.read_csv(file, sep="\t", header=None, names=["date", "max_temp", "min_temp", "precipitation"])

                # Filtered Existing data, if weather record already exists
                dates = df["date"].tolist()
                queryset = Weather.objects.filter(station_id=station_id, date__in=dates)

                # Remove already existing records from DataFrame
                already_exists_dates = list(map(int, queryset.values_list('date', flat=True)))
                already_exists = df[df['date'].isin(already_exists_dates)].index
                df = df.drop(already_exists)
                df["station_id"] = station_id
                weather_records_dfs.append(df)

            final_df = pd.concat(weather_records_dfs)
            # Appending records to list for bulk upload
            for i, row in final_df.iterrows():
                weather.append(Weather(
                    date=str(row['date']),
                    max_temp=int(row['max_temp']),
                    min_temp=int(row['min_temp']),
                    station_id=int(row['station_id']),
                    precipitation=int(row['precipitation']),
                ))

            # Bulk Creation of Weather data in batch of 5000
            Weather.objects.bulk_create(weather, batch_size=5000, ignore_conflicts=True)
            logger.info("Weather Data inserted successfully")
            logger.info(f"Total {len(weather)} weather records inserted")

        except Exception as e:
            logger.error(f"An error occurred while importing weather data: {e}")

    def set_stats(self):
        try:
            result = (
                Weather.objects.filter(
                    max_temp__gt=-9999,
                    min_temp__gt=-9999,
                    precipitation__gt=-9999,
                )
                .values("station_id", year=Substr("date", 1, 4))
                .annotate(
                    max_temp_avg=Avg("max_temp"),
                    min_temp_avg=Avg("min_temp"),
                    ppt_sum=Sum("precipitation"),
                )
            )

            create_stats, update_stats = [], []
            for res in result:
                qs = Statistics.objects.filter(station_id=res["station_id"], year=res["year"])
                if qs:
                    stats = qs.first()
                    stats.total_acc_ppt = res["ppt_sum"]
                    stats.avg_max_temp = res["max_temp_avg"]
                    stats.avg_min_temp = res["min_temp_avg"]
                    update_stats.append(stats)
                else:
                    create_stats.append(Statistics(
                        year=res["year"],
                        station_id=res["station_id"],
                        total_acc_ppt=res["ppt_sum"],
                        avg_max_temp=res["max_temp_avg"],
                        avg_min_temp=res["min_temp_avg"],
                    ))

            Statistics.objects.bulk_create(create_stats, batch_size=5000, ignore_conflicts=True)
            fields = ['avg_max_temp', 'avg_min_temp', 'total_acc_ppt']
            Statistics.objects.bulk_update(update_stats, fields=fields, batch_size=5000)
            logger.info("Weather statistics saved successfully")
            logger.info(f"{len(create_stats)} stats record created and {len(update_stats)} stats record updated")

        except Exception as e:
            logger.error(f"An error occurred while computing weather statistics: {e}")

    def handle(self, *args, **options):
        path = options['path']
        start_time = time.time()

        logger.info("Weather data ingestion started")
        self.import_weather(path)
        self.set_stats()

        logger.info(f"Total time taken: {(time.time() - start_time)} seconds")
