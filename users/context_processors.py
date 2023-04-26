def user_abbr(request):
    if request.user.is_authenticated:
        return {"user_abbr": request.user.email.split("@")[0]}
    return ""
