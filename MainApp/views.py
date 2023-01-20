from django.http import Http404
from django.shortcuts import render, redirect
from django.db.models import Q
from MainApp.models import Snippet
from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm
from django.contrib import auth
from django.contrib.auth.models import User
from django.db.models import Count


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


# /snippets/list
# /snippets/list/?lang=python
# /snippets/list/?user_id=2
def snippets_page(request):
    # TODO: реализовать "сброс фильтра"
    # TODO: реализовать направление сортировку по алфавиту
    print(f"user_id = {request.GET.get('user_id')}")
    context = {
        'pagename': 'Просмотр сниппетов'
    }
    # print(f"sort-data={request.GET.get('sort')}")
    if not request.user.is_authenticated:
        snippets = Snippet.objects.filter(private=False)
    else:
        snippets = Snippet.objects.filter(Q(private=False) | Q(user=request.user))
    if request.GET.get("lang"):
        snippets = snippets.filter(lang=request.GET['lang'])
        context['lang'] = request.GET['lang']

    if request.GET.get("user_id"):
        snippets = snippets.filter(user__id=request.GET['user_id'])

    if request.GET.get("sort"):
        snippets = snippets.order_by(request.GET.get("sort"))

    context['snippets'] = snippets
    users = User.objects.all().annotate(num_snippets=Count('snippet')).filter(num_snippets__gte=1)
    context['users'] = users
    return render(request, 'pages/view_snippets.html', context)


def snippet_detail(request, snippet_id):
    snippet = Snippet.objects.get(pk=snippet_id)
    comment_form = CommentForm()
    context = {
        'pagename': 'Информация о сниппете',
        'snippet': snippet,
        'comment_form': comment_form
    }
    return render(request, 'pages/snippet_detail.html', context)


def add_snippet_page(request):
    if request.method == "GET":  # вернуть страницу с формой
        form = SnippetForm()
        context = {
            'pagename': 'Добавление нового сниппета',
            'form': form
        }
        return render(request, 'pages/add_snippet.html', context)
    elif request.method == "POST":  # получаем данные формы
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.user = request.user
            snippet.save()
            return redirect("snippets-list")


def snippet_delete(request, snippet_id):
    snippet = Snippet.objects.get(pk=snippet_id)
    snippet.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))


def snippet_edit(request, snippet_id):
    pass


def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            context = {
                "errors": ["Логин или пароль некорректны"]
            }
            return render(request, 'pages/index.html', context)
    return redirect(request.META.get('HTTP_REFERER', '/'))


def logout(request):
    auth.logout(request)
    return redirect('home')


def registration(request):
    if request.method == "GET":
        form = UserRegistrationForm()
        context = {
            'form': form
        }
        return render(request, 'pages/registration.html', context)
    elif request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            context = {
                'form': form
            }
            return render(request, 'pages/registration.html', context)


def snippets_my(request):
    my_snippets = Snippet.objects.filter(user=request.user)
    context = {
        'pagename': 'Мои сниппетов',
        'snippets': my_snippets
    }
    return render(request, 'pages/view_snippets.html', context)


def comment_add(request):
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            snippet_id = request.POST.get("snippet_id")
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.snippet = Snippet.objects.get(pk=snippet_id)
            comment.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))
