from production.models import Aircraft, AssemblyRegistration
from production.exceptions.custom_exception import BusinessException


class AircraftService:

    # Constructor Method
    def __init__(self,aircraft_repository=Aircraft,
                 assembly_registration = AssemblyRegistration,
                 part_service = None):
        self.aircraft_repository = aircraft_repository
        self.assembly_registration = assembly_registration
        self.part_service = part_service

    # Method for find aircraft by aircraft id
    def find_aircraft_by_id(self,aircraft_id):
        try:
            aircraft = self.aircraft_repository.objects.get(id=aircraft_id)
        except self.aircraft_repository.DoesNotExist:
            raise BusinessException("Aircraft could not found by id !")
        return aircraft

    def assemble_aircraft(self,assembler,aircraft_id,parts):
        """
            Uçağın montaj işlemini gerçekleştirir:
              - Montajcı yetkilendirme kontrolü
              - Uçağın doğrulanması
              - Montaj kaydının oluşturulması
              - Her parçanın kontrolü, stoğunun düşürülmesi ve kayda eklenmesi
            """
        self._validate_assembler(assembler)
        aircraft = self._get_aircraft_by_id(aircraft_id)
        self._initialize_part_service()

        registration = self._create_assembly_registration(aircraft,assembler)
        self._process_parts_for_registration(registration,aircraft,parts)

        self.aircraft_repository.save(aircraft)
        registration.save()
        return registration

    def _validate_assembler(self,assembler):
        if assembler.team.name.upper() != "MONTAJ TAKIMI":
            raise BusinessException("Aircraft could not assemble by this assembler !")

    def _get_aircraft_by_id(self,aircraft_id):
        try:
            return self.aircraft_repository.objects.get(id=aircraft_id)
        except self.aircraft_repository.DoesNotExist:
            raise BusinessException("Aircraft could not found by id !")

    def _initialize_part_service(self):
        if not self.part_service:
            from production.services.part_service import PartService
            self.part_service = PartService()

    def _create_assembly_registration(self,aircraft,assembler):
        return self.assembly_registration.objects.create(
            aircraft=aircraft,
            assembler=assembler
        )

    def _process_parts_for_registration(self,registration,aircraft,parts):
        """
            Her bir parça için:
              - Parça bilgisini getirir
              - Uçağa ait olup olmadığını kontrol eder
              - Stoğu düşürür
              - Montaj kaydına ekler
        """
        for part_data in parts:
            part_id = part_data.get("part_id")
            quantity_used = part_data.get("quantity",1)

            part = self._get_part(part_id)
            self._validate_part_belongs_to_aircraft(part,aircraft)
            self.part_service.decrease_stock_of_part(part_id,quantity_used)
            registration.parts_used.add(part)

    def _get_part(self,part_id):
        """Belirtilen ID'ye sahip parçayı getirir."""
        try:
            return self.part_service.find_part_by_id(part_id)
        except self.part_service.part_model.DoesNotExist:
            raise BusinessException("Part could not found by id : " + str(part_id))

    def _validate_part_belongs_to_aircraft(self, part, aircraft):
        """Parçanın, belirtilen uçağa ait olup olmadığını kontrol eder."""
        if part.aircraft != aircraft:
            raise BusinessException(f"Part with id {part.id} does not belong to the aircraft!")

    def create_aircraft(self, user, data):
        # 1. Montaj takımına ait olmayan kullanıcılar için hata fırlatıyoruz.
        if user.team.name.upper() != "MONTAJ TAKIMI":
            raise BusinessException("Sadece Montaj Takımı uçak oluşturabilir!")

        # 2. Gelen veriden uçak tipini alıyoruz. (Zorunlu alan)
        aircraft_type = data.get("type")
        if not aircraft_type:
            raise BusinessException("Uçak tipi gereklidir!")

        # 3. Eklenecek miktarı belirliyoruz, belirtilmezse varsayılan olarak 1 kabul ediyoruz.
        quantity_to_add = data.get("quantity", 1)

        # 4. Aynı tipe sahip uçak zaten mevcut mu diye kontrol ediyoruz.
        try:
            # Mevcut uçak kaydını repository üzerinden bulmaya çalışıyoruz.
            aircraft = Aircraft.objects.get(type=aircraft_type)
            # 5. Eğer uçak varsa, yeni kayıt oluşturmak yerine miktarını artırıyoruz.
            aircraft.quantity += quantity_to_add
            aircraft.save()  # Artırılan miktarı veri tabanına kaydediyoruz.
        except Aircraft.DoesNotExist:
            # 6. Eğer uçak bulunamazsa, yeni bir uçak kaydı oluşturuyoruz.
            aircraft = Aircraft.objects.create(
                type=aircraft_type,
                quantity=quantity_to_add  # Yeni kayıtta miktar, eklenmek istenen miktar olarak ayarlanır.
            )
        # 7. İşlem tamamlandığında (varsa miktar artırılmış ya da yeni kayıt oluşturulmuş) uçağı geri döndürüyoruz.
        return aircraft

    def get_all_aircraft(self):
        try:
            aircraft_list = self.aircraft_repository.objects.all().order_by("id")
            return aircraft_list
        except Exception as e:
            raise BusinessException("Something went wrong : " + str(e))