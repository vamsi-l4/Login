"""
URL configuration for login_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def api_root(request):
    return JsonResponse({
        'message': 'Login API',
        'version': '1.0',
        'endpoints': [
            '/api/accounts/signup/',
            '/api/accounts/login/',
            '/api/accounts/verify-email/',
            '/admin/'
        ]
    })

def favicon(request):
    # Return a simple transparent favicon
    from django.http import HttpResponse
    # 1x1 transparent GIF
    favicon_data = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x21\xF9\x04\x01\x00\x00\x00\x00\x2C\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3B'
    return HttpResponse(favicon_data, content_type='image/gif')

urlpatterns = [
    path('', api_root, name='api-root'),
    path('favicon.ico', favicon, name='favicon'),
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
]
