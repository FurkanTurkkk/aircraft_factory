from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# my_html_views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from production.exceptions.custom_exception import BusinessException
from production.services.personnel_service import PersonnelService


def login_html_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Başarılı login sonrası dashboard'a yönlendiriyoruz
        else:
            messages.error(request, "Kullanıcı adı veya şifre hatalı")
            return render(request, 'login.html')


def register_html_view(request):
    if request.method == 'GET':
        # Kayıt formunu gösteren template (örneğin register.html)
        return render(request, 'register.html')

    elif request.method == 'POST':
        # Form verilerini alıyoruz
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        team_id = request.POST.get('team_id')

        service = PersonnelService()
        try:
            # Kullanıcı kaydını yapıyoruz
            user = service.register(username, password, email, team_id)
            # Kayıt başarılı ise kullanıcıya mesaj göster ve login sayfasına yönlendir
            messages.success(request, "Kayıt başarılı, lütfen giriş yapınız.")
            return redirect('login_page_html')  # urls.py'de 'login_page' ismine sahip URL
        except BusinessException as e:
            # İş mantığına özel hata durumunda formu yeniden göster ve hata mesajı gönder
            messages.error(request, e.detail)
            return render(request, 'register.html', {
                'username': username,
                'email': email,
                'team_id': team_id
            })
        except Exception as e:
            # Genel hata durumunda formu yeniden göster
            messages.error(request, str(e))
            return render(request, 'register.html', {
                'username': username,
                'email': email,
                'team_id': team_id
            })

@login_required
def dashboard_view(request):
    # Örneğin, kullanıcı modelinizde 'team' ilişkisi varsa:
    team_name = request.user.team.name if hasattr(request.user, 'team') else "Takımınız Yok"
    context = {
        'team_name': team_name,
    }
    return render(request, 'dashboard.html', context)
