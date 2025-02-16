# production/views/my_html_views.py

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.shortcuts import render, redirect

from production.models import Part, Aircraft
from production.serializer import AssemblyRequestSerializer
from production.services.aircraft_service import AircraftService
from production.services.assembly_service import AssemblyService
from production.services.inventory_service import InventoryService
from production.services.part_service import PartService
from production.services.personnel_service import PersonnelService
from production.services.team_service import TeamService


@login_required
def dashboard_view(request):
    # Kullanıcı modelinizde team ilişkisi varsa onu gönderelim.
    team_obj = getattr(request.user, 'team', None)
    team_name = team_obj.name if team_obj and hasattr(team_obj, 'name') else "Takım Yok"
    context = {
        'team_name': team_name,
    }
    return render(request, "dashboard.html", context)

@login_required
def list_of_inventory(request):
    try:
        service = InventoryService()

        user = request.user
        team = user.team

        inventory_list = service.list_inventory(team)
        context = {"inventory_list": inventory_list}
        return render(request, "list_inventory.html", context)

    except Exception as e:
        messages.error(request, f"Bir hata oluştu: {str(e)}")
        return redirect('dashboard')

# Increase Quantity
def increase_quantity(request):
    if request.method == "POST":
        service = InventoryService()
        part_id = request.POST.get("part_id")
        service.increase_quantity(part_id, 1)
        return redirect('list_of_inventory_html')

# Decrease Quantity
def decrease_quantity(request):
    if request.method == "POST":
        service = InventoryService()
        part_id = request.POST.get("part_id")
        service.decrease_quantity(part_id, 1)
        return redirect('list_of_inventory_html')


@login_required
def start_assembly_process_html(request):
    selected_aircraft_id = request.GET.get('aircraft')  # Seçilen uçak ID'si
    aircrafts = Aircraft.objects.all()  # Tüm uçakları al

    # Parçaları sadece bir uçak seçildiyse al
    parts = []
    if selected_aircraft_id:
        selected_aircraft = Aircraft.objects.get(id=selected_aircraft_id)
        parts = Part.objects.filter(aircraft=selected_aircraft)

    return render(request, 'create_assembly.html', {
        'aircrafts': aircrafts,
        'selected_aircraft_id': selected_aircraft_id,
        'parts': parts,
    })

# Decrease Quantity
def start_assembly(request):
    if request.method == "POST":
        serializer = AssemblyRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        personnel = request.user

        with transaction.atomic():
            service = AssemblyService()
            assembly = service.start_assembly(
                aircraft_id=serializer.validated_data['aircraft_id'],
                items=serializer.validated_data['items'],
                user_id=personnel,
                team=request.user.team
            )

        assembly_service = AssemblyService()
        assembly_service.start_assembly(aircraft_id=serializer.validated_data['aircraft_id'], user_id=personnel, team=request.user.team)

        return redirect('start_assembly_html')


# --- Aircraft İşlemleri ---

@login_required
def list_of_aircraft_html_view(request):
    try:
        # Sadece Montaj Takımı personeli uçakları görebilir
        if request.user.team.name.upper() != "MONTAJ TAKIMI":
            messages.error(request, "Bu işlemi yapmaya yetkiniz yok.")
            return redirect('dashboard')

        service = AircraftService()
        aircraft_list = service.get_all_aircraft()
        context = {"aircraft_list": aircraft_list}
        return render(request, "list_of_aircraft.html", context)

    except Exception as e:
        # İstisnayı yakala ve kullanıcıya bir hata mesajı göster
        messages.error(request, f"Bir hata oluştu: {str(e)}")
        return redirect('dashboard')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_aircraft_html_view(request):
    if request.method == 'GET':
        return render(request, "create_aircraft.html")
    elif request.method == 'POST':
        # Formdan gelen verileri alalım
        # İsterseniz bir Django Form sınıfı da kullanabilirsiniz.
        data = {
            'field1': request.POST.get('field1'),
            'field2': request.POST.get('field2'),
            # ... gerekli alanlar
        }
        aircraft_service = AircraftService()
        try:
            aircraft = aircraft_service.create_aircraft(request.user, data)
            messages.success(request, "Uçak başarıyla oluşturuldu.")
            return redirect("list_of_aircraft_html")
        except Exception as e:
            messages.error(request, str(e))
            return render(request, "create_aircraft.html", {"data": data})


