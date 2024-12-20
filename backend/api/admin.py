from django.contrib import admin
from .modelsdb import Usuario, Pilot, Talhao, Farm, Product, Aeronave, Guia_aplicacao_supervisor, Guia_aplicacao_piloto, Profile, Foto_trajeto, Foto_produto, Foto_cond_atmosferica, Foto_panoramica, Receita
# Register your models here.
admin.site.register(Usuario)

admin.site.register(Pilot)

admin.site.register(Talhao)

admin.site.register(Farm)

admin.site.register(Product)

admin.site.register(Aeronave)

admin.site.register(Guia_aplicacao_supervisor)

admin.site.register(Guia_aplicacao_piloto)

admin.site.register(Profile)

admin.site.register(Foto_trajeto)

admin.site.register(Foto_produto)

admin.site.register(Foto_cond_atmosferica)

admin.site.register(Foto_panoramica)

admin.site.register(Receita)