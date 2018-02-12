from django.shortcuts import render

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required()
def socialMediaView(request):
    template_name = 'socialMedia.html'
    user = User.objects.get(username=request.user.username)

    return render(request=request, template_name=template_name, context={'cryptocurrency': table}, )