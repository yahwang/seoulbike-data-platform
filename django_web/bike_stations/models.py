from django.db import models

class BikeLoc(models.Model):
    st_id = models.IntegerField(verbose_name='CONTENT_ID', primary_key=True)
    st_name = models.CharField(max_length=100,verbose_name='CONTENT_NM')
    st_cradle = models.IntegerField(verbose_name='CRADLE_COUNT')
    st_addr = models.CharField(max_length=300, verbose_name='ADDRESS')
    st_lat = models.FloatField(verbose_name='LATITUDE')
    st_lon = models.FloatField(verbose_name='LONGITUDE')
    st_gu = models.CharField(max_length=20, verbose_name='ADDR_GU')

    class Meta:
        verbose_name = 'Bike Station'
        verbose_name_plural = 'Bike Stations'
        ordering=['st_id']

    def __str__(self):
        return '{} - {}'.format(self.st_id, self.st_name)