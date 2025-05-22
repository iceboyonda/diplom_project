import os
import random
from django.core.management.base import BaseCommand
from tyres.models import TyreModel, TyreVariant, RimModel, RimVariant
from django.conf import settings

def smart_title(s):
    # Преобразует имя файла в красивое название
    s = os.path.splitext(s)[0]
    s = s.replace('_', ' ').replace('-', ' ')
    return s.title()

class Command(BaseCommand):
    help = 'Автоматически создает шины и диски с вариациями на основе файлов из media/tyres и media/rims/variants.'

    def handle(self, *args, **kwargs):
        # Проверяем, есть ли уже товары
        if TyreModel.objects.exists() or RimModel.objects.exists():
            self.stdout.write(self.style.SUCCESS('Товары уже существуют, автозаполнение не требуется.'))
            return

        self.stdout.write('Добавляю реальные шины и диски с вариациями...')

        # --- Реальные шины ---
        tyres_data = [
            {
                'name': 'X-Ice North 4',
                'brand': 'Michelin',
                'image': 'michelinx-icenorth4.jpg',
                'description': 'Зимняя шипованная шина для суровых условий.',
                'variants': [
                    {'width': 205, 'profile': 55, 'radius': 16, 'season': 'winter', 'studded': True, 'speed_index': 'T', 'price': 12000, 'stock': 10},
                    {'width': 215, 'profile': 60, 'radius': 17, 'season': 'winter', 'studded': True, 'speed_index': 'T', 'price': 13500, 'stock': 8},
                ]
            },
            {
                'name': 'Pilot Sport 4',
                'brand': 'Michelin',
                'image': 'MichelinPilotSport4.jpg',
                'description': 'Летняя спортивная шина.',
                'variants': [
                    {'width': 225, 'profile': 45, 'radius': 17, 'season': 'summer', 'studded': False, 'speed_index': 'Y', 'price': 14000, 'stock': 12},
                    {'width': 235, 'profile': 40, 'radius': 18, 'season': 'summer', 'studded': False, 'speed_index': 'Y', 'price': 15500, 'stock': 7},
                ]
            },
            {
                'name': 'Hakkapeliitta 10',
                'brand': 'Nokian',
                'image': 'nokianhakkapelita10.jpg',
                'description': 'Зимняя шипованная шина.',
                'variants': [
                    {'width': 205, 'profile': 55, 'radius': 16, 'season': 'winter', 'studded': True, 'speed_index': 'T', 'price': 12500, 'stock': 9},
                    {'width': 215, 'profile': 50, 'radius': 17, 'season': 'winter', 'studded': True, 'speed_index': 'T', 'price': 13800, 'stock': 6},
                ]
            },
            {
                'name': 'Turanza T005',
                'brand': 'Bridgestone',
                'image': 'BridgestoneTuranzaT005.jpg',
                'description': 'Летняя шина для комфортной езды.',
                'variants': [
                    {'width': 205, 'profile': 55, 'radius': 16, 'season': 'summer', 'studded': False, 'speed_index': 'V', 'price': 11000, 'stock': 11},
                    {'width': 225, 'profile': 45, 'radius': 17, 'season': 'summer', 'studded': False, 'speed_index': 'W', 'price': 12800, 'stock': 8},
                ]
            },
        ]
        tyres_dir = os.path.join(settings.MEDIA_ROOT, 'tyres')
        for tyre_data in tyres_data:
            image_path = f"tyres/{tyre_data['image']}" if os.path.exists(os.path.join(tyres_dir, tyre_data['image'])) else ''
                tyre = TyreModel.objects.create(
                name=tyre_data['name'],
                brand=tyre_data['brand'],
                description=tyre_data['description'],
                image=image_path
            )
            for v in tyre_data['variants']:
                TyreVariant.objects.create(model=tyre, **v)
            self.stdout.write(f"Шина {tyre_data['brand']} {tyre_data['name']} создана.")

        # --- Реальные диски ---
        rims_data = [
            {
                'name': 'CH-R',
                'brand': 'BBS',
                'description': 'Классический премиум-диск.',
                'image': 'bbschr.jpg',
                'variants': [
                    {'diameter': 18, 'width': 8.0, 'bolt_pattern': '5x112', 'offset': 'ET45', 'dia': '66.6', 'color': 'Серебристый', 'material': 'Алюминий', 'price': 45000, 'stock': 5},
                    {'diameter': 19, 'width': 8.5, 'bolt_pattern': '5x112', 'offset': 'ET40', 'dia': '66.6', 'color': 'Черный', 'material': 'Алюминий', 'price': 52000, 'stock': 3},
                ]
            },
            {
                'name': 'Ultraleggera',
                'brand': 'OZ Racing',
                'description': 'Лёгкий спортивный диск.',
                'image': 'ozracingultraleggera.jpg',
                'variants': [
                    {'diameter': 17, 'width': 7.5, 'bolt_pattern': '5x100', 'offset': 'ET35', 'dia': '57.1', 'color': 'Черный', 'material': 'Алюминий', 'price': 32000, 'stock': 4},
                    {'diameter': 18, 'width': 8.0, 'bolt_pattern': '5x112', 'offset': 'ET45', 'dia': '66.6', 'color': 'Антрацит', 'material': 'Алюминий', 'price': 37000, 'stock': 2},
                ]
            },
            {
                'name': 'RPF1',
                'brand': 'Enkei',
                'description': 'Легендарный японский кованный диск.',
                'image': 'enkeirpf1.jpg',
                'variants': [
                    {'diameter': 17, 'width': 7.5, 'bolt_pattern': '5x114.3', 'offset': 'ET48', 'dia': '73.1', 'color': 'Серебристый', 'material': 'Кованый', 'price': 38000, 'stock': 6},
                    {'diameter': 18, 'width': 8.5, 'bolt_pattern': '5x114.3', 'offset': 'ET35', 'dia': '73.1', 'color': 'Черный', 'material': 'Кованый', 'price': 42000, 'stock': 3},
                ]
            },
            {
                'name': 'SR-KAI',
                'brand': 'WORK',
                'description': 'Японский спортивный диск WORK SR-KAI.',
                'image': 'worksrkai.jpg',
                'variants': [
                    {'diameter': 17, 'width': 7.5, 'bolt_pattern': '5x114.3', 'offset': 'ET42', 'dia': '73.1', 'color': 'Серебристый', 'material': 'Алюминий', 'price': 34000, 'stock': 4},
                    {'diameter': 18, 'width': 8.5, 'bolt_pattern': '5x114.3', 'offset': 'ET35', 'dia': '73.1', 'color': 'Графит', 'material': 'Алюминий', 'price': 39000, 'stock': 2},
                ]
            },
        ]
        rims_dir = os.path.join(settings.MEDIA_ROOT, 'rims', 'variants')
        for rim_data in rims_data:
            image_path = f"rims/variants/{rim_data['image']}" if os.path.exists(os.path.join(rims_dir, rim_data['image'])) else ''
                rim = RimModel.objects.create(
                name=rim_data['name'],
                brand=rim_data['brand'],
                description=rim_data['description'],
                image=image_path
            )
            for v in rim_data['variants']:
                RimVariant.objects.create(model=rim, **v)
            self.stdout.write(f"Диск {rim_data['brand']} {rim_data['name']} создан.")

        self.stdout.write(self.style.SUCCESS('Автоматическое создание реальных шин и дисков завершено!')) 