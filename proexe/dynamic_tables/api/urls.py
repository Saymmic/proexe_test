from django.urls import path

from proexe.dynamic_tables.api.views import (
    DynamicTableListRowsCreateApi,
    DynamicTableRowCreateApi,
    TableCreateApi,
    TableUpdateApi,
)

app_name = "dynamic_tables"

urlpatterns = [
    path("table/", TableCreateApi.as_view(), name="create"),
    path("table/<str:pk>/", TableUpdateApi.as_view(), name="update"),
    path("table/<str:pk>/row/", DynamicTableRowCreateApi.as_view(), name="create_row"),
    path("table/<str:pk>/rows/", DynamicTableListRowsCreateApi.as_view(), name="list_rows"),
]
