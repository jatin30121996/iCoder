from django.shortcuts import render, HttpResponse, redirect
from .models import Post, BlogComment
from django.contrib import messages
from .templatetags import extras

# Create your views here.
def blogHome(request):
    allPosts = Post.objects.all()
    context = {"allPosts": allPosts}
    return render(request, 'blog/blogHome.html', context)


def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    repDict = {}
    for replay in replies:
        if replay.parent.sno not in repDict.keys():
            repDict[replay.parent.sno] = [replay]
        else:
            repDict[replay.parent.sno].append(replay)
    context = {"post": post, 'comments':comments, 'user': request.user, 'replyDict': repDict}
    return render(request, 'blog/blogPost.html', context)


def postComment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        parentSno = request.POST.get("parentSno")
        post = Post.objects.get(sno=postSno)
        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, "Your replay has been posted successfully")
    return redirect(f"/blog/{post.slug}")

