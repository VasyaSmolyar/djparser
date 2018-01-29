from django.urls import path
from . import views

app_name = 'djparser'

urlpatterns = [
    path('',views.index,name='index'),
    path('delete/<int:sid>/',views.delete,name='delete'),
    path('result/<int:sid>/',views.result,name='result'),
    path('parse/<int:sid>/',views.parse,name='parse'),
    path('setting/',views.setting,name='setting')
]
