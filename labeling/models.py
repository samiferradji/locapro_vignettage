from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User)

    class Meta:
        abstract = True


class Employee(BaseModel):
    code_RH = models.CharField(max_length=10, verbose_name=" Code RH", unique=True)
    nom = models.CharField(max_length=80, verbose_name="Nom et Prénom")
    actif = models.BooleanField(verbose_name='Actif ?', default=True)

    class Meta:
        verbose_name = "Employée"

    def __str__(self):
        return self.nom


class Table(BaseModel):
    table_number = models.IntegerField(verbose_name='numéro de table')
    reponsable = models.ForeignKey(Employee, verbose_name='Responsable de la table')

    def __str__(self):
        return " ".join(("Table numéro :", str(self.table_number)))


class Produit(BaseModel):
    code = models.CharField(max_length=15, verbose_name='hightchart produit')
    produit = models.CharField(max_length=150, verbose_name='Désignation du produit')

    def __str__(self):
        return self.produit


class Lot(BaseModel):
    produit = models.ForeignKey(Produit, verbose_name="Produit")
    lot = models.CharField(max_length=20, verbose_name='Lot')
    peremption = models.DateField(verbose_name="Date de péremption")
    ppa = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='PPA')
    colisage = models.SmallIntegerField(verbose_name='Colisage')
    qtt = models.PositiveIntegerField(verbose_name='Quantité totale du lot')

    def __str__(self):
        return " ".join((str(self.produit), " Lot : ", self.lot))


class Labeling(BaseModel):
    labeling_date = models.DateField(verbose_name="Date d'exécution", default=timezone.now)
    table = models.ForeignKey(Table)
    lot = models.ForeignKey(Lot)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Rapport de vignettage"

        permissions = (
            ("can_add_labeling", "Ajouter des bons de vignettage"),
            ("can_view_history", "Voir l'historique"),
            ("can_view_statistics", "Voir les statistiques"),
            )


class LabelingTempo(BaseModel):
    labeling_date = models.DateField(verbose_name="Date d'exécution", default=timezone.now)
    table = models.ForeignKey(Table)
    lot = models.ForeignKey(Lot)

    def __str__(self):
        return str(self.id)


class LabelingDetails(BaseModel):
    parent = models.ForeignKey(Labeling)
    employee = models.ForeignKey(Employee, verbose_name="vignetteur")
    labeling_qtt = models.PositiveSmallIntegerField(verbose_name='Nombre de vignette collées')
    souches_qtt = models.PositiveSmallIntegerField(verbose_name='Nombre de souches collés')
    unlabeling_qtt = models.PositiveSmallIntegerField(verbose_name='Nombre de vignette enlevées')

    class Meta:
        verbose_name = "Détails du rapport de vignettage"


class LabelingDetailsTempo(BaseModel):
    parent_id = models.ForeignKey(LabelingTempo)
    employee = models.ForeignKey(Employee, verbose_name="vignetteur")
    labeling_qtt = models.PositiveSmallIntegerField(verbose_name='Nombre de vignette collées')
    souches_qtt = models.PositiveSmallIntegerField(verbose_name='Nombre de souches collés')
    unlabeling_qtt = models.PositiveSmallIntegerField(verbose_name='Nombre de vignette enlevées')
