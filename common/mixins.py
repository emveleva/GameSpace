from django.contrib.auth.mixins import UserPassesTestMixin


class DisableFieldsMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.disabled = True


class ReviewPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        review = self.get_object()

        user = self.request.user

        return (
            user == review.user
            or user.is_staff
            or user.groups.filter(name='Moderators').exists()
        )