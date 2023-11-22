from django.shortcuts import render
from django.conf import settings
from .models import Slider
from django.views import View
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin


def media_admin(request):
    return {'media_url': settings.MEDIA_URL}


def index(request):
    return render(request, 'main_app/index.html')


class SliderView(View):
    def get(self, request):
        sliders = Slider.objects.filter(Q(is_active=True))
        return render(request, 'main_app/sliders.html', {'sliders': sliders})


# __________________________________________________ contact us
class ContactUs(View):
    def get(self, request):
        return render(request, 'main_app/contact_us.html')

# ___________________________________________________

# def handler404(request, exception=None):
#     return render(request, 'main/404.html')
