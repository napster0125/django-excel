"""playExcel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    url(r'^api/dsjchsj87673yf787df6u2hc87wr/', admin.site.urls),
    url(r'^api/kryptos', include('kryptos.urls')),
    url(r'^api/echo', include('echo.urls')),
    url(r'^api/hashinclude',include('hashinclude.urls')),
    url(r'^api/dalalbull/', include('dalalbull.urls')),
    url(r'^api/', include('common.urls')),
    
]   

if settings.DEBUG:
    urlpatterns +=   static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
