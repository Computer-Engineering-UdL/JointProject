from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.contrib.auth import get_user_model

UserModel = get_user_model()


def worker_required(worker_type=None):
    """Allows only the worker specified to access the view. Admins can access all views."""
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            if worker_type is None:
                if hasattr(request.user, 'worker'):
                    return view_func(request, *args, **kwargs)
            else:
                if hasattr(request.user, 'worker') and request.user.worker.type == worker_type:
                    return view_func(request, *args, **kwargs)
            return HttpResponseForbidden()

        return _wrapped_view

    return decorator


def admin_required(view_func):
    """Allows only the admin to access the view."""
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        return view_func(request, *args, **kwargs)

    return _wrapped_view
