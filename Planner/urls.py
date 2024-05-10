from django.urls import path
from Planner import views as v

urlpatterns = [
    path('', v.planner_home, name='planner_home'),
    path('add-room/', v.add_room, name='add_room'),
]
