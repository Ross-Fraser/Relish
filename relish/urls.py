from django.contrib import admin
from django.urls import path, include

handler404 = 'roastery.views.custom_page_not_found'
handler403 = 'roastery.views.custom_permission_denied_view'


urlpatterns = [
    path("admin/", admin.site.urls),
    path("summernote/", include("django_summernote.urls")),
    path("", include("roastery.urls"), name="roastery-urls"),
    path("accounts/", include("accounts.urls")),
    path("", include("django.contrib.auth.urls")),
    path("roastery/", include("roastery.urls")),
    path("", include("roastery.urls")),
    path("bag/", include("bag.urls")),
]
