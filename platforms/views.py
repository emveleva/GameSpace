from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from platforms.forms import EditPlatformForm, DeletePlatformForm, AddPlatformForm
from platforms.models import Platform


def platforms_list(request: HttpRequest):
    list_platforms = Platform.objects.all().order_by('name')

    context = {
        'platforms': list_platforms,
        'page_title': 'All Platforms'
    }

    return render(request, 'platforms/platforms_list.html', context)

def add_platform(request: HttpRequest):
    form = AddPlatformForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        platform = form.save()
        return redirect('platforms_list')

    return render(request, 'platforms/platform_form.html', {
        'form': form,
        'action': 'add',
        'cancel_url': reverse('platforms_list'),
    })

def edit_platform(request: HttpRequest, slug: str):
    platform = get_object_or_404(Platform, slug=slug)

    form = EditPlatformForm(request.POST or None, instance=platform)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('platforms_list')

    return render(request, 'platforms/platform_form.html', {
        'form': form,
        'action': 'edit',
        'cancel_url': platform.get_absolute_url(),
    })

def delete_platform(request: HttpRequest, slug: str):
    platform = get_object_or_404(Platform, slug=slug)

    form = DeletePlatformForm(request.POST or None, instance=platform)

    for field in form.fields.values():
        field.disabled = True

    if request.method == 'POST':
        platform.delete()
        return redirect('platforms_list')

    return render(request, 'platforms/platform_form.html', {
        'form': form,
        'action': 'delete',
        'cancel_url': reverse('platforms_list'),
    })