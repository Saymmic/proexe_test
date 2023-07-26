from django.urls import path

from proexe.dynamic_tables.api.views import TableCreateApi

app_name = "dynamic_tables"

urlpatterns = [
    path("table/", TableCreateApi.as_view(), name="create"),
    # path("<int:course_id>/", CourseDetailApi.as_view(), name="detail"),
    # path("create/", CourseCreateApi.as_view(), name="create"),
    # path("<int:course_id>/update/", CourseUpdateApi.as_view(), name="update"),
    # path("<int:course_id>/specific-action/", CourseSpecificActionApi.as_view(), name="specific-action"),
]
