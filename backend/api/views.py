from django.shortcuts import render, redirect, get_object_or_404
from .modelsdb import Usuario, Pilot, Farm, Talhao, Product, Aeronave, Guia_aplicacao_supervisor, Guia_aplicacao_piloto, AuthUser, Foto_cond_atmosferica, Foto_produto, Foto_trajeto, Foto_panoramica, Receita
from .forms import PilotsForm, FarmForm, TalhaoForm, ProductsForm, AeronaveForm, GuiaAplicacaoSupForm, GuiaAplicacaoPilotoForm, CustomUserForm, ReceitaForm
from django.forms import modelformset_factory
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import JsonResponse
import ast
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.db import IntegrityError

import base64
from django.core.files.base import ContentFile

def role_required(role):
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if hasattr(request.user, 'profile') and request.user.profile.role == role:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You don't have permission to access this page.")
        return _wrapped_view
    return decorator

# roles: 1 - supervisor, 10 - piloto
def index(request): 
    loginForm = CustomUserForm()      
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        #campos vazios
        if not password or not username:
            return render(request, 'index.html')

        userL = authenticate(request, username=username, password=password)
        if hasattr(userL, 'profile'):
            user_role = userL.profile.role 
            login(request, userL)
            if user_role == '1':
                next_url = request.GET.get('next', '/home/')
                return HttpResponseRedirect(next_url)
                # return redirect(page_r1)  
            elif user_role == '10':
                return redirect(page_r2)  

        user = Usuario.objects.filter(username=username).first()
        if not user or user.passwd != password:
            messages.error(request, 'Usuário ou Senha Incorretos.', extra_tags='msg_index')
            return render (request, 'index.html', {'form': loginForm})
        elif user.passwd == password and user.role == '1':
            request.session['username'] = user.username
            return redirect(page_r1)
        elif user.passwd == password and user.role == '10':
            request.session['cpf'] = user.cpf
            return redirect(page_r2)   
        
    loginForm = CustomUserForm()     
    return render (request, 'index.html', {'form': loginForm})


def logout_view(request):
    logout(request)  # This logs out the user by clearing the session
    return redirect(index)  # Redirect to the login page or any other page


@role_required('1')
def page_r1(request):
    if request.user.is_authenticated:
        print(f"Hello, {request.user.username}")
    else:
        print("You are not logged in.")
    return render (request, 'page_r1.html')


@role_required('10')
def page_r2(request):
    return render (request, 'page_r2.html')


@login_required
def pilot_registration(request, pk=None):
    if pk: 
        instance = get_object_or_404(Pilot, pk=pk)
        action = 'edited'    
    else:
        instance = None
        action = 'added'

    if request.method == 'POST':
        if "delete" in request.POST:
            try:  
                instance.delete()
                return redirect(pilot_list)
            except IntegrityError:
                messages.error(request, "Não é possível excluir este piloto porque ele está sendo referenciada por outros objetos.", extra_tags='msg_pilot')
                return redirect (pilot_registration)    
        
        name = request.POST['name']
        cpf = request.POST['cpf']
        birth_date = request.POST['birth_date']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        phone_number = request.POST['phone_number']
        hiring_date = request.POST['hiring_date']
        
        info = {'name': name, 'cpf': cpf, 'birth_date': birth_date, 'address': address, 'city': city, 'state': state, 'phone_number': phone_number, 'hiring_date': hiring_date}
        
        #campos vazios
        if not name or not cpf or not birth_date or not address or not city or not state or not phone_number or not hiring_date:
            return render(request, 'pilot_registration.html')
        
        pilot = PilotsForm(request.POST, instance=instance)
        if pilot.is_valid():
            is_active = request.POST.get('is_active_hidden') == 'true'
            pilot.instance.active = is_active
            # if instance:
            #     pilot.instance.cpf = instance.cpf
            pilot.save()
            if action == 'edited':
                messages.success(request, 'Piloto Editado!', extra_tags='msg_pilot')
            else:
                messages.success(request, 'Piloto Adicionado!', extra_tags='msg_pilot')
            return redirect(pilot_registration)
        elif not pilot.is_valid():
            if action == 'edited':
                messages.error(request, 'Ocorreu um Erro ao Editar o Piloto.', extra_tags='msg_pilot')
            else:
                messages.error(request, 'Ocorreu um Erro ao Adicionar o Piloto.', extra_tags='msg_pilot')
            return redirect (pilot_registration)
    else:
        form = PilotsForm(instance=instance)
        btn_value = 'Adicionar' if None else 'Editar' 

    return render(request, 'pilot_registration.html', {'form': form, 'pk': pk})

