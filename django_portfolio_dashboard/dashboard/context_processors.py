from .models import PortfolioSettings

def user_settings(request):
    if request.user.is_authenticated:
        settings, created = PortfolioSettings.objects.get_or_create(user=request.user)
        return {'settings': settings}
    return {'settings': None}