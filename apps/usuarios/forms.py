from apps.programas.models import Programa
from apps.cursos.models import Curso
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(label="Correo electrónico", max_length=100,
        widget=forms.TextInput(attrs={
             'id': 'usernameInput',
             'placeholder': 'Correo electrónico',
             'class': 'form-control'
        }))
    password = forms.CharField(label="Contraseña", max_length=100,
        widget=forms.TextInput(attrs={
            'type': 'password',
            'id': 'passwordInput',
            'placeholder': 'Contraseña',
             'class': 'form-control'
        }))


class RegistrarUsuarioForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegistrarUsuarioForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

        self.fields['first_name'].label = "Nombres"
        self.fields['last_name'].label = "Apellidos"
        self.fields['email'].label = "Dirección de correo electrónico"
        self.fields['password1'].label = "Contraseña nueva"
        self.fields['password2'].label = "Confirmar contraseña nueva"

    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'email',)

    def clean_first_name(self):
        nombres = self.cleaned_data['first_name']
        nombres = nombres.strip().title()
        return nombres

    def clean_last_name(self):
        apellidos = self.cleaned_data['last_name']
        apellidos = apellidos.strip().title()
        return apellidos

    def clean(self):
        form_data = self.cleaned_data
        try:
            usuario_encontrado = Usuario.objects.get(email=form_data["email"])
            usuario_actual = self.instance
            if usuario_actual:
                if usuario_actual != usuario_encontrado:
                    self._errors["email"] = ["El correo electrónico del usuario ya existe"]
            else:
                self._errors["email"] = ["El correo electrónico del usuario ya existe"]
        except Usuario.DoesNotExist:
            pass

class ModificarUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'email',)

    def __init__(self, *args, **kwargs):
        super(ModificarUsuarioForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

        self.fields['first_name'].label = "Nombres"
        self.fields['last_name'].label = "Apellidos"
        self.fields['email'].label = "Dirección de correo electrónico"

    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'email',)

    def clean(self):
        form_data = self.cleaned_data
        try:
            usuario_encontrado = Usuario.objects.get(email=form_data["email"])
            usuario_actual = self.instance
            if usuario_actual:
                if usuario_actual != usuario_encontrado:
                    self._errors["email"] = ["El correo electrónico del usuario ya existe"]
            else:
                self._errors["email"] = ["El correo electrónico del usuario ya existe"]
        except Usuario.DoesNotExist:
            pass


class RestablecerContrasenaForm(forms.Form):
    password1 = forms.CharField(
        label = 'Contraseña nueva', max_length = 50,
        widget = forms.TextInput(attrs = {
        'type': 'password',
        'placeholder': 'Contraseña',
        'data-parsley-contrasena': '',
        'class': 'form-control'
    }))

    password2 = forms.CharField(label = 'Confirmar contraseña nueva', max_length = 50,
        widget = forms.TextInput(attrs = {
        'type': 'password',
        'placeholder': 'Confirmar contraseña',
        'data-parsley-confirmacion': 'id_password1',
        'class': 'form-control'
    }))

    def clean(self):
        form_data = self.cleaned_data
        if form_data["password1"] != form_data["password2"]:
            self._errors["password2"] = ["Las contraseñas no coinciden"]
        return form_data


class CargueMasivoEstudiantesForm(forms.Form):
    archivo = forms.FileField(label="Archivo de estudiantes")

class CargueMasivoPersonalForm(forms.Form):
    archivo = forms.FileField(label="Archivo de usuarios")


class CursosFiltroForm(forms.Form):
    NIVELES_ACADEMICOS = (
        ('Pregrado', "Pregrado"),
        ('Maestría', "Maestría"),
        ('Doctorado', "Doctorado"),
    )
    nivel_academico = forms.ChoiceField(choices=NIVELES_ACADEMICOS, label='Nivel académico')
    cursos = forms.ModelChoiceField(queryset=Curso.objects.none(), required=True)
    
    def __init__(self, *args, **kwargs):
        nivel_academico = kwargs.pop('nivel_academico', None)
        curso = kwargs.pop('curso', None)
        super(CursosFiltroForm, self).__init__(*args, **kwargs)
        if curso:
            self.fields['cursos'].initial = Curso.objects.get(id=curso)
        programas = Programa.objects.filter(nivel_academico=nivel_academico)
        self.fields['cursos'].queryset= Curso.objects.filter(programas__in=programas).distinct()
        self.fields['nivel_academico'].initial = nivel_academico
     