@login_required
def pilot_list(request, pk=None):
    pilot_info = Pilot.objects.all().order_by('cpf').values()

    return render (request, 'pilot_list.html', {'pilot_list': pilot_info})


def edit_pilot(request, pk):
    item = Pilot.objects.get(pk=pk)
    form = PilotsForm(instance=item)
    return render(request, 'pilot_registration.html', {'form': form})


@login_required
def pilot_list2(request):
    pilot_info = Pilot.objects.all().order_by('cpf').values()
    paginator = Paginator(pilot_info, 7)  # Show 30 items per page

    page_number = request.GET.get('page')
    pilot_list = paginator.get_page(page_number)

    return render (request, 'pilot_list2.html', {'pilot_list': pilot_list})


farm_id = {'id': None, 'name': None}
@login_required
def farm_registration(request, idt=None, idf=None):
    info = Farm.objects.all().values('id_farm', 'name')
    item = None
    if idf: 
        instanceF = get_object_or_404(Farm, pk=idf)
        actionF = 'edited'    
    else:
        instanceF = None
        actionF = 'added'

    if idt: 
        instanceT = get_object_or_404(Talhao, pk=idt)
        item = Talhao.objects.select_related('farm').get(pk=idt)
        actionT = 'edited'    
    else:
        instanceT = None
        actionT = 'added'
        
    if request.method == 'POST':
        if "deleteF" in request.POST: 
            try:
                instanceF.delete()
                return redirect(farm_list)
            except IntegrityError:
                messages.error(request, "Não é possível excluir esta fazenda porque ela está sendo referenciada por outros objetos.", extra_tags='msg_farm')
                return redirect (farm_registration)
        if "deleteT" in request.POST:  
            instanceT.delete()
            return redirect(farm_talhao_list)
        
        if 'submit-fazenda' in request.POST:
            farm_form = FarmForm(request.POST, instance=instanceF)
            if farm_form.is_valid():
                farm_form.save()
                if actionF == 'edited':
                    messages.success(request, 'Fazenda Editada!', extra_tags='msg_farm')
                else:
                    messages.success(request, 'Fazenda Adicionada!', extra_tags='msg_farm')
                farm_id['id'] = request.POST['id_farm']
                farm_id['name'] = request.POST['name']

                return redirect (farm_registration)
            elif not farm_form.is_valid():
                if actionF == 'edited':
                     messages.success(request, 'Ocorreu um Erro ao Adicionar a Fazenda.', extra_tags='msg_farm')
                else:
                    messages.success(request, 'Ocorreu um Erro ao Adicionar a Fazenda.', extra_tags='msg_farm')
                return redirect (farm_registration)
        
        elif 'submit-talhao' in request.POST:
            talhao_form = TalhaoForm(request.POST, instance=instanceT)
            if talhao_form.is_valid():
                talhao_form.save()
                if actionT == 'edited':
                    messages.success(request, 'Talhão Editado!', extra_tags='msg_farm')
                else:
                    messages.success(request, 'Talhão Adicionado!', extra_tags='msg_farm')
                return redirect (farm_registration)
            elif not talhao_form.is_valid():
                if actionT == 'edited':
                    messages.success(request, 'Ocorreu um Erro ao Editar o Talhão.', extra_tags='msg_farm')
                else:
                    messages.success(request, 'Ocorreu um Erro ao Adicionar o Talhão.', extra_tags='msg_farm')
                return redirect (farm_registration)
    else:
        form = FarmForm(instance=instanceF)  
        form_talhao = TalhaoForm(instance=instanceT)  
    
    context = {'farm_info': info, 'farm_id': farm_id, 'form': form, 'form_talhao': form_talhao, 'idt': idt, 'idf': idf, 'talhao': item}  
    return render (request, 'farm_registration.html', context)


