from django.urls import path
from payApp import views

urlpatterns = [
    path('',views.starting_page),
    path('handle-request',views.handle_callback)
]
