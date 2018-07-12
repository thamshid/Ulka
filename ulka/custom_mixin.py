from django.contrib.auth.mixins import AccessMixin


class AdminCheckMixin(AccessMixin):
    """
    CBV mixin which verifies that the current user is authenticated.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super(AdminCheckMixin, self).dispatch(request, *args, **kwargs)