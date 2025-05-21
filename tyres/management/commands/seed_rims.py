from django.core.management.base import BaseCommand
from tyres.models import RimModel, RimVariant

class Command(BaseCommand):
    help = 'Seeds the database with some initial rim data.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting existing rim models and variants...')
        RimVariant.objects.all().delete()
        RimModel.objects.all().delete()
        self.stdout.write('Existing data deleted.')

        rims_data = [
            {
                'brand': 'BBS',
                'name': 'LM',
                'description': 'Легендарные составные диски',
                'variants': [
                    {'diameter': 18.0, 'width': 8.0, 'bolt_pattern': '5x120', 'offset': 'ET35', 'dia': '72.5', 'color': 'Silver', 'material': 'Forged', 'price': 50000, 'stock': 10},
                    {'diameter': 18.0, 'width': 9.0, 'bolt_pattern': '5x120', 'offset': 'ET42', 'dia': '72.5', 'color': 'Silver', 'material': 'Forged', 'price': 55000, 'stock': 8},
                ]
            },
            {
                'brand': 'OZ Racing',
                'name': 'Ultraleggera',
                'description': 'Легкие спортивные диски',
                'variants': [
                    {'diameter': 17.0, 'width': 7.5, 'bolt_pattern': '5x100', 'offset': 'ET35', 'dia': '57.1', 'color': 'Black', 'material': 'Cast', 'price': 15000, 'stock': 15},
                    {'diameter': 18.0, 'width': 8.0, 'bolt_pattern': '5x112', 'offset': 'ET45', 'dia': '66.6', 'color': 'Anthracite', 'material': 'Cast', 'price': 18000, 'stock': 12},
                ]
            },
            {
                'brand': 'Rays',
                'name': 'Volk Racing TE37',
                'description': 'Культовые кованые диски',
                'variants': [
                    {'diameter': 18.0, 'width': 9.5, 'bolt_pattern': '5x114.3', 'offset': 'ET12', 'dia': '73.1', 'color': 'Bronze', 'material': 'Forged', 'price': 70000, 'stock': 6},
                    {'diameter': 19.0, 'width': 10.5, 'bolt_pattern': '5x114.3', 'offset': 'ET22', 'dia': '73.1', 'color': 'Bronze', 'material': 'Forged', 'price': 85000, 'stock': 4},
                ]
            },
            {
                'brand': 'Work',
                'name': 'Emotion CR Kai',
                'description': 'Популярные диски для тюнинга',
                'variants': [
                    {'diameter': 17.0, 'width': 9.0, 'bolt_pattern': '5x114.3', 'offset': 'ET17', 'dia': '73.1', 'color': 'White', 'material': 'Cast', 'price': 20000, 'stock': 18},
                    {'diameter': 18.0, 'width': 9.5, 'bolt_pattern': '5x114.3', 'offset': 'ET30', 'dia': '73.1', 'color': 'Matte Bronze', 'material': 'Cast', 'price': 24000, 'stock': 14},
                ]
            },
            {
                'brand': 'Vossen',
                'name': 'HF-3',
                'description': 'Стильные литые диски',
                'variants': [
                    {'diameter': 20.0, 'width': 9.0, 'bolt_pattern': '5x112', 'offset': 'ET32', 'dia': '66.6', 'color': 'Gloss Black', 'material': 'Hybrid Forged', 'price': 40000, 'stock': 9},
                    {'diameter': 20.0, 'width': 10.5, 'bolt_pattern': '5x120', 'offset': 'ET42', 'dia': '72.5', 'color': 'Double Tinted Gloss Black', 'material': 'Hybrid Forged', 'price': 45000, 'stock': 7},
                ]
            },
            {
                'brand': 'Enkei',
                'name': 'RPF1',
                'description': 'Легкие гоночные диски',
                'variants': [
                    {'diameter': 17.0, 'width': 8.0, 'bolt_pattern': '5x100', 'offset': 'ET45', 'dia': '73.1', 'color': 'Silver', 'material': 'Cast', 'price': 16000, 'stock': 20},
                    {'diameter': 18.0, 'width': 9.0, 'bolt_pattern': '5x114.3', 'offset': 'ET35', 'dia': '73.1', 'color': 'Silver', 'material': 'Cast', 'price': 19000, 'stock': 16},
                ]
            },
            {
                'brand': 'Rotiform',
                'name': 'LAS-R',
                'description': 'Стенс-диски с интересным дизайном',
                'variants': [
                    {'diameter': 19.0, 'width': 8.5, 'bolt_pattern': '5x112', 'offset': 'ET35', 'dia': '57.1', 'color': 'Silver Machined', 'material': 'Cast', 'price': 25000, 'stock': 11},
                    {'diameter': 19.0, 'width': 10.0, 'bolt_pattern': '5x120', 'offset': 'ET40', 'dia': '72.5', 'color': 'Silver Machined', 'material': 'Cast', 'price': 28000, 'stock': 9},
                ]
            },
        ]

        for rim_data in rims_data:
            rim_model = RimModel.objects.create(
                brand=rim_data['brand'],
                name=rim_data['name'],
                description=rim_data['description']
                # image=... # Здесь можно добавить загрузку изображений, если нужно
            )
            for variant_data in rim_data['variants']:
                RimVariant.objects.create(
                    model=rim_model,
                    diameter=variant_data['diameter'],
                    width=variant_data['width'],
                    bolt_pattern=variant_data['bolt_pattern'],
                    offset=variant_data['offset'],
                    dia=variant_data['dia'],
                    color=variant_data['color'],
                    material=variant_data['material'],
                    price=variant_data['price'],
                    stock=variant_data['stock']
                    # image=... # Здесь можно добавить загрузку изображений вариантов, если нужно
                )
        self.stdout.write(self.style.SUCCESS('Successfully seeded rim data.')) 