@login_required
def farm_list(request):
    # só mostra as faezndas que tem talhao mas acho q é pra ser
    farm_info = Farm.objects.all()

    farm_list = []

    for parent in farm_info:
        children = Talhao.objects.filter(farm_id=parent)
        total_value = children.aggregate(total=Sum('area'))['total'] or 0  # Calculate the sum

        farm_list.append({
            'farm_info': parent,
            'total_area': total_value,
        })

    context = {
        'farm_list': farm_list,
    }

    return render (request, 'farm_list.html', context)


@login_required
def farm_talhao_list(request):
    farm_info = Farm.objects.order_by('id_farm').all()
    farm_data = []
   
    for parent in farm_info:
        children = Talhao.objects.filter(farm_id=parent)
        total_value = children.aggregate(total=Sum('area'))['total'] or 0  # Calculate the sum

        if children.exists():
            farm_data.append({
                'parent': parent,
                'children': children,
                'total_value': total_value,
            })

    context = {
        'parent_data': farm_data,
    }

    return render (request, 'farm_and_talhao_list.html', context)


def edit_farm(request, pk):
    item = Farm.objects.get(pk=pk)
    form = FarmForm(instance=item)
    formTalhao = TalhaoForm()
    farm_info = item
    return render(request, 'farm_registration.html', {'form': form, 'form_talhao': formTalhao, 'item': item})


@login_required
def farm_list2(request):
    farm_info = Farm.objects.all()

    farm_list = []

    for parent in farm_info:
        children = Talhao.objects.filter(farm_id=parent)
        total_value = children.aggregate(total=Sum('area'))['total'] or 0  # Calculate the sum

        if children.exists():
            farm_list.append({
                'farm_info': parent,
                'total_area': total_value,
            })

    context = {
        'farm_list': farm_list,
    }
    return render (request, 'farm_list2.html', context)


@login_required
def farm_talhao_list2(request):
    farm_info = Farm.objects.order_by('id_farm').all()
    farm_data = []
   
    for parent in farm_info:
        children = Talhao.objects.filter(farm_id=parent)
        total_value = children.aggregate(total=Sum('area'))['total'] or 0  # Calculate the sum

        if children.exists():
            farm_data.append({
                'parent': parent,
                'children': children,
                'total_value': total_value,
            })

    context = {
        'parent_data': farm_data,
    }

    return render (request, 'farm_and_talhao_list2.html', context)


def edit_talhao(request, pk):
    item = Talhao.objects.select_related('farm').get(pk=pk)
    formTalhao = TalhaoForm(instance=item)
    form = FarmForm()
    
    return render(request, 'farm_registration.html', {'form': form, 'form_talhao': formTalhao, 'talhao': item})


@login_required
def product_registration(request, pk=None):
    if pk: 
        instance = get_object_or_404(Product, pk=pk)
        action = 'edited'    
    else:
        instance = None
        action = 'added'

    if request.method == 'POST':
        if "delete" in request.POST: 
            try: 
                instance.delete()
                return redirect(product_list)
            except IntegrityError:
                messages.error(request, "Não é possível excluir este produto porque ele está sendo referenciada por outros objetos.", extra_tags='msg_product')
                return redirect (product_registration)
    
        form = ProductsForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            if action == 'edited':
                messages.success(request, 'Produto Editado!', extra_tags='msg_product')
            else:
                messages.success(request, 'Produto Adicionado!', extra_tags='msg_product')
            return redirect(product_registration)
        elif not form.is_valid():
            if action == 'edited':
                messages.error(request, 'Ocorreu um Erro ao Editar o Produto.', extra_tags='msg_product')
            else:
                messages.error(request, 'Ocorreu um Erro ao Adicionar o Produto.', extra_tags='msg_product')
            return render (request, 'product_registration.html', {'form': form})
    else:
        form = ProductsForm(instance=instance)

    return render (request, 'product_registration.html', {'form': form, 'pk': pk})


@login_required
def product_list(request):
    product_list = Product.objects.all().order_by('id').values()

    return render (request, 'product_list.html', {'product_list': product_list})


def edit_product(request, pk):
    item = Product.objects.get(pk=pk)
    form = ProductsForm(instance=item)
    return render(request, 'product_registration.html', {'form': form})


