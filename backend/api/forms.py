from django import forms
from .modelsdb import Pilot, Talhao, Farm, Product, Aeronave, Guia_aplicacao_supervisor, Guia_aplicacao_piloto, Foto_cond_atmosferica, Foto_panoramica, Foto_produto, Foto_trajeto, Receita
from django.contrib.auth.models import User

class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'inputs logininputs'
    }))

    class Meta:
        model = User
        fields = ['username', 'password']  # Include the fields you want to show in the form

    # Overriding __init__ to customize widgets
    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        
        # Add custom classes to the fields
        self.fields['username'].widget.attrs.update({'class': 'inputs logininputs', 'autofocus': 'autofocus'})
        self.fields['password'].widget.attrs.update({'class': 'inputs logininputs', 'type': 'password'})
        self.fields['password'].label = "Senha"


class PilotsForm(forms.ModelForm):
    # remove ':' do fim dos labels
    def __init__(self, *args, **kwargs):
            super(PilotsForm, self).__init__(*args, **kwargs)
            self.label_suffix = ""

            if self.instance and self.instance.pk:
                self.fields['cpf'].widget.attrs['readonly'] = True

    class Meta:
        model = Pilot
        fields = ['name', 'cpf', 'birth_date', 'address', 'city', 'state', 'phone_number', 'hiring_date', 'active']

        labels = {
            'name': 'Nome *',
            'cpf': 'CPF *',
            'birth_date': 'Data de Nascimento *',
            'address': 'Endereço *',
            'city': 'Cidade *',
            'state': 'Estado *',
            'phone_number': 'Telefone *',
            'hiring_date': 'Data de Contratação *',
            'active': '',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'inputs', 
                                           'required': 'required',        
                                           'autofocus': 'autofocus', }),
            'cpf': forms.TextInput(attrs={'class': 'inputs', 'id': 'cpf', 'name': 'cpf', 'required': 'required', }),
            'birth_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'inputs', 'required': 'required', 'type': 'date'}),
            'address': forms.TextInput(attrs={'class': 'inputs', 'required': 'required','name': 'address'}),
            'city': forms.TextInput(attrs={'class': 'inputs', 'required': 'required'}),
            'state': forms.TextInput(attrs={'class': 'inputs', 'required': 'required'}),
            'phone_number': forms.TextInput(attrs={'class': 'inputs', 'id':'phone_number', 'name': 'phone_number', 'required': 'required'}),
            'hiring_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'inputs', 'required': 'required', 'type': 'date', 'placeholder': 'Selecione a Data'}),
            'active': forms.CheckboxInput(attrs={'class': 'checkbox-activity', 'id': 'active', 'name': 'active'}),
        }
        

