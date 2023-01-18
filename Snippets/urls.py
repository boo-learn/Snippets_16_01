from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page, name='home'),
    path('snippets/add/', views.add_snippet_page, name='snippets-add'),
    path('snippets/list/', views.snippets_page, name='snippets-list'),
    path('snippet/detail/<int:snippet_id>', views.snippet_detail, name='snippet-detail'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
