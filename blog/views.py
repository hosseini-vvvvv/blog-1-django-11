from ast import Try
import email
from itertools import count
from nntplib import ArticleInfo
from pdb import post_mortem
from pydoc import describe
from re import template
from telnetlib import LOGOUT
# from smtplib import _AuthObject
# from ssl import _PasswordType
from turtle import title
from unittest import result
from urllib import request
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
# from tomlkit import comment
from .models import Account, Article, Category, Test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView
from .forms import *
# =======>>> * yani harchi to form bood khodet importesh kon
from django.core.mail import send_mail    #eshterak ba email
from taggit.models import Tag   #for TAG
from django.db.models import Count   #for TAG Similar
from django.contrib.postgres.search import SearchVector,SearchQuery,TrigramSimilarity  #for search
from django.db.models.functions import Greatest  #for search
from django.db.models import Q   #for search
from django.contrib.auth import login,authenticate,logout  #for login
from django.contrib.auth import login as auth_login





class Meta:
        db_table = ''
        managed = True
        verbose_name = 'ModelName'
        verbose_name_plural = 'ModelNames'




def home(request):
    context = {
        "articles": Article.objects.filter(status="p"),

    }
    return render(request, "page/home.html", context)


def detail(request, slug):
    context = {
        "article": get_object_or_404(Article, slug=slug, status='p')

    }
    return render(request, "page/detail.html", context)


def category(request, slug):
    context = {
        "category": get_object_or_404(Category, slug=slug, status=True)

    }
    return render(request, "page/category.html", context)


def index(request):

    return render(request,'page/index.html')





# def site(request,slug):
#     context = {
#         "test": get_object_or_404(Test, slug=slug, status='p')

#     }
#     return render(request,"page/test.html",context)

def site(request,slug,pk):
    context = get_object_or_404(Test,status='p',slug=slug,id=pk)
    comments=context.comments.filter(active=True)
    # >>>>======= ya
    # comments = Comment.objects.filter(post=context)
    new_comment=None
    if request.method=='POST':
        comment_form=CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.post=context
            new_comment.save()
    else:
        
        ids=Test.tags.values_list('id',flat=True)
        similar_posts=Test.objects.filter(tags__in=ids).exclude(id=context.id)
        print(similar_posts)
        similar_posts=similar_posts.annotate(s_count=Count('tags')).order_by('-s_count','-published')
        for i in  similar_posts:
            print(i.title,i.s_count)
        
    
    
    
        comment_form=CommentForm()
    contexts={
        'context':context,
        'comments':comments,
        'new_comment':new_comment,
        'comment_form':comment_form,
        'similar_posts':similar_posts 
        
        
    }    
    return render(request,"page/test.html",contexts)


def users(request,tag_slug=None):
     
    
    
    posts=Test.objects.all()
    tag=None   #for TAG
    if tag_slug:
        tag=Tag.objects.get(slug=tag_slug)
        posts=posts.filter(tags__in=[tag])    #for TAG
        
    paginator=Paginator(posts,2)
    page=request.GET.get('page')
    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)
    
    return render(request,"page/users.html",{'posts':posts,'page':page,'tag':tag})   #for TAG
# ========>* baraye TAGS
# >>>>> BEJAYE BALAII PAIINI ESTEFADE MISHAVAD <<<<<<<<




# class PostListView(ListView):
#     queryset = Test.objects.all()
#     context_object_name = "posts"
#     paginate_by = 1
#     template_name = 'page/users.html'


def UserAccount(request):
    user = request.user
    try:
        account = Account.objects.get(user=user)
    except:
        account = Account.objects.create(user=user)

    if request.method == "POST":
        form = AccountForm(request.POST)

        if form.is_valid():
            user.first_name = form.cleaned_data['name']
            user.last_name = form.cleaned_data['last_name']
            account.gender = form.cleaned_data['gender']
            account.address = form.cleaned_data['address']
            account.age = form.cleaned_data['age']
            account.phone = form.cleaned_data['phone']
            user.save()
            account.save()
            return redirect('blog:index')
        else:

            return render(request,'page/forms/account_form.html', {'form':form,'account': account})
    form = AccountForm()
    return render(request,'page/forms/account_form.html', {'form':form,'account':account})




