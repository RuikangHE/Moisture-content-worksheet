from django.test import TestCase
from core.models import MoistureContent
from decimal import Decimal

# Create your tests here.
class MoistureContentModelTests(TestCase):
    """
    Test calculations in question 2 
    """
    def setUp(self):
        MoistureContent.objects.create(
            tare_id='MT001',
            tare_mass=300.0,
            tare_and_material_wet_mass=2859.6,
            dry_mass_bal='01BAL',
            tare_and_material_dry_mass=2525.7,
        )
        MoistureContent.objects.create(
            tare_id='MT002',
            tare_mass=500.0,
            tare_and_material_wet_mass=2336.6,
            dry_mass_bal='01BAL',
            tare_and_material_dry_mass=2021.9,
        )
    
    def test_material_wet_mass_calculations(self):
        mc_1 = MoistureContent.objects.get(tare_id='MT001')
        mc_2 = MoistureContent.objects.get(tare_id='MT002')
        self.assertEqual(mc_1.material_wet_mass, Decimal('2559.6'))
        self.assertEqual(mc_2.material_wet_mass, Decimal('1836.6'))       

    def test_material_dry_mass_calculations(self):
        mc_1 = MoistureContent.objects.get(tare_id='MT001')
        mc_2 = MoistureContent.objects.get(tare_id='MT002')
        self.assertEqual(mc_1.material_dry_mass, Decimal('2225.7'))
        self.assertEqual(mc_2.material_dry_mass, Decimal('1521.9'))

    def test_water_content_calculations(self):
        mc_1 = MoistureContent.objects.get(tare_id='MT001')
        mc_2 = MoistureContent.objects.get(tare_id='MT002')
        self.assertEqual(mc_1.water_content, '15.0%')
        self.assertEqual(mc_2.water_content, '20.7%')
