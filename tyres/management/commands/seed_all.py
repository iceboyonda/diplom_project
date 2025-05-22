import random
from django.core.management.base import BaseCommand
from tyres.models import TyreModel, TyreVariant, RimModel, RimVariant

# Примеры шин (по фикстурам)
TYRES = [
    {"name": "X-Ice North 4", "brand": "Michelin", "description": "Зимняя шина с отличным сцеплением на льду.", "season": "winter", "studded": True},
    {"name": "IceContact 3", "brand": "Continental", "description": "Современная зимняя шина для суровых условий.", "season": "winter", "studded": True},
    {"name": "Blizzak VRX3", "brand": "Bridgestone", "description": "Японская зимняя шина для города и трассы.", "season": "winter", "studded": False},
    {"name": "Hakkapeliitta 10", "brand": "Nokian", "description": "Финская шина для суровой зимы.", "season": "winter", "studded": True},
    {"name": "UltraGrip Ice 2", "brand": "Goodyear", "description": "Зимняя нешипованная шина для легковых авто.", "season": "winter", "studded": False},
    {"name": "Pilot Sport 4", "brand": "Michelin", "description": "Летняя шина для динамичной езды.", "season": "summer", "studded": False},
    {"name": "Turanza T005", "brand": "Bridgestone", "description": "Летняя шина для комфорта и безопасности.", "season": "summer", "studded": False},
    {"name": "EcoContact 6", "brand": "Continental", "description": "Экономичная летняя шина.", "season": "summer", "studded": False},
    {"name": "Energy Saver+", "brand": "Michelin", "description": "Летняя шина для экономии топлива.", "season": "summer", "studded": False},
    {"name": "EfficientGrip Performance", "brand": "Goodyear", "description": "Летняя шина для мокрой дороги.", "season": "summer", "studded": False},
    {"name": "Nordman SX2", "brand": "Nokian", "description": "Бюджетная летняя шина.", "season": "summer", "studded": False},
    {"name": "Vector 4Seasons Gen-3", "brand": "Goodyear", "description": "Всесезонная шина для любых условий.", "season": "all_season", "studded": False},
    {"name": "CrossClimate+", "brand": "Michelin", "description": "Всесезонная шина для Европы и России.", "season": "all_season", "studded": False},
    {"name": "AllSeasonContact", "brand": "Continental", "description": "Всесезонная шина для мягких зим.", "season": "all_season", "studded": False},
]

TYRE_VARIANTS = [
    # width, profile, radius, speed_index, price, stock
    (205, 55, 16, "T", 7500, 10),
    (215, 60, 17, "H", 8200, 5),
    (195, 65, 15, "T", 6900, 8),
    (225, 45, 18, "V", 9900, 3),
    (205, 60, 16, "H", 8100, 7),
    (215, 55, 17, "T", 8700, 4),
    (225, 50, 17, "H", 9500, 6),
    (235, 45, 18, "V", 10200, 2),
    (195, 65, 15, "T", 6700, 9),
    (205, 60, 16, "H", 7300, 5),
    (225, 45, 17, "W", 9800, 7),
    (235, 40, 18, "Y", 11200, 4),
    (205, 55, 16, "V", 7200, 8),
    (215, 60, 17, "W", 8300, 5),
    (195, 65, 15, "T", 6100, 10),
    (205, 60, 16, "H", 6700, 6),
]

RIMS = [
    {"brand": "BBS", "name": "LM", "description": "Легендарные составные диски", "variants": [
        {"diameter": 18.0, "width": 8.0, "bolt_pattern": "5x120", "offset": "ET35", "dia": "72.5", "color": "Silver", "material": "Forged", "price": 50000, "stock": 10},
        {"diameter": 18.0, "width": 9.0, "bolt_pattern": "5x120", "offset": "ET42", "dia": "72.5", "color": "Silver", "material": "Forged", "price": 55000, "stock": 8},
    ]},
    {"brand": "OZ Racing", "name": "Ultraleggera", "description": "Легкие спортивные диски", "variants": [
        {"diameter": 17.0, "width": 7.5, "bolt_pattern": "5x100", "offset": "ET35", "dia": "57.1", "color": "Black", "material": "Cast", "price": 15000, "stock": 15},
        {"diameter": 18.0, "width": 8.0, "bolt_pattern": "5x112", "offset": "ET45", "dia": "66.6", "color": "Anthracite", "material": "Cast", "price": 18000, "stock": 12},
    ]},
]

class Command(BaseCommand):
    help = 'Автоматически создает шины и диски с вариациями без логических ошибок.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Удаляю старые шины и диски...')
        TyreVariant.objects.all().delete()
        TyreModel.objects.all().delete()
        RimVariant.objects.all().delete()
        RimModel.objects.all().delete()
        self.stdout.write('Создаю новые шины и вариации...')
        for tyre in TYRES:
            tyre_model = TyreModel.objects.create(
                name=tyre["name"],
                brand=tyre["brand"],
                description=tyre["description"]
            )
            # Для каждой шины — 2-4 вариации с одним сезоном и типом шипов
            variants = random.sample(TYRE_VARIANTS, k=random.randint(2, 4))
            for v in variants:
                TyreVariant.objects.create(
                    model=tyre_model,
                    width=v[0],
                    profile=v[1],
                    radius=v[2],
                    season=tyre["season"],
                    studded=tyre["studded"],
                    speed_index=v[3],
                    price=v[4],
                    stock=v[5]
                )
        self.stdout.write('Создаю новые диски и вариации...')
        for rim in RIMS:
            rim_model = RimModel.objects.create(
                brand=rim["brand"],
                name=rim["name"],
                description=rim["description"]
            )
            for v in rim["variants"]:
                RimVariant.objects.create(
                    model=rim_model,
                    diameter=v["diameter"],
                    width=v["width"],
                    bolt_pattern=v["bolt_pattern"],
                    offset=v["offset"],
                    dia=v["dia"],
                    color=v["color"],
                    material=v["material"],
                    price=v["price"],
                    stock=v["stock"]
                )
        self.stdout.write(self.style.SUCCESS('Автозаполнение шин и дисков завершено!')) 