"""
Authentication compatibility layer for Tina.

Auth is handled by GatewayAuth in app.py, which injects the actual
decorators into this module at runtime for backward compatibility
with routes that import from here.
"""

from functools import wraps

from flask import redirect, url_for, flash

# These get set at runtime by app.py via GatewayAuth
auth = None
login_required = None
admin_required = None
get_current_user = None


def manager_required(f):
    """Decorator requiring manager or admin role."""
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_current_user() if get_current_user else None
        if not user or not hasattr(user, 'is_authenticated') or not user.is_authenticated:
            return redirect(url_for('gateway_auth.login'))
        role = getattr(user, 'role', 'user')
        base_role = role.split(':')[0] if ':' in role else role
        if base_role not in ('manager', 'admin'):
            flash('You need manager access to view this page.', 'warning')
            return redirect(url_for('web.index'))
        return f(*args, **kwargs)
    return decorated
