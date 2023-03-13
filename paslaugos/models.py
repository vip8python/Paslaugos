from django.db import models
from django.db.models import Sum


class AutomobilioModelis(models.Model):
    marke = models.CharField(max_length=50)
    modelis = models.CharField(max_length=50)
    virselis = models.ImageField(upload_to='virseliai', null=True)

    class Meta:
        verbose_name = 'Automobilio modelis'
        verbose_name_plural = 'Automobilio modeliai'
        db_table = 'automobilio modelis'

    def __str__(self):
        return f'{self.marke} {self.modelis}'


class Automobilis(models.Model):
    valstybinis_nr = models.CharField(max_length=20)
    automobilio_modelis = models.ForeignKey(AutomobilioModelis, on_delete=models.SET_NULL, null=True)
    vin_kodas = models.CharField(max_length=20, null=True)
    klientas = models.CharField(max_length=50, null=True)
    defektai = models.TextField(max_length=2500, default='')
    virselis = models.ImageField(upload_to='covers', null=True)
    class Meta:
        verbose_name = 'Automobilis'
        verbose_name_plural = 'Automobiliai'
        db_table = 'automobilis'

    def __str__(self):
        return f'{self.klientas} : {self.automobilio_modelis} --> {self.valstybinis_nr}'


class Uzsakymas(models.Model):
    data = models.DateTimeField(auto_now=True)
    automobilis = models.ForeignKey(Automobilis, on_delete=models.CASCADE, null=True)
    suma = models.DecimalField(default=0, decimal_places=2, max_digits=8)

    STATUSAS = (
        ('p', 'Priimtas'),
        ('v', 'Vykdomas'),
        ('i', 'Įvykdytas'),
        ('a', 'Apmokėtas'),
    )
    status = models.CharField('Užsakymo statusas',
                              max_length=1,
                              choices=STATUSAS,
                              blank=True,
                              default='s',
                              help_text='Pažymėti užsakymo statusą, pirminis - "Suformuotas"',
                              )

    class Meta:
        ordering = ['data']
        verbose_name = 'Uzsakymas'
        verbose_name_plural = 'Uzsakymai'
        db_table = 'uzsakymas'

    def __str__(self):
        return f"{self.data.strftime('%Y-%m-%d %H:%M')} - {self.automobilis} : {self.suma}"


class Paslauga(models.Model):
    pavadinimas = models.CharField(max_length=50, null=True)
    kaina = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    aprasymas = models.TextField(max_length=5000, default='')
    class Meta:
        verbose_name = 'Paslauga'
        verbose_name_plural = 'Paslaugos'
        db_table = 'paslaugos'

    def __str__(self):
        return f'{self.pavadinimas}'


class UzsakymoEilute(models.Model):
    paslauga = models.ForeignKey(Paslauga, on_delete=models.SET_NULL, null=True)
    uzsakymas = models.ForeignKey(Uzsakymas, on_delete=models.SET_NULL, null=True)
    kiekis = models.IntegerField(default=0)
    kaina = models.DecimalField(default=0, decimal_places=2, max_digits=8)

    class Meta:
        verbose_name = 'Uzsakymo eilute'
        verbose_name_plural = 'Uzsakymo eilutes'
        db_table = 'uzsakymo eilutes'

    def __str__(self):
        return f'{self.paslauga} - {self.uzsakymas} - {self.kaina}'

    def save(self, *args, **kwargs):
        self.kaina = self.kiekis * self.paslauga.kaina
        super().save(*args, **kwargs)
        uzsakymas = self.uzsakymas
        uzsakymas.suma = uzsakymas.uzsakymoeilute_set.all().aggregate(Sum('kaina'))['kaina__sum'] or 0
        uzsakymas.save()

