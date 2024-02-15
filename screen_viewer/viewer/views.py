from typing import Any
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.http import HttpResponse, JsonResponse
from screen_viewer.settings import SCREEN_DATE_FORMAT

from datetime import datetime

from .models import Location, Screenshot
from .forms import LocationForm
from users.decorators import superuser_required
from users.forms import DeleteForm


@method_decorator(login_required, name="dispatch")
class Viewer(TemplateView):
    template_name = "viewer.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_superuser:
            context['locations'] = Location.objects.all()
        else:
            context['locations'] = Location.objects.filter(profile__user=self.request.user)
        return context
    

@method_decorator(superuser_required, name='dispatch')
class LocationsView(ListView):
    template_name = "locations.html"
    model = Location


@method_decorator(superuser_required, name='dispatch')
class AddLocationView(CreateView):
    template_name = "location.html"
    model = Location
    success_url = reverse_lazy("viewer:locations")
    form_class = LocationForm


@method_decorator(superuser_required, name='dispatch')
class EditLocationView(UpdateView):
    template_name = "location_edit.html"
    model = Location
    success_url = reverse_lazy("viewer:locations")
    form_class = LocationForm
    


@method_decorator(superuser_required, name='dispatch')
class DeleteLocationView(DeleteView):
    model = Location
    success_url = reverse_lazy("viewer:locations")
    form_class = DeleteForm
    template_name = "location_delete.html"


@login_required
def load_data(request):
    screen_date = datetime.strptime(request.GET.get('date'), '%d.%m.%Y')
    location_id = int(request.GET.get('location'))
    screenshots = Screenshot.objects.filter(screen_date=screen_date, 
                                            location__id=location_id)\
                                    .order_by('img_created_at')\
                                    .values('path', 
                                            'thmb_path', 
                                            'img_created_at')
    
    return JsonResponse({"success": True, "data": list(screenshots)})