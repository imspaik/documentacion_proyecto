from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from AppGF.models import *

# Register your models here.

from .models import Usuario,Pescado,Señuelo,ZonaPesca,MaterialSeñuelo,Captura,Marea

class UsuarioInline(admin.StackedInline):
    model = Usuario
    can_delete = False
    
class UserAdmin(BaseUserAdmin):
    inlines = (UsuarioInline,)    	

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Pescado)
admin.site.register(Señuelo)
admin.site.register(ZonaPesca) 
admin.site.register(MaterialSeñuelo)  
admin.site.register(Captura) 
admin.site.register(Marea)
