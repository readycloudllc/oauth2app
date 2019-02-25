def get_from_request_data(request, attr, default=None):
    return request.POST.get(attr, request.GET.get(attr, default))
