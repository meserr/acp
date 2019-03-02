from django.db import models

# Create your models here.
class Peptides(models.Model):
    peptide = models.CharField(max_length=50, verbose_name="Peptit")
    label = models.BooleanField(verbose_name="Etiket")
    length = models.IntegerField(verbose_name="Uzunluk")

    def __str__(self):
        return  self.peptide