class CursosTransferenciaForm(forms.Form):
    curso_a_transferir = forms.ModelChoiceField(queryset=Curso.objects.all(), required=False)
   
    def __init__(self, *args, **kwargs):
        nivel_academico = kwargs.pop('nivel_academico', None)
        curso = kwargs.pop('curso', None)
        super(CursosTransferenciaForm, self).__init__(*args, **kwargs)

        codigos_tg_I = Curso.obtener_cursos_de_tg_I()
        codigos_tg_II = Curso.obtener_cursos_de_tg_II()
        codigos_posgrado = Curso.obtener_cursos_de_proyecto_posgrado()
        codigos_continuacion = Curso.obtener_cursos_de_continuacion()
        codigos_anteproyecto_pregrado = Curso.obtener_cursos_de_anteproyecto_pregrado()
        codigos_anteproyecto_posgrado = Curso.obtener_cursos_de_anteproyecto_posgrado()   

        if curso:
            programas = Programa.objects.filter(cursos_del_programa__curso=curso)
            curso = Curso.objects.get(id=curso)
            cursos = Curso.objects.filter(programas__in=programas)
            if nivel_academico == 'Pregrado':
                if curso in codigos_anteproyecto_pregrado:
                    self.fields['curso_a_transferir'].queryset =  cursos.filter(
                        id__in=codigos_tg_I.values('id')
                    ).distinct()
                elif curso in codigos_tg_I:
                    self.fields['curso_a_transferir'].queryset =  cursos.filter(
                        id__in=codigos_tg_II.values('id')
                    ).distinct()
                else:
                    self.fields['curso_a_transferir'].queryset =  cursos.filter(
                        id__in=codigos_continuacion.values('id')
                    ).distinct()
            if nivel_academico == 'Maestría' or nivel_academico == 'Doctorado':
                if curso in codigos_anteproyecto_posgrado:
                    self.fields['curso_a_transferir'].queryset =  cursos.filter(
                        id__in=codigos_posgrado.values('id')
                    ).distinct()
                else:
                    self.fields['curso_a_transferir'].queryset =  cursos.filter(
                        id__in=codigos_posgrado.values('id')
                    ).distinct()

    def clean(self):
        cleaned_data = super().clean()
        curso_a_transferir = cleaned_data.get('curso_a_transferir', None)
        if curso_a_transferir == None:
            self.add_error('curso_a_transferir', "Falta escoger el curso a tranferir")


class CursosTransferenciaReprobadosForm(forms.Form):
    curso_a_transferir = forms.ModelChoiceField(queryset=Curso.objects.all(), required=False)
   
    def __init__(self, *args, **kwargs):
        nivel_academico = kwargs.pop('nivel_academico', None)
        curso = kwargs.pop('curso', None)
        super(CursosTransferenciaReprobadosForm, self).__init__(*args, **kwargs)

        codigos_anteproyecto_pregrado = Curso.obtener_cursos_de_anteproyecto_pregrado()
        codigos_anteproyecto_posgrado = Curso.obtener_cursos_de_anteproyecto_posgrado()

        if curso:
            programas = Programa.objects.filter(cursos_del_programa__curso=curso)
            curso = Curso.objects.get(id=curso)
            cursos = Curso.objects.filter(programas__in=programas)
            if nivel_academico == 'Pregrado':
                self.fields['curso_a_transferir'].queryset =  cursos.filter(
                    id__in=codigos_anteproyecto_pregrado.values('id')
                ).distinct()
            if nivel_academico == 'Maestría' or nivel_academico == 'Doctorado':
                self.fields['curso_a_transferir'].queryset =  cursos.filter(
                    id__in=codigos_anteproyecto_posgrado.values('id')
                ).distinct()

    def clean(self):
        cleaned_data = super().clean()
        curso_a_transferir = cleaned_data.get('curso_a_transferir', None)
        if curso_a_transferir == None:
            self.add_error('curso_a_transferir', "Falta escoger el curso a tranferir")

class EstudiantesCambioMatriculaForm(forms.ModelForm):
    cambio_siguiente_periodo = forms.BooleanField(label="", required=False)
    class Meta:
        model = Usuario
        fields = ("cambio_siguiente_periodo",)
 

class PeriodosFiltroEstudianteForm(forms.Form):

    periodos_academicos = forms.ModelChoiceField(queryset=PeriodoAcademico.objects.all(), label="Periodos académicos")

    def __init__(self, *args, **kwargs):
        periodo_academico = kwargs.pop('periodo_academico', None)
        super(PeriodosFiltroEstudianteForm, self).__init__(*args, **kwargs)

        self.fields['periodos_academicos'].initial = periodo_academico


class ActualizarFechaGradoForm(forms.ModelForm):
    class Meta:
        model = FechaDeGrado
        fields = ('ano', 'mes')

    
    def __init__(self, *args, **kwargs):
        super(ActualizarFechaGradoForm, self).__init__(*args, **kwargs)
        self.fields['ano'].help_text = '<span class="f-s-11 label-blue">Campo opcional:</span> Escriba el año en el que se graduó el estudiante.'
        self.fields['mes'].help_text = '<span class="f-s-11 label-blue">Campo opcional:</span> Escriba el mes en el que se graduó el estudiante.'

    def clean(self):
        form_data = self.cleaned_data
        mes = form_data['mes']
        if mes > 12 or mes < 1:
            self.add_error('mes', "Especifique un mes dentro del rango [1 - 12]")


