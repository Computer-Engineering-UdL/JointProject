from django.urls import path
from Planner import views as v

urlpatterns = [
    path('', v.planner_home, name='planner_home'),
    path('add-room/', v.add_room, name='add_room'),
    path('room-assignment/', v.room_assignment, name='room_assignment'),
    path('new-worker/', v.new_worker, name='new_worker')
]
