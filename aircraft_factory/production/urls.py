from django.urls import path
from production.api_views import personnel_view, team_view, part_view, aircraft_view, inventory_view, assembly_view
from production.html_views import my_html_views  # HTML view'leriniz

urlpatterns = [
    # FOR API:
    path('api/user/login/', personnel_view.login_view, name='login_api'),
    path('api/user/register/', personnel_view.register_view, name='register_api'),
    path('api/aircraft/list/', aircraft_view.list_of_aircraft_view, name='list_of_aircraft_api'),
    path('api/aircraft/create/', aircraft_view.create_aircraft_view, name='create_aircraft_api'),
    path('api/part/create/', part_view.create_part_view, name='create_part_api'),
    path('api/part/list/', inventory_view.list_quantity_and_part_of_inventory, name='list_of_part_api'),
    path('api/team/create/', team_view.create_view, name='create_team_api'),
    path('api/assembly/create/',assembly_view.start_assembly_process, name='start_assembly_api'),

    # FOR HTML:
    path('' , my_html_views.login_html_view, name='home_html'),
    path('user/login/', my_html_views.login_html_view, name='login_html'),
    path('user/register/', my_html_views.register_html_view, name='register_html'),
    path('dashboard/', my_html_views.dashboard_view, name='dashboard'),
    path('aircraft/list/', my_html_views.list_of_aircraft_html_view, name='list_of_aircraft_html'),
    path('aircraft/create/', my_html_views.create_aircraft_html_view, name='create_aircraft_html'),
    path('aircraft/assembly/', my_html_views.assembly_html_view, name='assembly_html'),
    path('part/create/', my_html_views.create_part_html_view, name='create_part_html'),
    path('part/<int:part_id>/increase/', my_html_views.increase_stock_of_part_html_view, name='increase_stock_of_part_html'),
    path('part/<int:part_id>/decrease/', my_html_views.decrease_stock_of_part_html_view, name='decrease_stock_of_part_html'),
    path('team/create/', my_html_views.create_team_html_view, name='create_team_html'),
    path('team/get/', my_html_views.get_team_html_view, name='get_team_html'),
]

