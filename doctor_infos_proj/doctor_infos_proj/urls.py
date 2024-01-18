from django.contrib import admin
from django.urls import path
from doctor_infos_app.views import DoctorViewSet
from django.http import HttpResponse
from ninja import File, NinjaAPI

import logging

admin.autodiscover()

api_v1 = NinjaAPI(version="1.0.0")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('doctor', DoctorViewSet.as_view({'get': 'list','post': 'create'})),
    path('doctor/<id>', DoctorViewSet.as_view({'get': 'retrieve'}), name="get-doctor-id"),
]

logging.info('setting up urls...')