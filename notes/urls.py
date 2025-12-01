from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('', views.NotesView.as_view()), 
    path('<int:id>/', views.NotesDetailView.as_view()),
    path('<int:id>/summarize/', views.NoteSummarizer.as_view()),
    path("ai/paraphrase/", views.ParaphraseAPI.as_view()),
    path("ai/keywords/", views.KeywordsApi.as_view()),
    path("ai/titlegen/", views.TitleGenAPi.as_view()),
]


