# @Author: Tushar Agarwal(tusharcoder) <tushar>
# @Date:   2017-05-08T15:56:12+05:30
# @Email:  tamyworld@gmail.com
# @Filename: models.py
# @Last modified by:   tushar
# @Last modified time: 2017-08-09T17:50:01+05:30





from django.conf.urls import include, url
from django.views.decorators.csrf import csrf_exempt

from .views import renderView, getModelFields, uploadExcelSheet


urlpatterns = [
 url(r'^$', renderView, name='index'),

 #ajax views
 url(r'^getModelFields/$',getModelFields,name="get_model_fields"),
 url(r'^uploadData/$',uploadExcelSheet,name="upload_data"),
]
