from django.urls import path

from proexe.dynamic_tables.views.create_dynamic_table import CreateDynamicTableAPIView

app_name = "dynamic_tables"
urlpatterns = [
    path("table/", view=CreateDynamicTableAPIView.as_view(), name="create_table"),
]