class FarmForm(forms.ModelForm):
    # remove ':' do fim dos labels
    def __init__(self, *args, **kwargs):
        super(FarmForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""
        if self.instance and self.instance.pk:
            self.fields['id_farm'].widget.attrs['readonly'] = True
    
    class Meta:
        model = Farm
        fields = ['id_farm', 'name', 'owner', 'city', 'state']

        labels = {
            'id_farm': 'Código da Fazenda *',
            'name': 'Nome da Fazenda *',
            'owner': 'Grupo/Proprietário *',
            'city': 'Cidade *',
            'state': 'Estado *',
        }

        widgets = {
            'id_farm': forms.TextInput(attrs={'class': 'inputs', 'required': 'required'}),
            'name': forms.TextInput(attrs={'class': 'inputs', 'required': 'required', 'type': 'text'}),
            'owner': forms.TextInput(attrs={'class': 'inputs', 'required': 'required'}),
            'city': forms.TextInput(attrs={'class': 'inputs', 'required': 'required'}),
            'state': forms.TextInput(attrs={'class': 'inputs', 'required': 'required'}),
        }


class TalhaoForm(forms.ModelForm):
    # remove ':' do fim dos labels
    def __init__(self, *args, **kwargs):
        super(TalhaoForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""
        if self.instance and self.instance.pk:
            self.fields['farm'].widget.attrs['readonly'] = True
            self.fields['id_talhao'].widget.attrs['readonly'] = True

    class Meta:
        model = Talhao
        fields = ['farm', 'id_talhao', 'area', 'technician']

        labels = { 
            'farm': 'Código da Fazenda *',
            'id_talhao': 'Código do Talhão *',
            'area': 'Área (ha) *',
            'technician': 'Resposável de Área'
        }

        widgets = {
            'farm': forms.Select(attrs={'class': 'inputs', 'required': 'required', 'name': 'farm', 'id': 'farm'}),
            'id_talhao': forms.NumberInput(attrs={'class': 'inputs', 'required': 'required'}),
            'area': forms.NumberInput(attrs={'class': 'inputs', 'required': 'required'}),
            'technician': forms.TextInput(attrs={'class': 'inputs'}), 
        }


class ProductsForm(forms.ModelForm):
    # remove ':' do fim dos labels
    def __init__(self, *args, **kwargs):
        super(ProductsForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""
        if self.instance and self.instance.pk:
            self.fields['id'].widget.attrs['readonly'] = True

    class Meta:
        model = Product

        fields = ['id', 'nome_comercial', 'grupo_produto', 'principio_ativo', 'dosagem_recomendada', 'observacao']  # Specify which fields to include
        
        labels = {
            'id': 'Código do Produto',
            'nome_comercial': 'Nome Comercial',
            'grupo_produto': 'Grupo do Produto',
            'principio_ativo': 'Princípio Ativo',
            'dosagem_recomendada': 'Dosagem Recomendada (L/ha)',
            'taxa_aplicacao': 'Taxa de Aplicação (L)',
            'observacao': 'Observações',
        }
        
        widgets = {
            'id': forms.NumberInput(attrs={'class': 'inputs', 'required': 'required'}),
            'nome_comercial': forms.TextInput(attrs={'class': 'inputs', 'required': 'required'}),
            'grupo_produto': forms.Select(),
            'principio_ativo': forms.TextInput(attrs={'class': 'inputs', 'required': 'required'}),
            'dosagem_recomendada': forms.TextInput(attrs={'class': 'inputs', 'required': 'required'}),
            'taxa_aplicacao': forms.TextInput(attrs={'class': 'inputs', 'required': 'required'}),
            'observacao': forms.TextInput(attrs={'class': 'inputs obs'}),
        }


class AeronaveForm(forms.ModelForm):
    # remove ':' do fim dos labels
    def __init__(self, *args, **kwargs):
        super(AeronaveForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""
        if self.instance and self.instance.pk:
            self.fields['id'].widget.attrs['readonly'] = True

    class Meta:
        model = Aeronave
        fields = ['id', 'model', 'manufacturer', 'capacity']

        labels = {
            'id': 'Código da Aeronave *',
            'model': 'Modelo *',
            'manufacturer': 'Fabricante *',
            'capacity': 'Capacidade de Carga (litros) *',
        }

        widgets = {
            'id': forms.TextInput(attrs={'class': 'inputs', 'required': 'required'}),
            'model': forms.TextInput(attrs={'class': 'inputs', 'required': 'required'}),
            'manufacturer': forms.Select(attrs={'class': '', 'required': 'required'}),
            'capacity': forms.NumberInput(attrs={'class': 'inputs', 'required': 'required'}),
        }


class GuiaAplicacaoSupForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        username = kwargs.pop('session_username', None)  # Pass the username dynamically
        print(username, 'kargs')
        super(GuiaAplicacaoSupForm, self).__init__(*args, **kwargs)
        # remove ':' do fim dos labels
        self.label_suffix = ""

        # Add a placeholder option for the foreign key field
        self.fields['id_fazenda'].empty_label = "Selecione a fazenda"  # Custom label
        self.fields['id_fazenda'].choices = [(None, "Selecione a fazenda")] + list(Farm.objects.values_list('id_farm', 'name'))
        # self.fields['id_produto'].empty_label = "Selecione o produto"  # Custom label
        # self.fields['id_produto'].choices = [(None, "Selecione o produto")] + list(Product.objects.values_list('id','nome_comercial'))
        self.fields['id_piloto'].empty_label = "Selecione o piloto"  # Custom label
        self.fields['id_piloto'].choices = [(None, "Selecione o piloto")] + list(Pilot.objects.values_list('cpf','name'))

    class Meta:
        model = Guia_aplicacao_supervisor
        fields = ['id_fazenda', 'talhao', 'data', 'id_piloto', 'area_aplicacao', 'cultura', 'id_receita']

        labels = {
            'data': 'Data de Aplicação *',
            'id_piloto': 'Piloto *',
            'id_fazenda': 'Fazenda *',
            'cultura': 'Cultura *',
            'area_aplicacao': 'Área de Aplicação (ha) *',
            'id_receita': 'Produtos *',
        }

        widgets = {
            'data': forms.DateInput(format=('%Y-%m-%dT%H:%M'), attrs={'class': 'inputs', 'type': 'datetime-local'}),
            'id_piloto': forms.Select(attrs={'class': 'inputs', 'required': 'required'}),
            'id_fazenda': forms.Select(attrs={'class': 'inputs', 'required': 'required', 'name': 'farm_id', 'id': 'farm_id'}),
            'talhao': forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-multiple inputs', 'required': 'required', 'name': 'talhao', 'id': 'talhao'}),
            'cultura': forms.Select(attrs={'class': 'inputs', 'required': 'required'}),
            'area_aplicacao': forms.NumberInput(attrs={'class': 'inputs', 'required': 'required', 'id': 'area'}),
            'id_receita': forms.SelectMultiple(attrs={'class': 'produtos', 'required': 'required', 'id': 'produto'}),           
        }

class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        fields = ['id_produto', 'dosagem', 'taxa_aplicacao']

        labels = {
            'id_produto': 'Produto(s) *',
            'dosagem': 'Dosagem (L/ha) *',
            'taxa_aplicacao': 'Taxa de Aplicação (L) *',
        }

        widgets = {
            'id_produto': forms.SelectMultiple(attrs={'class': 'inputs', 'required': 'required'}),
            'dosagem': forms.NumberInput(attrs={'class': 'inputs', 'required': 'required'}),
            'taxa_aplicacao': forms.NumberInput(attrs={'class': 'inputs', 'required': 'required'}),
        }



class GuiaAplicacaoPilotoForm(forms.ModelForm):
    # remove ':' do fim dos labels
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = "" 

    class Meta:
        model = Guia_aplicacao_piloto
        fields = ['id_aplicacao', 'data_realizacao', 'bicos', 'direcao_vento', 'vazao', 'altura_voo', 'umidade', 'temperatura', 'rajada_vento', 'realizado', 'observacao'] 

        labels = {
            'data_realizacao': 'Data de Realização',
            'bicos': 'Bicos',
            'direcao_vento': 'Direção do Vento',
            'vazao': 'Vazão (L)',
            'altura_voo': 'Altura de Voo (m)',
            'umidade': 'Umidade (%)',
            'temperatura': 'Temperatura (C°)',
            'rajada_vento': 'Rajada de Vento (km/h)',
            'realizado': 'Realizado',
            'observacao': 'Observações',
        } 

        widgets = {
            'data_realizacao': forms.DateInput(format=('%Y-%m-%dT%H:%M'), attrs={'class': 'inputs', 'type': 'datetime-local', 'required': 'required'}),
            'bicos': forms.NumberInput(attrs={'class': 'inputs', }),
            'direcao_vento': forms.TextInput(attrs={'class': 'inputs', }),
            'vazao': forms.NumberInput(attrs={'class': 'inputs', }),
            'altura_voo': forms.NumberInput(attrs={'class': 'inputs', }),
            'umidade': forms.NumberInput(attrs={'class': 'inputs', }),
            'temperatura': forms.NumberInput(attrs={'class': 'inputs', }),
            'rajada_vento': forms.NumberInput(attrs={'class': 'inputs', }),
            'realizado': forms.CheckboxInput(attrs={'class': 'checkbox-guia', 'id': '', 'name': '', 'checked':'checked'}),
            'observacao': forms.TextInput(attrs={'class': 'inputs obs'}),
        }

class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        fields = ['id_produto', 'dosagem', 'taxa_aplicacao']

        labels = {
            'id_produto': '',
            'dosagem': 'Dosagem (L/ha) *',
            'taxa_aplicacao': 'Taxa de Aplicação (L) *',
        }

        widgets = {
            'id_produto': forms.Select(attrs={'class': 'select-edit', 'required': 'required', 'readonly': 'readonly'}),
            'dosagem': forms.NumberInput(attrs={'class': 'inputs', 'required': 'required'}),
            'taxa_aplicacao': forms.NumberInput(attrs={'class': 'inputs', 'required': 'required'}),
        }

