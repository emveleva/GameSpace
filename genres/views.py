from collections import defaultdict

from django.db.models.functions import Lower
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from genres.forms import AddGenreForm, EditGenreForm, DeleteGenreForm
from genres.models import Genre

class GenresListView(TemplateView):
    template_name = 'genres/genres_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        genres = Genre.objects.annotate(
            lower_name=Lower('name')
        ).order_by('lower_name')

        grouped_genres = defaultdict(list)

        for genre in genres:
            first_letter = genre.name[0].upper()
            grouped_genres[first_letter].append(genre)

        context['grouped_genres'] = dict(sorted(grouped_genres.items()))
        context['page_title'] = 'All Genres'

        return context


class AddGenreView(CreateView):
    model = Genre
    form_class = AddGenreForm
    template_name = 'genres/genre_form.html'
    success_url = reverse_lazy('genres_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'add'
        context['cancel_url'] = reverse_lazy('genres_list')
        return context


class EditGenreView(UpdateView):
    model = Genre
    form_class = EditGenreForm
    template_name = 'genres/genre_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'edit'
        context['cancel_url'] = self.object.get_absolute_url()
        return context

    def get_success_url(self):
        return self.object.get_absolute_url()


class DeleteGenreView(DeleteView):
    model = Genre
    template_name = 'genres/genre_form.html'
    success_url = reverse_lazy('genres_list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_form(self, form_class=None):
        form = DeleteGenreForm(instance=self.object)

        for field in form.fields.values():
            field.disabled = True

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['action'] = 'delete'
        context['cancel_url'] = reverse_lazy('genres_list')
        return context