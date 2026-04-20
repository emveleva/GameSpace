from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db.models import Avg, Count
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView, DeleteView

from games.models import Game
from reviews.models import Review
from .forms import RegisterForm, LoginForm, EditProfileForm, DeleteProfileForm


class RegisterView(CreateView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('dashboard')

class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('welcome')

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        user_games = Game.objects.filter(created_by=user)
        user_reviews = Review.objects.filter(user=user)

        context.update({
            'games_count': user_games.count(),
            'reviews_count': user_reviews.count(),

            'recent_reviews_on_user_games': (
                Review.objects.filter(game__created_by=user)
                .exclude(user=user)
                .select_related('game', 'user')
                .order_by('-created_at')[:5]
            ),

            'top_rated_user_games': (
                user_games.annotate(avg_rating=Avg('reviews__rating'))
                .order_by('-avg_rating')[:5]
            ),

            'most_used_genres': (
                user_games.values('genres__name')
                .annotate(total=Count('genres'))
                .order_by('-total')[:5]
            ),

            'recent_user_reviews': (
                user_reviews.select_related('game')
                .order_by('-created_at')[:5]
            ),
        })

        return context

class ProfileDetailsView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/profile_details.html'

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object

        context.update({
            'favorite_games': profile.favorite_games.all(),
            'reviews': profile.reviews.order_by('-created_at')[:5],
        })

        return context

class EditProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/profile_form.html'
    form_class = EditProfileForm
    success_url = reverse_lazy('profile-details')

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'edit'
        context['cancel_url'] = reverse_lazy('profile-details')
        return context


class DeleteProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile_form.html'
    success_url = reverse_lazy("welcome")

    def get_profile(self):
        return self.request.user.profile

    def get(self, request, *args, **kwargs):
        profile = self.get_profile()

        form = DeleteProfileForm(instance=profile)

        return render(request, self.template_name, {
            "form": form,
            "action": "delete",
            "cancel_url": reverse_lazy("profile-details"),
        })

    def post(self, request, *args, **kwargs):
        user = request.user  # ALWAYS user here

        logout(request)
        user.delete()  # cascades profile automatically

        return redirect(self.success_url)