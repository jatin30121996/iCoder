from django.shortcuts import render, HttpResponse, redirect
from .models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def home(request):
    return render(request, "home/home.html")


def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name) < 2 or len(email) < 3 or len(phone) < 10 or len(content) < 4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been successfully sent")
    return render(request, "home/contact.html")


def about(request):
    return render(request, "home/about.html")


def search(request):
    query = request.GET.get('query')
    if query != "":
        allPoststitle = Post.objects.filter(title__icontains=query)
        allPostscontent = Post.objects.filter(content__icontains=query)
        allPosts = allPoststitle.union(allPostscontent)
        params = {'allPosts': allPosts, 'query':query}
    elif len(query) > 78:
        params = {'allPosts': [], 'query': query}
        messages.warning(request, "No search results found")
    else:
        params = {'allPosts':[], 'query':query}
        messages.warning(request, "No search results found")
    return render(request, 'home/search.html', params)


def handleSignUp(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect('home')
        if not username.isalnum():
            messages.error(request, "Username should only contain letters and numbers")
            return redirect('home')
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('home')
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your iCoder account has been successfully created")
        return redirect('home')

    else:
        return HttpResponse('404 - Not Found')


def handleLogin(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpass']
        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials, Please try again")
            return redirect('home')
    return HttpResponse("404 - Not Found")


def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('home')