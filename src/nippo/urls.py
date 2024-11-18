from django.urls import path
from .views import (
                    NippoListView,
                    NippoDetailView,
                    NippoCreateModelFormView,
                    NippoUpdateModelFormView,
                    NippoDeleteView
                    )

urlpatterns = [
    # mainのurls.pyで'nippo/'でここを指定しているのでそれ以降を指定する
    path("", NippoListView.as_view(), name="nippo-list"),
    path("detail/<slug:slug>/", NippoDetailView.as_view(), name="nippo-detail"),
    path("create/", NippoCreateModelFormView.as_view(), name="nippo-create"),
    path("update/<slug:slug>/", NippoUpdateModelFormView.as_view(), name="nippo-update"),
    path("delete/<slug:slug>/", NippoDeleteView.as_view(), name="nippo-delete"),

    # path("create/", nippoCreateView, name="nippo-create"),
    # path("update/<int:pk>/", nippoUpdateView, name="nippo-update"),
    # path("create/", NippoCreateFormView.as_view(), name="nippo-create"),
    # path("delete/<int:pk>/", nippoDeleteView, name="nippo-delete"),
]
