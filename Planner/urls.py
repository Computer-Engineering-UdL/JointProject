from django.urls import path

from Planner import views as v

urlpatterns = [
    path('', v.planner_home, name='planner_home'),
    path('add-room/', v.add_room, name='add_room'),
    path('room-assignment/', v.room_assignment, name='room_assignment'),
    path('room-detail/<int:room_id>/', v.cleaner_room_detail, name='planner_room_detail'),
    path('assign-cleaner/<int:room_id>/', v.assign_cleaner_to_room, name='assign_cleaner_to_room'),
    path('unassign-cleaner/<int:room_id>/', v.unassign_cleaner_from_room, name='unassign_cleaner_from_room'),
    path('new-worker/', v.new_worker, name='new_worker')
]
