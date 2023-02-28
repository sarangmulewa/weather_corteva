from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Station(models.Model):
    modified = models.DateTimeField(_('Modified'), default=timezone.now)
    name = models.CharField(_("Station Name"), unique=True, max_length=50)
    created = models.DateTimeField(_('Created'), default=timezone.now, editable=False)

    class Meta:
        ordering = ('-name',)
        get_latest_by = 'modified'

    def __str__(self):
        return f'{self.id}:{self.name}'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Station, self).save(*args, **kwargs)


class Weather(models.Model):
    date = models.CharField(_("Date"), max_length=20)
    precipitation = models.IntegerField(_("Precipitation"))
    max_temp = models.IntegerField(_("Maximum temperature"))
    min_temp = models.IntegerField(_("Minimum temperature"))
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='records', null=True, blank=True)

    modified = models.DateTimeField(_('Modified'), default=timezone.now)
    created = models.DateTimeField(_('Created'), default=timezone.now, editable=False)

    class Meta:
        get_latest_by = 'modified'
        unique_together = ("date", "station")

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Weather, self).save(*args, **kwargs)


class Statistics(models.Model):
    avg_max_temp = models.FloatField(_("Average Maximum Temperature"))
    avg_min_temp = models.FloatField(_("Average minimum temperature"))
    year = models.CharField(_("Year of Stats"), max_length=20, null=True)
    total_acc_ppt = models.FloatField(_("Total accumulated precipitation"))
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='stats', null=True, blank=True)

    modified = models.DateTimeField(_('Modified'), default=timezone.now)
    created = models.DateTimeField(_('Created'), default=timezone.now, editable=False)

    class Meta:
        get_latest_by = 'year'
        verbose_name_plural = _("Statistics")

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Statistics, self).save(*args, **kwargs)
