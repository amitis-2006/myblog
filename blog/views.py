

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_protect

from .models import Post
from django.http import HttpResponse
from django.views.generic.edit import CreateView , UpdateView , DeleteView
from django.urls import reverse_lazy
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import  login , authenticate
from django.shortcuts import redirect
from .forms import signUpForm
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import  ContentType
from .models import Post
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render
from django.core.paginator import Paginator
from .forms import CommentForm
from django.contrib import messages
from . models import Profile
from .forms import ProfileForm , UserForm
from .forms import ContactForm
from django.core.mail import send_mail




class PostCreateView(LoginRequiredMixin , CreateView):
    model=Post
    form_class=PostForm
    template_name='blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin , UpdateView):
    model=Post
    form_class=PostForm
    template_name='blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')
    login_url='/login/'
    redirect_field_name = 'next'
    def get_object(self, queryset=None):
        return get_object_or_404(Post, slug=self.kwargs['slug'] , author=self.request.user)

class PostDeleteView(LoginRequiredMixin , DeleteView):
    model=Post
    template_name='blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
    login_url = '/login/'
    redirect_field_name = 'next'
    def get_object(self, queryset=None):
        return get_object_or_404(Post, slug=self.kwargs['slug'] , author=self.request.user)

class MyLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = AuthenticationForm
    redirect_authenticated_user = True
    def get_success_url(self):
        return '/admin/'

def index(request):
    return HttpResponse("Hello")

def post_list(request):
    posts = Post.objects.filter(status='published').order_by('-published')
    paginator = Paginator(posts , 3)
    page_number = request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    post_count = posts.count()

    return render(request, 'blog/post/list.html',{
        'posts': posts,
        'post_count':post_count,
        'page_obj': page_obj,
    })

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    post.view_count +=1
    post.save(update_fields=['view_count'])

    comments = post.comments.all()
    new_comment = None

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                new_comment = form.save(commit=False)
                new_comment.post = post
                new_comment.author = request.user
                new_comment.save()
                messages.success(request, 'Your comment has been posted to you successfully!')
                return redirect('blog:post_detail', slug=slug)
            else:
                return redirect('blog:login')
    else:
        form = CommentForm()

    return render(request, 'blog/detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'new_comment': new_comment
    })

def signup_view(request):
    print("signup_view called")
    if request.method == "POST":
        form = signUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff = True
            user.save()

            content_type =ContentType.objects.get_for_model(Post)
            permissions = Permission.objects.filter(content_type=content_type)
            user.user_permissions.add(*permissions)

            login(request, user)
            return redirect('/admin/')
        else:
            print("form errors:" , form.errors)
    else:
        form = signUpForm()
    return render(request , "registration/signup.html" , {'form':form})

def login_view(request):
    form = AuthenticationForm(request , data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            login(request, form.get_user())
            return redirect ('blog:post_list')
    return render(request , "registration/login.html" , {'form':form})

def home(request):
    posts=Post.objects.all().order_by('-published')[:3]
    return render(request, 'blog/home.html' , {'posts':posts})
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
    else:
        form = PostForm()
    return render(request, 'your_template.html', {'form': form})


@login_required(login_url='/login/')
def profile_view(request):
    user = request.user
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('blog:profile')
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'blog/profile.html', context)
@csrf_protect
@login_required
def request_publish(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == 'POST' and post.status == 'draft':
        post.status = 'pending'
        post.save(update_fields=['status'])
        messages.success(request, 'Post has been sent for approval.')
    return redirect('blog:profile')

def contact_us(request):
    if request.method=='POST':
        form= ContactForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['name']
            email=form.cleaned_data['email']
            message=form.cleaned_data['message']
            subject=f"New contact message from {name}"
            message_body = f"sender:{name}\nEmail:{email}\n\nMessage:{message}"

            send_mail(
                subject,
                message_body,
                email,
                ['amitiskatebi2006@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, 'Your message was sent successfully.thank you for contacting us.')
            return redirect('blog:contact_us')
    else:
        form = ContactForm()
    return render(request, 'blog/contact_us.html',{'form':form})