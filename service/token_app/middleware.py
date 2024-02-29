def AddRefreshToBody(get_response):
    def middleware(request):
        if 'refresh' in request.COOKIES:
            token = request.COOKIES.get('refresh')
            request.POST._mutable = True
            request.POST['refresh'] = token
            request.POST._mutable = False
        return get_response(request)
    
    return middleware
