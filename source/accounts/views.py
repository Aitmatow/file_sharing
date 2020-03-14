from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import DetailView, UpdateView, ListView


from accounts.forms import SignUpForm
from webapp.models import File


def login_view(request):
    context = {}
    if request.method == 'GET':
        next_url = request.GET.get('next', '')
        context['next'] = next_url
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if next_url:
                return redirect(next_url)
            return redirect('file_list')
        else:
            context['next'] = next_url
            context['has_error'] = True
    return render(request, 'login.html', context=context)

def logout_view(request):
    logout(request)
    return redirect('file_list')

def register_view(request):
    if request.method == 'GET':
        form = SignUpForm()
        return render(request, 'register.html', context={'form':form})
    elif request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data.get('username'),
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                is_active=True
            )
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            return redirect('file_list')
        else:
            return render(request, 'register.html', context={'form': form})

class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['files'] = File.objects.filter(created_by=self.request.user).order_by('-created_date')
        return context

class UsersList(ListView):
    template_name = 'users_list.html'
    model = User
    paginate_by = 5
    paginate_orphans = 1
    page_kwarg = 'page'