@login_required
def product_list2(request):
    product_list = Product.objects.all().order_by('id').values()

    return render (request, 'product_list2.html', {'product_list': product_list})


@login_required
def aeronave_registration(request, pk=None):   
    if pk: 
        instance = get_object_or_404(Aeronave, pk=pk)
        action = 'edited'    
    else:
        instance = None
        action = 'added'

    if request.method == 'POST':
        if "delete" in request.POST:
            try:  
                instance.delete()
                return redirect(aeronave_list)
            except IntegrityError:
                messages.error(request, "Não é possível excluir esta aeronave porque ela está sendo referenciada por outros objetos.", extra_tags='msg_aeronave')
                return redirect (aeronave_registration)
        
        form = AeronaveForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            if action == 'edited':
                messages.success(request, 'Aeronave Editada!', extra_tags='msg_aeronave')
            else:
                messages.success(request, 'Aeronave Adicionada!', extra_tags='msg_aeronave')
            return redirect(aeronave_registration)
        elif not form.is_valid():
            if action == 'edited':
                messages.error(request, 'Ocorreu um Erro ao Editar a Aeronave.', extra_tags='msg_aeronave')
            else:
                messages.error(request, 'Ocorreu um Erro ao Adicionar a Aeronave.', extra_tags='msg_aeronave')
    else:
        form = AeronaveForm(instance=instance)

    return render (request, 'aeronave_registration.html', {'form': form, 'pk': pk})


@login_required
def aeronave_list(request):
    aero_info = Aeronave.objects.all().order_by('id').values()
    
    return render (request, 'aeronave_list.html', {'aero_info': aero_info})


def edit_aeronave(request, pk):
    item = Aeronave.objects.get(pk=pk)
    form = AeronaveForm(instance=item)
    return render(request, 'aeronave_registration.html', {'form': form})


@login_required
def aeronave_list2(request):
    aero_info = Aeronave.objects.all().order_by('id').values()
    
    return render (request, 'aeronave_list2.html', {'aero_info': aero_info})


ReceitaFormSet = modelformset_factory(Receita, form=ReceitaForm, extra=0)

@login_required
def guia_aplicacao(request, id=None):
    # username = request.session.get('username')  # Get the username from the session
    username = request.user.username
    if username:
        try:
            # Get the User object associated with the username
            user = Usuario.objects.get(username=username)
        except Usuario.DoesNotExist:
            user = None  # Handle the case where the user does not exist
    
    action = 'added'
    # fazer uns comentarios aqui urgente
    if id: 
        instance = get_object_or_404(Guia_aplicacao_supervisor, pk=id)
        form = GuiaAplicacaoSupForm(request.POST or None, instance=instance)
        formset = ReceitaFormSet(queryset=Receita.objects.filter(id_guia_sup=instance))
        action = 'edited'
        
        item = Guia_aplicacao_supervisor.objects.get(pk=id)
        talhoes = item.get_talhao()
    
        context = {
            'form': form,
            'formReceita': formset,
            'serialized_data': talhoes,
            'id_guia': int(item.cod_aplicacao),
        }
        print("a1",instance)    
    else:
        form = GuiaAplicacaoSupForm(session_username=username)
        formset = ReceitaFormSet(queryset=Receita.objects.none())
        instance = None
        context = {
            'form': form,
            'formReceita': formset,
        }
        print("a",instance) 

    if request.method == 'POST':    
        pk = request.POST.get('cod_aplicacao')  
        if pk:
            
            try:
                instance = Guia_aplicacao_supervisor.objects.get(pk=pk)

                if "delete" in request.POST: 
                    try: 
                        instance.delete()
                        return redirect(guia_aplicacao_list)
                    except IntegrityError:
                        messages.error(request, "Não é possível excluir esta fazenda porque ela está sendo referenciada por outros objetos.", extra_tags='msg_guia')
                        return redirect (farm_registration)
            
                form = GuiaAplicacaoSupForm(request.POST, instance=instance)
                action = 'edited'
                item = Guia_aplicacao_supervisor.objects.get(pk=id)
                talhoes = item.get_talhao()
                context = {
                    'form': form,
                    'formReceita': ReceitaForm(),
                    'serialized_data': talhoes,
                    'id_guia': int(item.cod_aplicacao),
                }
            except Guia_aplicacao_supervisor.DoesNotExist:
                # If the PK does not exist, create a new instance
                form = GuiaAplicacaoSupForm(request.POST)
                formset = ReceitaFormSet(queryset=Receita.objects.none())
                context = {
                    'form': form,
                    'formReceita': formset,
                }
        else:
            # If no PK is provided, create a new instance
            form = GuiaAplicacaoSupForm(request.POST)
            formset = ReceitaFormSet(queryset=Receita.objects.none())
            context = {
                    'form': form,
                    'formset': formset
            }
        form = GuiaAplicacaoSupForm(request.POST, session_username=username, instance=instance)
        formset = ReceitaFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            obj = form.save(commit=False)  # Don't save yet
            obj.id_responsavel_global = AuthUser.objects.get(id=request.user.id)  # You can also set the user here if needed
            
            # parent_selection = form.save(commit=False)
            selected_child_ids = form.cleaned_data['talhao']
            data_list = ast.literal_eval(selected_child_ids)
            
            ','.join(map(str, form.cleaned_data['talhao']))
            talhoes = ','.join(map(str, data_list))
            obj.set_talhao(talhoes)
            
            obj.save() 
            
            for form in formset:
                receita = form.save(commit=False)
                receita.id_guia_sup = obj
                receita.save()

            if action == 'edited':
                messages.success(request, 'Guia Editada!', extra_tags='msg_guia')
            else:
                messages.success(request, 'Guia Adicionada!', extra_tags='msg_guia')
            return redirect(guia_aplicacao)
        elif not form.is_valid() or not formset.is_valid():
            print("Formset management form errors:", formset.non_form_errors())  # For management-level issues
            for form in formset:
                print("Form errors:", form.errors)  # For individual form errors
            if action == 'edited':
                messages.error(request, 'Ocorreu um Erro ao Editar a Guia.', extra_tags='msg_guia')
            else:
                messages.error(request, 'Ocorreu um Erro ao Adicionar a Guia.', extra_tags='msg_guia')

    return render (request, 'guia_aplicacao.html', context)