def ContactUs(request):
    sent=False
    
    if request.method=='POST':
        
            form=ContactusForm(request.POST)
            if form.is_valid():
                cd=form.cleaned_data
                subject=cd['subject']
                name=cd['name']
                email=cd['email']
                phone=cd['phone']
                message=cd['message']
                msg="name:{0}\nphone:{1}\nemail:{2}\nmessage:\n{3}".format(name,phone,email,message)
                
                send_mail(subject,msg,'django1401test@gmail.com',['django1401test@gmail.com'],fail_silently=False)
                sent=True
    else:
        form=ContactusForm()
    return render(request,'page/forms/contact_us.html',{'form':form,'sent':sent})
    


def SharePost(request,post_id):
    
    post= get_object_or_404(Test,status='p',id=post_id)
    sent=False
    
    if request.method=='POST':
        form=shareForm(request.POST)
        if form.is_valid():
            
            cd=form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject=' {0} has invited you to read {1} post'.format(cd['name'],post.title)
            # name=cd['name']
            message=cd['message']
            msg="{0} has invited you to read {1} post{2}{3}{4}{5}".format(cd['name'],post.title,'\n',message,'\n',post_url)
        
            send_mail(subject,msg,'django1401test@gmail.com',[cd['to']],fail_silently=False)
            sent=True
    else:
        form=shareForm()
    return render(request,'page/forms/share_post.html',{'form':form,'post':post})






def search(request,tag_slug=None):
   
    if request.method=='POST':
        query_name=request.POST.get('search_input')
        if query_name:
            request.session['query_se']=query_name
        else:
            try:
                query_name=request.session['query_se']
            except:
                query_name=""  
            posts=Test.objects.annotate(similarity=Greatest(TrigramSimilarity('description',query_name),TrigramSimilarity('title',query_name))).filter(similarity__gt=0).order_by('-similarity')
            tag=None  
        if tag_slug:
            tag=Tag.objects.get(slug=tag_slug)
            posts=posts.filter(tags__in=[tag])    
    
        paginator=Paginator(posts,2)
        page=request.GET.get('page')
        try:
            posts=paginator.page(page)
        except PageNotAnInteger:
            posts=paginator.page(1)
        except EmptyPage:
            posts=paginator.page(paginator.num_pages)
        return render(request,"page/users.html",{'posts':posts,'page':page,'tag':tag})   #for TAG
   




def user_login(request): 
  if request.method=='POST':
      form=LoginForm(request.POST)
      if form.is_valid():
          cd=form.cleaned_data
          user=authenticate (request,username=cd['username'],password=cd['password'])
          if user is not None:
            if user.is_active:
                # login(user,request)
                return redirect('blog:index')
            else:
                return HttpResponse ('<h1>اکانت شما غیر فعال است</h1>')
          else:
                return HttpResponse ('<h1>اطلاعات شما نادرست است</h1>')   
  else:
      form=LoginForm()
  return render(request,'page/forms/account/login.html',{'form':form})



def user_logout(request):
    logout(request)
    return redirect("blog:index")


def change_password(request): 
  if request.method=='POST':
      user=request.user
      form=ChangePasswordForm(request.POST)
      if form.is_valid():
          cd=form.cleaned_data
          old_password=cd['old_password']
          new_password1=cd['new_password1']
          new_password2=cd['new_password2']
          if not user.check_password(old_password):
          
             return HttpResponse ('<h1>  پسورد قبلی شما درست نیست</h1>')
          elif new_password1!= new_password2:
            
             return HttpResponse ('<h1>پسورد های جدید شما باهم مطابقت ندارند</h1>')

          else:
              user.set_password(new_password1)
              user.save()
              return HttpResponse ('<h1>پسورد شما تغییر یافت</h1>')

  else:       
     form=LoginForm()
  return render(request,'page/forms/account/change_password.html',{'form':form})