from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from snippets import views
from snippets.views import RegistrationAPI, LoginAPI

register = RegistrationAPI.as_view({
    'get': 'retrieve',
    'post': 'register',
})

authenticate = LoginAPI.as_view({
    #'get': 'retrieve',
    'post': 'authenticate_user'
})

urlpatterns = [
    path('snippets/', views.snippet_list),
    path('snippets/<int:pk>', views.snippet_detail),
    path('register/', register, name="register"),
    path('auth/', authenticate, name="authenticate_user")
]

urlpatterns = format_suffix_patterns(urlpatterns)