@login_required
def guia_aplicacao_list(request):
    guia_list = Guia_aplicacao_supervisor.objects.prefetch_related('id_receita', 'receita_set').select_related('id_piloto', 'id_fazenda', 'id_responsavel_global', 'guia_aplicacao_piloto').order_by('data').all()
    
    if request.method == 'POST':
        verificar = 'verificar' in request.POST
        id_aplicacao = request.POST.get('id_aplicacao')
        guia = get_object_or_404(Guia_aplicacao_supervisor, cod_aplicacao=id_aplicacao)
        if verificar:
            guia.realizado = verificar
            guia.save()

    return render (request, 'guia_aplicacao_list.html', {'guia_data': guia_list})


@login_required
def guia_aplicacao_piloto(request, pk=None):
    form = GuiaAplicacaoPilotoForm()
    cpfPiloto = request.user.profile.cpf
    # form_foto = FotoProdutoForm()
    # seleciona as guias do piloto, que ainda nao tem relacao com a tabela guia_aplicacao_piloto
    guias = Guia_aplicacao_supervisor.objects.prefetch_related('id_receita', 'receita_set').select_related('id_responsavel_global').filter(id_piloto=cpfPiloto, guia_aplicacao_piloto__isnull=True).order_by('data').all()

    context = {
        'form': form,
        'guias': guias,
    }
    
    pk = request.POST.get('id_aplicacao') 
    if pk:
        try:
            instance = Guia_aplicacao_piloto.objects.get(pk=pk)
            form = GuiaAplicacaoPilotoForm(request.POST, instance=instance)
            action = 'edited'
        except Guia_aplicacao_piloto.DoesNotExist:
            form = GuiaAplicacaoPilotoForm(request.POST)
    else:
        form = GuiaAplicacaoPilotoForm(request.POST)

    if request.method == 'POST':
        if "delete" in request.POST:
            try:  
                instance.delete()
                return redirect(guia_piloto_list)
            except IntegrityError:
                messages.error(request, "Não é possível excluir esta guia porque ela está sendo referenciada por outros objetos.", extra_tags='msg_guia_piloto')
                return redirect (guia_aplicacao_piloto)

        if form.is_valid():
            guia_id = request.POST['id_aplicacao']

            info = form.save(commit=False)
            guia = get_object_or_404(Guia_aplicacao_supervisor, cod_aplicacao=guia_id)

            guia.save()  

            info.save()
            instance = info
            
            # delete existing images
            images_to_delete_farm = request.POST.get('images_to_delete_farm', '').split(',')
            for image_id in images_to_delete_farm:
                if image_id:
                    Foto_panoramica.objects.filter(id_foto=image_id).delete()

            images_to_delete_prod = request.POST.get('images_to_delete_prod', '').split(',')
            for image_id in images_to_delete_prod:
                if image_id:
                    Foto_produto.objects.filter(id_foto=image_id).delete()

            images_to_delete_cond = request.POST.get('images_to_delete_cond', '').split(',')
            for image_id in images_to_delete_cond:
                if image_id:
                    Foto_cond_atmosferica.objects.filter(id_foto=image_id).delete()

            images_to_delete_traj = request.POST.get('images_to_delete_traj', '').split(',')
            for image_id in images_to_delete_traj:
                if image_id:
                    Foto_panoramica.objects.filter(id_foto=image_id).delete()

            # upload images
            fileset1 = request.FILES.getlist('ft_panoramica')
            for f in fileset1:
                Foto_panoramica.objects.create(id_aplicacao=info, foto=f.read())  # Save each file to PhotoSet1

            # Handle files for PhotoSet2
            fileset2 = request.FILES.getlist('ft_produto')
            for f in fileset2:
                Foto_produto.objects.create(id_aplicacao=info, foto=f.read())  # Save each file to PhotoSet2

            # Handle files for PhotoSet2
            fileset4 = request.FILES.getlist('ft_cond_atmosferica')
            for f in fileset4:
                Foto_cond_atmosferica.objects.create(id_aplicacao=info, foto=f.read())  # Save each file to PhotoSet2

            # Handle files for PhotoSet2
            fileset3 = request.FILES.getlist('ft_trajeto')
            for f in fileset3:
                Foto_trajeto.objects.create(id_aplicacao=info, foto=f.read())  # Save each file to PhotoSet2

            messages.success(request, 'Guia Adicionada!', extra_tags='msg_guia_piloto')
            return redirect(guia_aplicacao_piloto)
        elif not form.is_valid():
            messages.error(request, 'Ocorreu um Erro ao Adicionar a Guia.', extra_tags='msg_guia_piloto')
            return render (request, 'guia_aplicacao_piloto.html', context)

    return render (request, 'guia_aplicacao_piloto.html', context)


