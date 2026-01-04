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
    # Return empty response for favicon requests
    from django.http import HttpResponse
    return HttpResponse(status=204)

urlpatterns = [
    path('', api_root, name='api-root'),
    path('favicon.ico', favicon, name='favicon'),
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
]
