from django.contrib import admin
from django.urls import include, path
from apps.reports.views import home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("accounts/", include("apps.accounts.urls")),
    path("catalog/", include("apps.catalog.urls")),
    path("journal/", include("apps.journal.urls")),
    path("reports/", include("apps.reports.urls")),
]
