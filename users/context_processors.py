from transmister.settings import PRICE_PER_MINUTE


def user_abbr(request):
    if request.user.is_authenticated:
        return {"user_abbr": request.user.email.split("@")[0]}
    return ""


def get_minute_price(request):
    return {"minute_price": PRICE_PER_MINUTE}
