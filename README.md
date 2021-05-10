# Django Users Manager

> Creado el 01-05-2021


Extendiendo la clase Usuarios con AbstractUser e implementando sistema personalizado de Login, Register y Logout usando un formulario que valide campos personalizados.


## Instalación
```shell

python -m venv venv

```

```shell

venv\scripts\activate

```

```shell

pip install -r requirements.txt

```

```shell

cd mysite

```

```shell

py manage.py runserver

```

```shell

Enjoyy!!

```


## Funcionalidades
- Modelo User Custom con AbstractUser
- Login (con username y email)
- Registro (con username y email)
- Perfil del usuario
- Logout
- Respuesta al introducir en la url usuario que no existe
- Modificar email
- Modificar contraseña
- Modificar otros campos
- Urls propias para el usuario con `include()`
- Eliminar cuenta (desactivar - is_active == False)
- Prohibir el acceso a ciertas vistas tras su uso
- Uso de Captchas y antispam
- Confirmar cuenta mediante un token por email tras registrarse (con temporizador)


## Cómo integrarlo a mi proyecto
1. Dentro del directorio `apps/` copia la aplicación users y pégalo dentro de tu proyecto.
2. Registra la aplicación dentro de `settings.py` y añade lo siguiente:

    ```py
        AUTH_USER_MODEL = 'users.User'
        AUTHENTICATION_BACKENDS = ['apps.users.backends.UsernameEmailBackend']

        # Esto para el modo de desarrollo (eliminar en producción)
        EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

        # Expiración del token
        EMAIL_VERIFY_TIMEOUT = 60 # In seconds
    ```

3. Dentro del directorio `templates/` añade el subdirectorio `auth/ - register/ - signup/`
4. Listo


## Librerías necesarias
#### Pillow
> https://pypi.org/project/Pillow/

### Django Simple Captcha
> https://pypi.org/project/django-simple-captcha/

## Google reCaptcha
Perfectamente se puede incluir

> https://www.google.com/recaptcha/admin/create

> https://developers.google.com/recaptcha/docs/v3