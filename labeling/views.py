import json
from datetime import timedelta

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from .models import LabelingDetailsTempo, Labeling, LabelingDetails, LabelingTempo, Employee


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')


@login_required(login_url='/login/')
def home(request):
    return render(request, "dashboard.html")


@login_required(login_url='/login/')
@permission_required('labeling.can_add_labeling')
def labeling(request):
    return render(request, "labeling.html")


@login_required(login_url='/login/')
@permission_required('labeling.can_view_history')
def history(request):
    return render(request, "history.html")


@login_required(login_url='/login/')
def production(request):
    status = ''
    status_message = ''
    if request.method == 'POST':
        user = request.user
        if request.POST['action'] == 'add_line':
            parent_id = request.POST['parent_id']
            employee_id = request.POST['employee_id']
            labeling_qtt = request.POST['labeling_qtt']
            souches_qtt = request.POST['souches_qtt']
            unlabeling_qtt = request.POST['unlabeling_qtt']
            LabelingDetailsTempo.objects.create(
                parent_id_id=parent_id,
                employee_id=employee_id,
                labeling_qtt=labeling_qtt,
                souches_qtt=souches_qtt,
                unlabeling_qtt=unlabeling_qtt,
                created_by=user
            )
            status = 'OK'
            status_message = 'Nouveau détail ajoutée'
            response = {'status': status,
                        'status_message': status_message}
            return HttpResponse(json.dumps(response), content_type='application/json')
        if request.POST['action'] == 'create_parent':
            date_operation = request.POST['date_operation']
            table_id = request.POST['table_id']
            lot_id = request.POST['lot_id']
            new_header = LabelingTempo.objects.create(
                labeling_date=date_operation,
                table_id=table_id,
                lot_id=lot_id,
                created_by=user
            )
            status = 'OK'
            status_message = 'Document créé'
            response = {'status': status,
                        'status_message': status_message, 'new_header_id': new_header.id}
            return HttpResponse(json.dumps(response), content_type='application/json')
        if request.POST['action'] == 'remove_line':
            id_line = int(request.POST['id_line'])
            LabelingDetailsTempo.objects.filter(id=id_line).delete()
            status = 'OK'
            status_message = 'Ligne supprimée'
            response = {'status': status,
                        'status_message': status_message}
            return HttpResponse(json.dumps(response), content_type='application/json')
            #  save
        if request.POST['action'] == 'cancel':
            parent_id = request.POST['parent_id']
            LabelingTempo.objects.filter(id=parent_id).delete()
            status = 'OK'
            status_message = 'Bon annulé'
            response = {'status': status,
                        'status_message': status_message}
            return HttpResponse(json.dumps(response), content_type='application/json')
        if request.POST['action'] == 'save':
            parent_id = request.POST['parent_id']
            new_header = LabelingTempo.objects.get(id=parent_id)
            new_details = LabelingDetailsTempo.objects.filter(parent_id_id=parent_id)

            saved_header = Labeling.objects.create(
                labeling_date=new_header.labeling_date,
                table_id=new_header.table_id,
                lot_id=new_header.lot_id,
                created_by=new_header.created_by
            )
            for obj in new_details:
                LabelingDetails.objects.create(
                    parent_id=saved_header.id,
                    employee_id=obj.employee_id,
                    labeling_qtt=obj.labeling_qtt,
                    souches_qtt=obj.souches_qtt,
                    unlabeling_qtt=obj.unlabeling_qtt,
                    created_by=obj.created_by
                )
            LabelingTempo.objects.filter(id=parent_id).delete()
            status = 'OK'
            status_message = 'Bon enregistré'
            response = {'status': status,
                        'status_message': status_message,
                        'new_id': saved_header.id}
            return HttpResponse(json.dumps(response), content_type='application/json')
        if request.POST['action'] == 'print':
            parent_id = request.POST['parent_id']
            parent = Labeling.objects.get(id=parent_id)
            details = LabelingDetails.objects.filter(parent_id=parent_id)
            return render(request, 'print.html', {'parent': parent, 'details': details})
        if request.POST['action'] == 'print_statistics':
            date_debut = request.POST.get('date_debut')
            date_fin = request.POST.get('date_fin')
            query = LabelingDetails.objects.values('employee__nom', 'employee__code_RH').annotate(Sum('labeling_qtt'),
                                                                                                  Sum('souches_qtt'),
                                                                                                  Sum('unlabeling_qtt'))
            query = query.order_by('employee__nom')
            query = query.filter(parent__labeling_date__range=(date_debut, date_fin))
            for obj in query:
                obj['total'] = int(obj['labeling_qtt__sum']) + int(obj['souches_qtt__sum']) + int(
                    obj['unlabeling_qtt__sum'])
            return render(request, 'print_statistics.html', {
                'date_debut': date_debut,
                'date_fin': date_fin,
                'query': query
            })


