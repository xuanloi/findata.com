"""DataEntry URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path
from Backend import views, calculate, technical

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^data/(?P<name>.+)/$', views.data_list),
    url(r'^data-detail/(?P<name>.+)/(?P<pk>[0-9]+)/$', views.data_detail),
    url(r'^send-email/$', views.send_email_api),
    url(r'^upload-file/$', views.upload_file),
    url(r'^upload/$', views.upload),
    url(r'^getfile/(?P<filename>.+)/$', views.getfile),
    url(r'^export-data/$', views.export_data_api),
    url(r'^export-table/(?P<table>.+)/$', views.export_table_api),
    url(r'^download-file/(?P<name>.+)/$', views.download_file),
    url(r'^salary-summary/(?P<filter>.+)/$', views.salary_summary),
    url(r'^salary-calculation/(?P<filter>.+)/$', views.salary_calculation),
    url(r'^change-data-model/$', views.change_data_model),
    url(r'^migrate-data-model/$', views.migrate_data_model),
    url(r'^task-summary/(?P<filter>.+)/$', views.task_summary),
    url(r'^validate-import/(?P<name>.+)/$', views.validate_import),
    url(r'^import-data/(?P<name>.+)/$', views.import_data),
    url(r'^delete-report-via-task/$', views.delete_report),
    url(r'^check-model-relation/(?P<name>.+)/$', views.check_model_relation),
    url(r'^download/$', views.download),
    url(r'^get-hash/(?P<name>.+)/$', views.get_hash),
    url(r'^login/$', views.login),
    url(r'^get-datafile/(?P<name>.+)/$', views.get_datafile),
    url(r'^get-fin-item/$', calculate.get_fin_item),
    url(r'^get-ta-item/$', calculate.get_ta_item),
    url(r'^screener-performance/$', calculate.screener_performance),
    url(r'^valuation/$', calculate.valuation),
    url(r'^get-fin-item-v1/$', calculate.get_fin_item_v1),
    url(r'^insert-price-live/$', views.insert_price_live),
    url(r'^macd/$', technical.macd)
]