@login_required
def guia_piloto_list(request):
    cpfPiloto = request.user.profile.cpf
    guiaData = Guia_aplicacao_piloto.objects.filter(id_aplicacao_id__id_piloto=cpfPiloto).select_related('id_aplicacao').prefetch_related('foto_produto_set', 'foto_trajeto_set').order_by('-data_realizacao')

    return render (request, 'guia_piloto_list.html', {'guia_with_images': guiaData})

def edit_guia(request, pk):
    item = Guia_aplicacao_supervisor.objects.get(pk=pk)
    form = GuiaAplicacaoSupForm(instance=item)
    talhoes = item.get_talhao()
    formset = ReceitaFormSet(queryset=Receita.objects.filter(id_guia_sup=item))

    context = {
        'form': form,
        'serialized_data': talhoes,
        'formReceita': formset
    }
    
    return render(request, 'guia_aplicacao.html', context)

def edit_guia_piloto(request, pk):
    item = Guia_aplicacao_piloto.objects.get(pk=pk)
    form = GuiaAplicacaoPilotoForm(instance=item)

    cpfPiloto = request.session.get('cpf')
    # seleciona as guias do piloto, que ainda nao tem relacao com a tabela guia_aplicacao_piloto
    guias = Guia_aplicacao_supervisor.objects.filter(cod_aplicacao=pk).order_by('data').all()

    product_images = [
    {'id': prod.id_foto, 'foto':base64.b64encode(prod.foto).decode('utf-8') if prod.foto else None}
        for prod in item.foto_produto_set.all()
    ]

    trajeto_images = [
        {'id': trajeto.id_foto, 'foto':base64.b64encode(trajeto.foto).decode('utf-8') if trajeto.foto else None}
        for trajeto in item.foto_trajeto_set.all()
    ]

    cond_atm_images = [
        {'id': conds.id_foto, 'foto': base64.b64encode(conds.foto).decode('utf-8') if conds.foto else None}
        for conds in item.foto_cond_atmosferica_set.all()
    ]

    farm_images = [
        {'id': panoramica.id_foto, 'foto': base64.b64encode(panoramica.foto).decode('utf-8') if panoramica.foto else None}
        for panoramica in item.foto_panoramica_set.all()
    ]
    
    context = {
        'form': form,
        'guias': guias,
        'foto_panoramica': farm_images,
        'foto_produto': product_images,
        'foto_trajeto': trajeto_images,
        'foto_cond_at': cond_atm_images,
    }
    
    return render(request, 'guia_aplicacao_piloto.html', context)


