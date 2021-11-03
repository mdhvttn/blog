from django.shortcuts import render
from datetime import date
from .models import *
from django.views.generic import ListView
from django.views import View
from .forms import CommentForms
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.




class StartingPage(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    #we have to overide query set
    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


class AllPostsView(ListView):
    template_name = "blog/all_posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"




class SinglePostView(View):

    def is_stored(self,request,post_id):
        
        stored_post = request.session.get("stored_post")
        if stored_post is not None:
            is_saved_for_later = post_id in stored_post

        else:
            is_saved_for_later = False

        return is_saved_for_later

    def get(self,request,slug):
        post = Post.objects.get(slug=slug)
        context = {
            "post":post,
            "post_tags": post.tags.all(),
            "comment_form":CommentForms(),
            "comments":post.comments.all().order_by("-id"),
            
            "save_for_later" : self.is_stored(request, post.id)
        }
        return render(request,'blog/post-details.html',context)


    def post(self,request,slug):
        comment_form = CommentForms(request.POST)
        post = Post.objects.get(slug=slug)


        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()

            return HttpResponseRedirect(
                reverse("post-page-details",args = [slug])
            )
        
        context = {
            "post":post,
            "post_tags": post.tags.all(),
            "comment_form":comment_form,
            "save_for_later" : self.is_stored(request, post.id)
        }
        return render(request,'blog/post-details.html',context)


class ReadLaterView(View):

    def get(self,request):
        stored_post = request.session.get("stored_post")

        context = {}

        if stored_post is None  or len(stored_post) == 0:
            context['posts'] = []
            context['has_posts'] = False
        else:
            posts = Post.objects.filter(id__in=stored_post)
            context['posts'] = posts
            context['has_posts'] = True
        
        return render(request,'blog/stored_posts.html',context)


    def post(self,request):
        stored_post = request.session.get("stored_post")

        if stored_post is None:
            stored_post = []

        post_id = int(request.POST['post_id'])

        if post_id not in stored_post:
            stored_post.append(post_id)
        else:
            stored_post.remove(post_id)
        
        request.session["stored_post"] = stored_post


        return HttpResponseRedirect("/")


















