Projemizin genel amacı Savunma Sanayisinde, parça üretim ve montaj departmanında çalışan kişilerin, ürettikleri parçaların stoklarını tutmaya yarayan ayrıyeten
montaj işlemleri bittikten sonra envantere üretilen uçağı kaydetmektir.

-Programlama Dili : Python
-Framework : Django Rest Framework (DRF)
-Database : PostgreSQL
-Database Arayüz : pgAdmin4 (Opsiyonel)
-IDE : VS code ve PyCharm

Proje içerisine girdiğiniz zaman Aircraft.postman_collection adında .JSON uzantılı dosyayla hazır bir şekilde manuel testini yapabilirsiniz.

PROJE AKIŞI:
Senaryo kısmına geçmeden önce attığım projeyi zip olarak indirdikten sonra eğer macOS işletim sistemine sahipseniz projenin application dizinine gittikten sonra
'bash' kısmına python3 manage.py makemigrations yazarsanız migration klasörü içerisine 0001_initial.py isimli bir dosya gelecektir. Bu dosyanın amacı SQL e 
bağlanıp gerekli CREATE işlemlerini yapmaktır. Sonrasında python3 manage.py migrate diyoruz ve serverimizi ayağa kaldırmak için python3 manage.py runserver
diyip projemizi başlatıyoruz. SISTEM AYAĞA KALKAR KALKMAZ TEAM PART AIRCRAFT NESNELERİ DATABASEDE OTOMATİK OLUŞACAKTIR .Şimdi gelelim senaryomuza.

Bir çalışan (Personnel) sisteme kayıt olmadığı sürece herhangi bir işlem yapamayacaktır. Kayıt için register sayfasına yönlendirilip gerekli parametreleri girdikten sonra sisteme takımı belli olacak şekilde giriş yapabilmektedir. Sistem JWT ile güvenliği sağlamaktadır.

Her personel ait olduğu takımla alakalı işlemleri yapabilmektedir. KANAT TAKIMI na ait bir personnel KUYRUK,GÖVDE gibi takımların parça ekleme silme ve liste-lemesine karışamaz. İzni de yoktur zaten sistem uyarı verecektir.

Personeller ürettikleri her parçayı her üretim sonunda tek tek de ekleyebilmektedir , toplu bir şekilde de kayda geçebilmektedir.

Parçalar sadece uçağa aittir. Bu ne demek oluyor mesela KIZILELMA'ya ait bir kanat tipi TB2 ye asla takılamaz. Bu istek yapıldığı an uyarı mesajı gidecektir.

Nontaj takımının ise görevi tüm parçaları birleştirip bir uçak ortaya çıkarmaktır. Ve yapılan uçakları sadece Montaj ekibi listeleyebilmektedir. Öteki tüm gruplar sadece kendi ürettikleri parçaların listesini görebilmektedir. Ve ayrıca uçağın montajlama işleminde gerekli parçalarda eksiklik söz konusu olduğunda sistem uyarı vermektedir.

Montaj işlemi için kullanılacak malzemeler seçildiği anda AssemblyItem database tablosunda tüm detaylar mevcut olacaktır.

Settings.py ayarları anlamları

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=50),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': 'django-insecure-#vtk++^3&vt6t)+i5e&dw1yrr%fyy*u1_=a!t&*_hni@v@9u2k',
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=50),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

Güvenlik sağlamak amaçlı oluşacak JWT tokenin özelliklerini barındıran ve yapılandırılan kısımdır. Zaten settings.py tamamen yapılandırma amaçlı kullanılmaktadır.

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'EXCEPTION_HANDLER': 'production.exceptions.custom_exception.custom_exception_handler',
}

Rest framework içersindeki default Authentication sınıfını kullanarak JWT üretebilir demek istyor.


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'aircraft_factory_db',    # PostgreSQL'de oluşturduğunuz veritabanı adı
        'USER': '?',                      # PostgreSQL kullanıcı adı
        'PASSWORD': '123321',             # PostgreSQL şifresi
        'HOST': 'localhost',              # PostgreSQL sunucu adresi (genelde localhost)
        'PORT': '5432',                   # PostgreSQL port numarası
    }
}

DB ayarlaması yapığımız kısım.

