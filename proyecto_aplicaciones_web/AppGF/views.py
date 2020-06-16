from django.shortcuts import render
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from django.views.generic import CreateView,UpdateView,DeleteView
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.generic import ListView
from AppGF.models import *
from django.contrib.auth.views import LogoutView 
from django.forms import formset_factory

from AppGF.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404,HttpResponseRedirect,HttpResponse



def home(request):
    return render(request, 'AppGF/home.html')
 
    
class UsuarioList(ListView):
	model = Usuario
	fields = '__all__'
	template_name = "AppGF/usuarios_list.html"
	
class UsuarioDelete(DeleteView):
    model = Usuario
    fields = '__all__'
    template_name="AppGF/usuarios_delete.html"
    success_url = reverse_lazy('usuarios_list')
    
    def test_func(self):
        return self.request.user.is_staff == True

class UsuarioUpdate(LoginRequiredMixin,UpdateView):
    model = Usuario
    fields = '__all__'
    template_name="AppGF/usuarios_update.html"
    success_url = reverse_lazy('usuarios_list')          

class UsuarioDetail(LoginRequiredMixin,DetailView):

    model = Usuario
    template_name="AppGF/usuario_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)     
        return context
        
class PescadoCreate(LoginRequiredMixin,CreateView):
    model = Pescado
    
    fields = '__all__'
    template_name="AppGF/pescados_create.html"
    success_url = reverse_lazy('pescados_list')
       
           
class PescadoList(ListView):
    model = Pescado
    template_name="AppGF/pescados_list.html"
    
    def get_context_data(self, **kwargs):
        context = super(PescadoList,self).get_context_data(**kwargs)     
        return context
    
    
class PescadoDetail(LoginRequiredMixin,DetailView):

    model = Pescado
    template_name="AppGF/pescados_detail.html"
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)     
        return context    
    
class ZonaPescaCreate(LoginRequiredMixin,CreateView):
    model = ZonaPesca
    fields = '__all__'
    template_name="AppGF/zonapescas_create.html"
    success_url = reverse_lazy('zonapescas_list')

        
class ZonaPescaList(LoginRequiredMixin,ListView):
    model = ZonaPesca
    template_name="AppGF/zonapescas_list.html"

class SeñueloList(LoginRequiredMixin,ListView):
    model = Señuelo
    template_name="AppGF/señuelos_list.html"
    
class CapturaList(ListView):
	model = Captura
	fields = '__all__'
	login_url = '/accounts/login/'
	template_name = 'AppGF/capturas_list.html'
	
	def get_context_data(self, **kwargs):
		context = super(CapturaList,self).get_context_data(**kwargs)
		return context
		
class CapturaListUsu(LoginRequiredMixin,ListView):
	model = Captura
	fields = '__all__'
	login_url = '/accounts/login/'
	template_name = 'AppGF/capturas_list_usu.html'
	
	def get_context_data(self, **kwargs):
		context = super(CapturaListUsu,self).get_context_data(**kwargs)
		return context		
		
class CapturaCreate(LoginRequiredMixin,CreateView):
    model = Captura
    template_name="AppGF/captura_create.html"
    success_url = reverse_lazy('capturas_list')
    
class CapturaDetail(LoginRequiredMixin,DetailView):

    model = Captura
    template_name="AppGF/captura_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)     
        return context          

class CapturaUpdate(LoginRequiredMixin,UpdateView):
    model = Captura
    fields = 'pescado','fecha_captura', 'zona', 'marea','señuelo','cantpes', 'foto_captura',
    template_name="AppGF/capturas_update.html"
    success_url = reverse_lazy('capturas_list')
    
class CapturaDelete(LoginRequiredMixin,DeleteView):
    model = Captura
    fields = '__all__'
    template_name="AppGF/capturas_delete.html"
    success_url = reverse_lazy('capturas_list')
    
def contact(request):
	titulo = "Contactanos"
	form = ContactForm(request.POST or None)
	if form.is_valid():
		form_email = form.cleaned_data.get("email")
		form_mensaje = form.cleaned_data.get("mensaje")
		form_nombre = form.cleaned_data.get("nombre")
		asunto = "Form de Contacto"
		email_from = settings.EMAIL_HOST_USER
		email_to = [email_from]
		email_mensaje = "%s: %s enviado por %s" %(form_nombre, form_mensaje, form_email )
		send_mail(asunto,
			email_mensaje,
			email_from,
			email_to,
			fail_silently=False
			)
		return redirect('home')	
		#print email, mensaje, nombre
	context = {
		"form": form,
		"titulo": titulo,
	}
	return render (request, "sugerencias.html", context)
	
def crearCaptura(request):
    if request.method == 'POST':
        form1 = CrearCapturaForm(request.POST, request.FILES)
        if form1.is_valid():
            capturas = Captura()
            usuario = Usuario.objects.get(user=request.user)
            capturas.usuario = usuario
            capturas.fecha_captura = form1.cleaned_data.get('fecha_captura')
            capturas.pescado = form1.cleaned_data.get('pescado')
            capturas.cantpes = form1.cleaned_data.get('cantidad')
            capturas.caña = form1.cleaned_data.get('caña')
            capturas.carrete = form1.cleaned_data.get('carrete')
            capturas.señuelo = form1.cleaned_data.get('señuelo')
            capturas.foto_captura = form1.cleaned_data.get('foto_captura')
            capturas.zona = form1.cleaned_data.get('zona')
            capturas.marea = form1.cleaned_data.get('marea')

            capturas.save()
            return HttpResponseRedirect('../../captura')
    else:
        form1 = CrearCapturaForm()
    return render(request,'AppGF/capturas.html',{'capturas':form1})  	
    
def registro(request):
    if request.method == 'POST':
        form = Registro(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal            
            user.usuario.provincia = form.cleaned_data.get('provincia')
            user.usuario.localidad = form.cleaned_data.get('localidad')
            user.usuario.experiencia_como_pescador = form.cleaned_data.get('experiencia')
            user.usuario.foto_usuario = form.cleaned_data.get('foto_de_perfil')
            user.email= form.cleaned_data.get('email')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('inicio')
	
    else:
        form = Registro()
        
    return render(request, 'registro.html', {'form': form})            	
 
