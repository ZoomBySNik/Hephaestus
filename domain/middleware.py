from django.shortcuts import redirect


class AllowOnlySpecificPagesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Определите страницы, к которым вы хотите разрешить доступ
        self.allowed_pages = ['/login/']

    def __call__(self, request):
        response = self.get_response(request)

        if not request.user.is_authenticated and request.path not in self.allowed_pages:
            return redirect('login')

        return response
