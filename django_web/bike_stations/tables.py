import django_tables2 as tables
from django.utils.html import mark_safe, format_html
from django.urls import reverse
from .models import BikeLoc

edit_icon = '<a href="{}" class="btn-floating btn-small waves-effect waves-light green" style="float:inherit"><i class="material-icons">edit</i></a>'
del_icon = '<a href="{}" class="delete btn-floating btn-small waves-effect waves-light red" style="float:inherit"><i class="material-icons">delete</i></a>'
class EtcColumn(tables.Column):
    # accessor로 지정된 컬럼의 값이 value로 입력된다.
    '''
    attrs = {
        'td': {
            'data-st-id':lambda record: record.st_id
            }
        }
    '''
    def render(self, value):
        return format_html('<div class="row">{} {}</div>', 
                            mark_safe(edit_icon.format(reverse('st_list_edit', kwargs={'pk':value}))), 
                            mark_safe(del_icon.format(reverse('st_list_delete', kwargs={'pk':value})))
                            )
        
class BikeLocTable(tables.Table):
    etc = EtcColumn(accessor='st_id', verbose_name="")
    class Meta:
        model = BikeLoc
        fields = ('st_id','st_name','st_cradle','st_addr','st_lat','st_lon','st_gu','etc')
        template_name = 'django_tables2/table.html'
        attrs={'class':'highlight centered'}