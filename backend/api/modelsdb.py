from django.db import models
from django.contrib.auth.models import User

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Pilot(models.Model):
    name = models.CharField(max_length=80)
    cpf = models.CharField(primary_key=True, max_length=14)
    birth_date = models.DateField()
    address = models.TextField()
    city = models.TextField()
    state = models.TextField()
    phone_number = models.CharField(max_length=15)
    hiring_date = models.DateField()
    active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'pilot'

    def __str__(self):
        return f"{self.name}" 
       

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    role = models.CharField(max_length=10)
    cpf = models.CharField(max_length=14, null=True, blank=True)


# Signals to auto-create or update the Profile when the User model is saved
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Usuario(models.Model):
    username = models.CharField(primary_key=True, max_length=60)
    passwd = models.CharField(max_length=60)
    role = models.CharField(max_length=40)
    cpf = models.CharField(max_length=14, null=True, blank=True)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return f"{self.username}" 

class Farm(models.Model):
    id_farm = models.CharField(primary_key=True, max_length=60)
    name = models.TextField(max_length=80)
    owner = models.TextField()
    city = models.TextField()
    state = models.TextField()

    class Meta:
        db_table = 'farm'


class Talhao(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.PROTECT, related_name='children')
    id_talhao = models.BigIntegerField(primary_key=True)
    area = models.FloatField()
    technician = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'talhao'


class Product(models.Model):
    CHOICES = [
            ('', 'Escolha o Grupo do Produto'),
            ('Acaricida', 'Acaricida'),
            ('Agente biológico de controle', 'Agente biológico de controle'),
            ('Ativador de planta', 'Ativador de planta'),
            ('Bactericida', 'Bactericida'),
            ('Cupinicida', 'Cupinicida'),
            ('Feromônio', 'Feromônio'),
            ('Fertilizante', 'Fertilizante'),
            ('Formicida', 'Formicida'),
            ('Fungicida', 'Fungicida'),
            ('Herbicida', 'Herbicida'),
            ('Inseticida', 'Inseticida'),
            ('Nematicida', 'Nematicida'),
            ('Regulador de crescimento', 'Regulador de crescimento'),
        ]

    id = models.BigIntegerField(primary_key=True)
    nome_comercial = models.TextField()
    grupo_produto = models.CharField(
        max_length=50,
        choices=CHOICES,
    )
    principio_ativo = models.TextField()
    dosagem_recomendada = models.TextField()
    observacao = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'product'

    def __str__(self):
        return f"{self.nome_comercial}" 

class Aeronave(models.Model):
    CHOICES = [
        ('', 'Escolha o fabricante'),
        ('DJI', 'DJI'),
    ]

    id = models.CharField(primary_key=True, max_length=50)
    model = models.TextField()
    manufacturer = models.CharField(
        choices=CHOICES,
        max_length=50
    )
    capacity = models.FloatField()

    class Meta:
        db_table = 'aeronave'


class Receita(models.Model):
    id_receita = models.AutoField(primary_key=True)
    id_produto = models.ForeignKey(Product, on_delete=models.PROTECT)
    id_guia_sup = models.ForeignKey('Guia_aplicacao_supervisor', on_delete=models.PROTECT)
    dosagem = models.FloatField()
    taxa_aplicacao = models.FloatField()
    
    class Meta:
        db_table = 'receita'


class Guia_aplicacao_supervisor(models.Model):
    CHOICES = [
        ('', 'Selecione a cultura'),
        ('Algodão', 'Algodão'),
        ('Cana-de-açucar', 'Cana-de-açucar'),
        ('Milho', 'Milho'),
        ('Pasto', 'Pasto'),
        ('Soja', 'Soja'),
    ]

    cod_aplicacao = models.AutoField(primary_key=True)
    data = models.DateTimeField()
    id_fazenda = models.ForeignKey(Farm, on_delete=models.PROTECT)
    talhao = models.TextField(default='')
    cultura = models.CharField(
        max_length=50,
        choices=CHOICES,
    )
    area_aplicacao = models.FloatField()
    id_receita = models.ManyToManyField(Product, through='Receita')
    id_responsavel_global = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='id_responsavel_global', blank=True, null=True)
    realizado = models.BooleanField(default=False)
    id_piloto = models.ForeignKey(Pilot, on_delete=models.PROTECT, default='')

    # Store selected children as a comma-separated string
    def set_talhao(self, child_ids):
        self.talhao = child_ids
        print(self.talhao)

    # Retrieve the children IDs as a list from the comma-separated string
    def get_talhao(self):
        return self.talhao.split(',')

    class Meta:
        db_table = 'guia_aplicacao_supervisor'


class Guia_aplicacao_piloto(models.Model):
    id_aplicacao = models.OneToOneField(Guia_aplicacao_supervisor, on_delete=models.PROTECT, default='', primary_key=True)
    data_realizacao = models.DateTimeField(blank=True, null=True)
    # aeronave = models.ForeignKey(Aeronave, null=True, on_delete=models.SET_NULL)
    bicos = models.IntegerField(blank=True, null=True)
    direcao_vento = models.CharField(max_length=50, blank=True, null=True)
    vazao = models.FloatField(blank=True, null=True)
    altura_voo = models.FloatField(blank=True, null=True)
    umidade = models.FloatField(blank=True, null=True)
    temperatura = models.FloatField(blank=True, null=True)
    rajada_vento = models.FloatField(blank=True, null=True)
    realizado = models.BooleanField(default=False, blank=True, null=True)
    observacao = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        db_table = 'guia_aplicacao_piloto'


class Foto_panoramica(models.Model):
    id_foto = models.AutoField(primary_key=True)
    id_aplicacao = models.ForeignKey(Guia_aplicacao_piloto, on_delete=models.PROTECT)
    foto = models.BinaryField(editable=True)
    class Meta:
        db_table = 'foto_panoramica'

class Foto_trajeto(models.Model):
    id_foto = models.AutoField(primary_key=True)
    id_aplicacao = models.ForeignKey(Guia_aplicacao_piloto, on_delete=models.PROTECT)
    foto = models.BinaryField(editable=True)
    class Meta:
        db_table = 'foto_trajeto'

class Foto_cond_atmosferica(models.Model):
    id_foto = models.AutoField(primary_key=True)
    id_aplicacao = models.ForeignKey(Guia_aplicacao_piloto, on_delete=models.PROTECT)
    foto = models.BinaryField(editable=True, null=True, blank=True)
    class Meta:
        db_table = 'foto_cond_atmosferica'

class Foto_produto(models.Model):
    id_foto = models.AutoField(primary_key=True)
    id_aplicacao = models.ForeignKey(Guia_aplicacao_piloto, on_delete=models.PROTECT)
    foto = models.BinaryField(editable=True)
    class Meta:
        db_table = 'foto_produto'




