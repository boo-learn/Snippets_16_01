from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_page, name='home'),
    path('snippets/add/', views.add_snippet_page, name='snippets-add'),
    path('snippet/delete/<int:snippet_id>', views.snippet_delete, name='snippet-delete'),
    path('snippet/edit/<int:snippet_id>', views.snippet_edit, name='snippet-edit'),
    path('snippets/list/', views.snippets_page, name='snippets-list'),
    path('snippets/my/', views.snippets_my, name='snippets-my'),
    path('snippet/detail/<int:snippet_id>', views.snippet_detail, name='snippet-detail'),
    path('comment/add', views.comment_add, name="comment_add"),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('registration', views.registration, name='registration'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
