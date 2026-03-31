from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, TemplateView

from platforms.forms import EditPlatformForm, DeletePlatformForm, AddPlatformForm
from platforms.models import Platform

class PlatformsListView(TemplateView):
    template_name = 'platforms/platforms_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['platforms'] = Platform.objects.all().order_by('name')
        context['page_title'] = 'All Platforms'

        return context

class AddPlatformView(CreateView):
    model = Platform
    form_class = AddPlatformForm
    template_name = 'platforms/platform_form.html'
    success_url = reverse_lazy('platforms_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'add'
        context['cancel_url'] = reverse_lazy('platforms_list')
        return context

class EditPlatformView(UpdateView):
    model = Platform
    form_class = EditPlatformForm
    template_name = 'platforms/platform_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'edit'
        context['cancel_url'] = self.object.get_absolute_url()
        return context

    def get_success_url(self):
        return self.object.get_absolute_url()


class DeletePlatformView(DeleteView):
    model = Platform
    template_name = 'platforms/platform_form.html'
    success_url = reverse_lazy('platforms_list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_form(self, form_class=None):
        form = DeletePlatformForm(instance=self.object)

        for field in form.fields.values():
            field.disabled = True

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['action'] = 'delete'
        context['cancel_url'] = reverse_lazy('platforms_list')
        return context