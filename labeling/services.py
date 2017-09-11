import json
import operator
from functools import reduce

from django.db.models import Q
from django.http import HttpResponse

from .models import Table, Employee, Lot, Produit, LabelingDetails, LabelingDetailsTempo, Labeling


def list_of_tables(request):
    items = list(Table.objects.all().values('id', 'table_number'))
    data = json.dumps(items)
    return HttpResponse(data, content_type='application/json')


def list_of_employee(request):
    items = list(Employee.objects.all().order_by('nom').values('id', 'nom').filter(actif=True))
    data = json.dumps(items)
    return HttpResponse(data, content_type='application/json')


def list_of_lots(request):
    q = request.GET.get('q', '')
    q = q.split(' ')
    items = list(Lot.objects.all().values(
        'id', 'lot', 'produit__produit', 'peremption', 'ppa', 'colisage', 'qtt'
    ).filter(
        reduce(operator.and_, (Q(produit__produit__icontains=x) for x in q)
               ) |
        reduce(operator.and_, (Q(lot__icontains=x) for x in q))))

    for item in items:
        item['peremption'] = item['peremption'].isoformat()
        item['ppa'] = str(item['ppa'])
    data = json.dumps(items)
    return HttpResponse(data, content_type='application/json')


def list_of_produit(request):
    items = list(Produit.objects.all().values('id', 'produit'))
    data = json.dumps(items)
    return HttpResponse(data, content_type='application/json')


def list_of_tables(request):
    items = list(Table.objects.all().values('id', 'table_number'))
    data = json.dumps(items)
    return HttpResponse(data, content_type='application/json')


def list_of_labeling(request):
    page = int(request.GET['page'])
    rows = int(request.GET['rows'])
    sort = 'id'
    order = 'asc'
    q = request.GET.get('q', None)
    try:
        sort = request.GET['sort']
        order = request.GET['order']
    except:
        pass

    if page:
        to_row = page * rows
    else:
        to_row = 10
    if rows:
        from_row = to_row - rows
    else:
        from_row = 1
    items = Labeling.objects.all().values(
        'id',
        'labeling_date',
        'table__table_number',
        'lot__lot',
        'lot__ppa',
        'lot__peremption',
        'lot__colisage',
        'lot__produit__produit',
    ).order_by(sort)
    if q:
        items = items.filter(Q(lot__produit__produit__icontains=q) | Q(lot__lot__icontains=q))
    total = items.count()
    if order == 'desc':
        items = items.reverse()
    items = list(items[from_row:to_row])
    for item in items:
        item['lot__peremption'] = item['lot__peremption'].isoformat()
        item['labeling_date'] = item['labeling_date'].isoformat()
        item['lot__ppa'] = str(item['lot__ppa'])

    data = json.dumps({'rows': items, 'total': total})
    return HttpResponse(data, content_type='application/json')


def list_of_labeling_details(request):
    if request.GET['parent_id']:
        parent_id = request.GET['parent_id']
        items = list(LabelingDetails.objects.all().values(
            'id',
            'employee__nom',
            'labeling_qtt',
            'souches_qtt',
            'unlabeling_qtt'
        ).filter(parent_id=parent_id))
        data = json.dumps(items)
        return HttpResponse(data, content_type='application/json')
    else:
        return HttpResponse(None, content_type='application/json')


def list_of_labeling_details_tempo(request):
    parent_id = int(request.GET['parent_id'])
    items = list(LabelingDetailsTempo.objects.all().values(
        'id',
        'employee__nom',
        'labeling_qtt',
        'souches_qtt',
        'unlabeling_qtt'
    ).filter(parent_id=parent_id))
    data = json.dumps(items)
    return HttpResponse(data, content_type='application/json')
