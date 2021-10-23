from django.db import models
from decimal import Decimal

# Create your models here.
class MoistureContentManager(models.Manager):
    
    def create_moisture(self, tare_mass, tare_and_material_wet_mass, tare_and_material_dry_mass,  **extra_fields):
        if(tare_mass < 0 or tare_and_material_wet_mass < 0 or tare_and_material_dry_mass < 0):
            raise ValueError('Mass cannot be less than 0')
        if(Decimal(tare_mass) >= tare_and_material_wet_mass):
            raise ValueError('Tare and wet mass must be greater than tare mass')
        if(Decimal(tare_mass) >= tare_and_material_dry_mass):
            raise ValueError(f"Tare mass is {'greater than' if tare_mass > tare_and_material_dry_mass else 'equal to'}")
        if(tare_and_material_dry_mass > tare_and_material_wet_mass):
            raise ValueError('Dry mass greater than wet mass, cannot calculate a result')
        moisture_content = self.model(
            tare_mass=tare_mass,
            tare_and_material_wet_mass=tare_and_material_wet_mass,
            tare_and_material_dry_mass=tare_and_material_dry_mass,
            **extra_fields,
        )
        moisture_content.save(using=self._db) 
        return moisture_content


class MoistureContent(models.Model):
    """
    Moisture Content model which includes fields in the Measurements, Dry 
    Mass and Results sections.
    """
    BAL_01 = '01BAL'
    BAL_02 = '02BAL'
    BALANCE_CHOICES = [
        (BAL_01, '01BAL'),
        (BAL_02, '02BAL'),
    ]

    INSUFFICIENT_SAMPLE_MASS = 'ISM'
    DRYING_TEMPERATURE = 'DT'
    MATERIAL_EXCLUDED = 'ME'
    REPORT_TYPE_CHOICES = [
        (INSUFFICIENT_SAMPLE_MASS, 'Insufficient Sample Mass'),
        (DRYING_TEMPERATURE, 'Drying Temperature'),
        (MATERIAL_EXCLUDED, 'Material Excluded'),
    ]
    
    objects = MoistureContentManager()

    tare_id = models.CharField(max_length=20, unique=True)
    tare_mass = models.DecimalField(max_digits=10, decimal_places=1)
    tare_and_material_wet_mass = models.DecimalField(max_digits=10, decimal_places=1)
    dry_mass_bal = models.CharField(max_length=10, choices=BALANCE_CHOICES, default=BAL_01)
    tare_and_material_dry_mass = models.DecimalField(max_digits=10, decimal_places=1)
    report = models.CharField(max_length=200, choices=REPORT_TYPE_CHOICES, blank=True, null=True)

    @property
    def material_wet_mass(self):
        return self.tare_and_material_wet_mass - self.tare_mass
    
    @property
    def material_dry_mass(self):
        return self.tare_and_material_dry_mass - self.tare_mass
    
    @property
    def water_content(self):
        result = (self.material_wet_mass - self.material_dry_mass) / self.material_dry_mass
        return f'{round(result * 100, 1)}%'