@login_required(login_url='/login/')
def statistiques(request):
    if request.GET.get('action', None) == 'vignetteurs_staticstics':
        date_debut = request.GET.get('date_debut')
        date_fin = request.GET.get('date_fin')
        query = LabelingDetails.objects.values('employee__nom').annotate(Sum('labeling_qtt'), Sum('souches_qtt'),
                                                                         Sum('unlabeling_qtt'))
        query = query.filter(parent__labeling_date__range=(date_debut, date_fin))
        query = list(query)
        return HttpResponse(json.dumps(query), content_type='application/json')
    if request.GET.get('action', None) == 'lot_statistics':
        date_debut = request.GET.get('date_debut')
        date_fin = request.GET.get('date_fin')
        query = LabelingDetails.objects.values(
            'parent__lot__lot',
            'parent__lot__produit__produit',
            'parent__lot__qtt'
        ).annotate(Sum('labeling_qtt'), Sum('souches_qtt'),
                   Sum('unlabeling_qtt'))
        query = query.filter(parent__labeling_date__range=(date_debut, date_fin))
        query = list(query)
        return HttpResponse(json.dumps(query), content_type='application/json')
    if request.GET.get('action', None) == 'vignetteurs_staticstics_chart':

        date_debut = request.GET.get('date_debut')
        date_fin = request.GET.get('date_fin')
        query = LabelingDetails.objects.values('employee__nom').annotate(Sum('labeling_qtt'), Sum('souches_qtt'),
                                                                         Sum('unlabeling_qtt')
                                                                         ).order_by('labeling_qtt__sum').reverse()

        query = query.filter(parent__labeling_date__range=(date_debut, date_fin))
        query = list(query)
        for obj in query:
            obj['data'] = [
                int(obj['labeling_qtt__sum']) + int(obj['souches_qtt__sum']) + int(obj['unlabeling_qtt__sum']), ]
            obj['name'] = obj['employee__nom']

        return HttpResponse(json.dumps(query), content_type='application/json')
    if request.GET.get('action', None) == 'vignetteurs_staticstics_by_day_chart':
        date_debut = request.GET.get('date_debut')
        date_fin = request.GET.get('date_fin')
        try:
            vignetteur_id = request.GET.get('vignetteur')
            query = LabelingDetails.objects.filter(employee_id=vignetteur_id).order_by('parent__labeling_date')
        except:
            vignetteur = Employee.objects.all().order_by('nom').first()
            query = LabelingDetails.objects.filter(employee=vignetteur).order_by('parent__labeling_date')
            vignetteur_id = vignetteur.id
        query = query.filter(parent__labeling_date__range=(date_debut, date_fin))
        query = query.values('parent__labeling_date').annotate(Sum('labeling_qtt'), Sum('souches_qtt'),
                                                               Sum('unlabeling_qtt'))
        for obj in query:
            obj['parent__labeling_date'] = obj['parent__labeling_date'].isoformat()
            obj['data'] = [
                int(obj['labeling_qtt__sum']) + int(obj['souches_qtt__sum']) + int(obj['unlabeling_qtt__sum']), ]
            obj['name'] = obj['parent__labeling_date']
            obj['vignetteur'] = vignetteur_id

        query = list(query)

        return HttpResponse(json.dumps(query), content_type='application/json')


@login_required(login_url='/login/')
@permission_required('labeling.can_view_statistics')
def statistiques_view(request):
    date_debut = timezone.now().date() - timedelta(days=30)
    date_fin = timezone.now().date()
    return render(request, 'statistics.html', {'date_debut': date_debut.isoformat(), 'date_fin': date_fin.isoformat()})


@login_required(login_url='/login/')
@permission_required('labeling.can_view_statistics')
def dashboard(request):
    date_debut = timezone.now().date() - timedelta(days=30)
    date_fin = timezone.now().date()
    return render(request, 'dashboard.html', {'date_debut': date_debut.isoformat(), 'date_fin': date_fin.isoformat()})
