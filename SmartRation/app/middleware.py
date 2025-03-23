from django.shortcuts import redirect

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    
    def __call__(self, request):
        allowed_paths = ["/login/", "/register/", "/static/"] 

        if not request.session.get("user_id") and request.path not in allowed_paths:
            return redirect("login")  

        return self.get_response(request)



"""
def __call__(self, request):
        allowed_paths = ["/login/", "/register/", "/static/"]  # Paths that don't require authentication
        admin_only_paths = ["/admin-dashboard/", "/admin-settings/"]  # Restrict these pages

        user_role = request.session.get("role")  # Get user role from session

        if not request.session.get("user_id") and request.path not in allowed_paths:
            return redirect("login")  # Redirect unauthorized users to login

        # Prevent staff from accessing admin pages
        if user_role == "staff" and request.path in admin_only_paths:
            return redirect("home")  # Redirect staff to home page

        return self.get_response(request)
"""