from django.shortcuts import render


def page_not_found_view(request, exception):
    return render(request, 'front/errors/404.html', status=404)


def permission_denied_view(request, exception):
    return render(request, 'front/errors/403.html', status=403)


def server_error_view(request, *args):
    return render(request, 'front/errors/500.html', status=500)
