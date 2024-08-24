from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
import requests
from django.views.generic import TemplateView, ListView, FormView, CreateView, DeleteView
from urllib.parse import quote

from django.conf import settings
from .models import Profile, Bookmark
from .forms import CommentForm
from .models import API, Comment


def index(request):
    return render(request, 'movies/index.html')


class SearchMovie(ListView):
    template_name = 'movies/find_movie.html'
    http_method_names = ['post', 'get']
    context_object_name = 'response'
    paginate_by = 6

    def get_queryset(self):
        search_query = self.request.GET.get('search')
        if search_query:
            try:
                headers = {
                    'X-API-KEY': settings.API_KEY,
                    'accept': 'application/json'}
                url_with_params = quote(search_query)
                url = f'{settings.REQUEST_URL}{url_with_params}'
                response = requests.get(url, headers=headers)
                return response.json()['docs']
            except (TypeError, KeyError):
                return redirect('index')
        return []


class DetailMovie(TemplateView, FormView):
    template_name = 'movies/movie_detail.html'
    http_method_names = ['post', 'get']
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == "GET":
            movie_id = self.request.GET.get('detail')
            url = f'{settings.REQUEST_URL_DETAIL}{movie_id}'
            headers = {
                'X-API-KEY': settings.API_KEY,
                'accept': 'application/json'}
            response = requests.get(url, headers=headers).json()
            context['detail_response'] = response
            api = API.objects.get_or_create(name=response['name'], url=url)
            context['comments'] = Comment.objects.filter(movie=api[0]).select_related('movie')
            if self.request.user.is_authenticated:
                profile = Profile.objects.get(user=self.request.user)
                bookmark = Bookmark.objects.filter(movie=api[0], user=profile).select_related('user')
                if bookmark:
                    context['bookmark'] = bookmark
        return context

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        form = Comment.objects.create(author=profile,
                                      body=form.cleaned_data['body'],
                                      movie=API.objects.get(name__contains=self.request.GET.get('detail')))
        return super().form_valid(form)


class AddBookmark(CreateView):
    model = API

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user)
        movie = API.objects.get(name=self.request.GET.get('title'))
        bookmark = Bookmark.objects.get_or_create(user=profile, movie=movie)
        if bookmark:
            return redirect(request.META.get('HTTP_REFERER'))


class RemoveBookmark(DeleteView):
    model = API

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user)
        movie = API.objects.get(name=self.request.GET.get('title'))
        bookmark = Bookmark.objects.get(user=profile, movie=movie)
        bookmark.delete()
        return redirect(request.META.get('HTTP_REFERER'))

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)


class BookmarksView(LoginRequiredMixin, ListView):
    model = Bookmark
    template_name = 'movies/bookmarks.html'
    context_object_name = 'bookmarks'
    login_url = '/account/login'
    paginate_by = 8

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        return super().get_queryset().filter(user=profile)
