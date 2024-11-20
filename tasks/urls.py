from tasks import views
from django.urls import path

app_name = 'tasks'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    # path('pending/', views.progress_bar, name='pending')
]