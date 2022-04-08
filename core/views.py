from django.shortcuts import redirect
from GrodskiSite.settings import site_settings

# Create your views here.


def youtube(request):
    return redirect(site_settings['youtube_url'])
