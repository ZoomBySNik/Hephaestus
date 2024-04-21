from django.shortcuts import redirect


class AllowOnlySpecificPagesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Определите страницы, к которым вы хотите разрешить доступ
        self.allowed_pages = ['/login/', '/select_user_type/', '/registration/job_seeker', '/registration/employer']

    def __call__(self, request):
        response = self.get_response(request)

        if not request.user.is_authenticated and request.path not in self.allowed_pages:
            return redirect('login')

        return response


class ErrorHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # Перенаправление на определенное представление при исключении
        return redirect('error_page', error_message=str(exception))
