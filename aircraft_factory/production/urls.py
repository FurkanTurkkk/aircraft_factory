from django.urls import path
from production.controller import personnel_view, team_view, part_view, aircraft_view

urlpatterns = [
    path('user/register/', personnel_view.register_view, name='register'),
    path('user/login/', personnel_view.login_view, name='login'),
    path('team/create/',team_view.create_view, name='create_team'),
    path('team/find/<int:team_id>/',team_view.get_view, name='find_team'),
    path('part/add/',part_view.create_part_view, name='add_part'),
    path('part/delete/<int:part_id>/', part_view.delete_part_view, name='delete_part'),
    path('aircraft/list/',aircraft_view.list_of_aircraft_view, name='list_aircraft'),
    path('aircraft/assembly/',aircraft_view.assembly_view, name='assembly_aircraft'),
    path('aircraft/create/',aircraft_view.create_aircraft_view, name='create_aircraft'),
]

