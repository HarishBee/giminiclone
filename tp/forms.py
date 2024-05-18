from django import forms
from tp.models import register,forgot,password,Script



class regform(forms.ModelForm):
    class Meta:
        model=register
        fields='__all__'
class forgotform(forms.ModelForm):
    class Meta:
        model=forgot
        fields=['Email']
class passform(forms.ModelForm):
    class Meta:
        model= password
        fields='__all__'
class Script(forms.ModelForm):
    class Meta:
        model=Script
        fields='__all__'