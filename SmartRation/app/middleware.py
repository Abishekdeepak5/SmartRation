from django.shortcuts import redirect

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    
    def __call__(self, request):
        allowed_paths = ["/login/", "/register/", "/static/"] 

        if not request.session.get("user_id") and request.path not in allowed_paths:
            return redirect("login")  

        return self.get_response(request)
