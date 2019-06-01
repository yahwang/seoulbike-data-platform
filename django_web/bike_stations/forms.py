from django import forms
from .models import BikeLoc

class BikeLocForm(forms.ModelForm):
    class Meta:
        model = BikeLoc
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super(BikeLocForm, self).__init__(*args, **kwargs)
        # /edit 활용 시 st_id를 수정 못하게 하는 코드
        instance = getattr(self, 'instance', None)
        if instance and instance.st_id:
            self.fields['st_id'].widget.attrs['readonly'] = "readonly"
            #self.fields['st_id'].required = False