from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    # path('check_booking/' , check_booking),
    path('', home , name='home'),
    path('hotel-detail/<uid>/' , hotel_detail , name="hotel_detail"),
    path('login/', login_page , name='login_page'),
    path('logout/', user_logout , name='user_logout'),
    path('register/', register_page , name='register_page'),
    path('profile/', profile_page , name='profile_page'),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()