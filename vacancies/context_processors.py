def base_page(request) -> dict:
    return {
        'previous_page': request.META['HTTP_REFERER'],
    }