@login_required
def assembly_html_view(request):
    if request.user.team.name.upper() != "MONTAJ TAKIMI":
        messages.error(request, "Bu işlemi yapmaya yetkiniz yok.")
        return redirect('dashboard')

    if request.method == 'GET':
        return render(request, "assembly.html")
    elif request.method == 'POST':
        airplane_id = request.POST.get('airplane_id')
        used_parts = request.POST.get('parts_used')  # Örneğin, virgülle ayrılmış parça ID'leri
        service = AircraftService()
        try:
            registration = service.assemble_aircraft(request.user, airplane_id, used_parts)
            messages.success(request, "Uçak montajı başarıyla tamamlandı.")
            return redirect("dashboard")
        except Exception as e:
            messages.error(request, str(e))
            return render(request, "assembly.html")


# --- Part İşlemleri ---

@login_required
def create_part_html_view(request):
    if request.method == 'GET':
        return render(request, "create_part.html")
    elif request.method == 'POST':
        part_type = request.POST.get('part_type')
        stock = request.POST.get('stock')
        aircraft_id = request.POST.get('aircraft_id')
        airplane_type_of_part = request.POST.get('airplane_type_of_part')
        service = PartService()
        try:
            part, message_text = service.create_part(
                added_by=request.user,
                part_type=part_type,
                stock=stock,
                aircraft_id=aircraft_id,
                airplane_type_of_part=airplane_type_of_part,
            )
            messages.success(request, message_text)
            return redirect("dashboard")
        except Exception as e:
            messages.error(request, str(e))
            return render(request, "create_part.html")


@login_required
def increase_stock_of_part_html_view(request, part_id):
    if request.method == 'GET':
        return render(request, "increase_stock.html", {"part_id": part_id})
    elif request.method == 'POST':
        quantity = int(request.POST.get('quantity', 0))
        service = PartService()
        try:
            service.increase_stock_of_part(part_id, quantity)
            messages.success(request, "Stok artırma işlemi başarılı.")
            return redirect("dashboard")
        except Exception as e:
            messages.error(request, str(e))
            return render(request, "increase_stock.html", {"part_id": part_id})


@login_required
def decrease_stock_of_part_html_view(request, part_id):
    if request.method == 'GET':
        return render(request, "decrease_stock.html", {"part_id": part_id})
    elif request.method == 'POST':
        quantity = int(request.POST.get('quantity', 0))
        service = PartService()
        try:
            service.decrease_stock_of_part(part_id, quantity)
            messages.success(request, "Stok azaltma işlemi başarılı.")
            return redirect("dashboard")
        except Exception as e:
            messages.error(request, str(e))
            return render(request, "decrease_stock.html", {"part_id": part_id})


# --- Kullanıcı İşlemleri ---

def register_html_view(request):
    if request.method == 'GET':
        return render(request, "register.html")
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        team_id = request.POST.get('team_id')
        service = PersonnelService()
        try:
            service.register(username, password, email, team_id)
            messages.success(request, "Kayıt başarılı, lütfen giriş yapınız.")
            return redirect("login_html")
        except Exception as e:
            messages.error(request, str(e))
            return render(request, "register.html")


def login_html_view(request):
    if request.method == 'GET':
        return render(request, "login.html")
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        service = PersonnelService()
        try:
            user, token = service.login(username, password, request)
            # Django’nun session tabanlı auth sistemiyle giriş yapalım:
            from django.contrib.auth import login
            login(request, user)
            messages.success(request, "Giriş başarılı.")
            return redirect("list_of_inventory_html")
        except Exception as e:
            messages.error(request, str(e))
            return render(request, "login.html")


# --- Takım İşlemleri ---

@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_team_html_view(request):
    if request.method == 'GET':
        return render(request, "create_team.html")
    elif request.method == 'POST':
        name = request.POST.get('name')
        team_service = TeamService()
        try:
            team_service.create_team(name)
            messages.success(request, "Takım başarıyla oluşturuldu.")
            return redirect("dashboard")
        except Exception as e:
            messages.error(request, str(e))
            return render(request, "create_team.html")


@login_required
def get_team_html_view(request):
    team_id = request.GET.get('id')
    if not team_id:
        messages.error(request, "Takım ID gerekli.")
        return redirect("dashboard")
    team_service = TeamService()
    try:
        team = team_service.find_team_by_id(team_id)
        context = {"team": team}
        return render(request, "team_detail.html", context)
    except Exception as e:
        messages.error(request, str(e))
        return redirect("dashboard")