# ajax requests
def get_images_piloto(request, id):
    try:
        guiaSup = Guia_aplicacao_supervisor(cod_aplicacao=id) 
        guia = guiaSup.guia_aplicacao_piloto
            
        product_images = [
            base64.b64encode(prod.foto).decode('utf-8') if prod.foto else None
            for prod in guia.foto_produto_set.all()
        ]

        trajeto_images = [
            base64.b64encode(trajeto.foto).decode('utf-8') if trajeto.foto else None
            for trajeto in guia.foto_trajeto_set.all()
        ]

        cond_atm_images = [
            base64.b64encode(conds.foto).decode('utf-8') if conds.foto else None
            for conds in guia.foto_cond_atmosferica_set.all()
        ]

        farm_images = [
            base64.b64encode(panoramica.foto).decode('utf-8') if panoramica.foto else None
            for panoramica in guia.foto_panoramica_set.all()
        ]

        context = {
            'images': {
                'produto_imgs': product_images,
                'trajeto_imgs': trajeto_images,
                'cond_atm_imgs': cond_atm_images,
                'farm_imgs': farm_images
            }
        }
        return JsonResponse(context)
    except Guia_aplicacao_piloto.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)
    
def fetch_data_view(request, pk):
    instance = get_object_or_404(Pilot, pk=pk)  # Retrieve the instance
    data = {
        'name': instance.name,
        'cpf': instance.cpf,
        'birth_date': instance.birth_date,
        'address': instance.address,
        'city': instance.city,
        'state': instance.state,
        'phone_number': instance.phone_number,
        'hiring_date': instance.hiring_date,
        'active': instance.active,
        # Include all necessary fields here
    }
    return JsonResponse(data)
    
def fetch_data_farm_view(request, pk):
    instance = get_object_or_404(Farm, pk=pk)  # Retrieve the instance

    data = {
        'id_farm': instance.id_farm,
        'name': instance.name,
        'owner': instance.owner,
        'city': instance.city,
        'state': instance.state,
        'farm': instance.id_farm,
    }

    return JsonResponse(data)


def fetch_data_guia_farm(request, pk):
    children = Talhao.objects.filter(farm=str(pk)).values()
    
    talhao_ids = Talhao.objects.values_list('farm', flat=True)
    
    response_data = {
        'children': list(children)
    }
    return JsonResponse(response_data)

def fetch_data_guia_prod(request, pk):
    product = Product.objects.get(id=pk)
    data = {
        'dosagem': product.dosagem_recomendada,
    }
    
    return JsonResponse(data)


def fetch_data_guia_talhao(request):
    if request.method == 'GET':
        child_ids = request.GET.get('selected_talhao', '')  # Get selected children IDs from the request
        
        child_ids_l = child_ids.split(',')
        children = Talhao.objects.filter(id_talhao__in=child_ids_l)
        
        response_data = {
            'children': [
                {'id': child.id_talhao, 'area': child.area}
                for child in children
            ]
        }
        
    return JsonResponse(response_data)


def fetch_guia_piloto(request, parent_id):
    children = Guia_aplicacao_piloto.objects.filter(id_aplicacao=parent_id).select_related('id_aplicacao').values()
    aferido = Guia_aplicacao_supervisor.objects.get(cod_aplicacao=parent_id).realizado

    info = {
        'guia_p': list(children),
        'aferido': aferido,
    }
    return JsonResponse(info, safe=False)