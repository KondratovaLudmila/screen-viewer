from django.urls import path

from . import views

app_name = "viewer"

urlpatterns = [
    path('locations', views.LocationsView.as_view(), name='locations'),
    path('locations/add', views.AddLocationView.as_view(), name='location_add'),
    path('locations/<int:pk>/edit', views.EditLocationView.as_view(), name='location_edit'),
    path('locations/<int:pk>/delete', views.DeleteLocationView.as_view(), name='location_delete'),
    path('load_data', views.load_data, name='load_data'),
    path('', views.Viewer.as_view(), name='viewer'),
]