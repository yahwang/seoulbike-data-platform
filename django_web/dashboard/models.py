from django.db import models

class BikeParkingLog(models.Model):
    id = models.AutoField(primary_key=True)
    st_id = models.IntegerField(verbose_name='CONTENT_ID')
    st_cradle = models.IntegerField(verbose_name='CRADLE_COUNT')
    st_parking = models.IntegerField(verbose_name='PARKING_COUNT')
    log_time = models.DateTimeField()

    class Meta:
        verbose_name = 'Bike Log'
        verbose_name_plural = 'Bike Logs'
        ordering=['st_id']

    def __str__(self):
        return '{}'.format(self.st_id)