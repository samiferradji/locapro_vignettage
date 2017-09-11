from django.contrib import admin

from .models import *



class LotAdmin(admin.ModelAdmin):
    list_display = ('id', 'produit', 'lot', 'peremption', 'ppa', 'colisage', 'qtt')
    search_fields = ('produit__produit', 'lot')
    list_filter = ('produit__produit',)

class LabelingAdmin(admin.ModelAdmin):
    list_display = ('labeling_date', 'table', 'lot')
    search_fields = ('labeling_date', 'table__table_number', 'lot__lot')


class DetailsLabelingAdmin(admin.ModelAdmin):
    list_display = ('parent', 'employee', 'labeling_qtt', 'souches_qtt', 'unlabeling_qtt')

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('code_RH', 'nom', 'actif')


admin.site.register(Employee)
admin.site.register(Table)
admin.site.register(Produit)
admin.site.register(Lot, LotAdmin)
admin.site.register(Labeling, LabelingAdmin)
admin.site.register(LabelingDetails, DetailsLabelingAdmin)

admin.site.site_header = 'LOCAPRO'

# Register your models here.
