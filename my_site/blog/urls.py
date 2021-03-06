from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("",views.StartingPage.as_view(),name='starting-page'),
    path("posts",views.AllPostsView.as_view(),name='posts-page'),
    #slug: checks the uls patterns
    path("posts/<slug:slug>",views.SinglePostView.as_view(),name='post-page-details'),
    path("read-later",views.ReadLaterView.as_view(),name="read-later")
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL,document_root= settings.STATIC_ROOT)
