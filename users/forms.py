from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class Captcha(forms.Form):

        captcha =ReCaptchaField(widget=ReCaptchaV2Checkbox(attrs={'data-theme': 'dark','data-size': 'normal',},
                                                        api_params={'hl': 'fa'}),required=True)