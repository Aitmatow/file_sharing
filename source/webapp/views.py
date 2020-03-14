from urllib.parse import urlencode

from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Permission, User
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect

from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, FormView, DeleteView, UpdateView

from webapp.forms import SimpleSearchForm, FileForm, AnonFileForm
from webapp.models import File, DEFAULT_PROJECT_STATUS, FilePrivate


class FileList(ListView):
    template_name = 'file/file_list.html'
    model = File
    paginate_by = 10
    paginate_orphans = 1
    page_kwarg = 'page'
    ordering = ['-created_date']

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_search_form(self):
        return SimpleSearchForm(data=self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            access = DEFAULT_PROJECT_STATUS
        )
        if self.search_value:
            queryset = queryset.filter(
                Q(description__icontains=self.search_value)
            )
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context


class FileDetail(DetailView):
    template_name = 'file/file_detail.html'
    model = File
    context_key = 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class FileCreate(FormView):
    template_name = 'file/file_form.html'
    success_url = reverse_lazy('file_list')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if self.request.user.id == None:
            if form.is_valid():
                File.objects.create(
                    file=form.cleaned_data['file'],
                    description=form.cleaned_data['description']
                )
                return self.form_valid(form)
        else:
            if form.is_valid():
                File.objects.create(
                    file=form.cleaned_data['file'],
                    description=form.cleaned_data['description'],
                    created_by=self.request.user,
                    access=form.cleaned_data['access']
                )
                return self.form_valid(form)
        return self.form_invalid(form)

    def get_form_class(self, form_class=None):
        if self.request.user.id != None:
            form = FileForm
        else:
            form = AnonFileForm
        return form

class FileUpdate(UserPassesTestMixin, UpdateView):
    template_name = 'file/file_form.html'
    model = File
    form_class = FileForm

    def get_success_url(self):
        return reverse('file_detail', kwargs={'pk' : self.object.pk})

    def test_func(self):
        file = File.objects.get(id=self.kwargs['pk'])
        if (file.created_by == self.request.user) or (self.request.user.has_perm('webapp.change_file')):
            return self.request.user

class FileDelete(UserPassesTestMixin, DeleteView):
    template_name = 'file/file_delete.html'
    model = File
    success_url = reverse_lazy('file_list')

    def test_func(self):
        file = File.objects.get(id=self.kwargs['pk'])
        if (file.created_by == self.request.user) or (self.request.user.has_perm('webapp.delete_file')):
            return self.request.user


class FileDownload(View):
    def get(self, request):
        file_id = request.GET.get('file_id')
        file = File.objects.get(id=file_id)
        file.downloaded += 1
        file.save()
        return JsonResponse({'status':200})

class PrivateUserDelete( View):
    def post(self, request):
        file = File.objects.get(pk = int(request.POST['file_id']))
        user = User.objects.get(id = int(request.POST['user_id']))
        FilePrivate.objects.filter(file=file, user=user).delete()
        return JsonResponse({'status':'200'})



class PrivateUserAdd(View):
    def post(self, request):
        file = File.objects.get(pk = int(request.POST['file']))
        user = request.POST['user_name']
        try:
            user_obj = User.objects.get(username=user)
            file_exists = FilePrivate.objects.get_or_create(file=file, user=user_obj)
            if file_exists[1] == False:
                return JsonResponse({'answer': 'Пользователь уже существует!'})
            else:
                return JsonResponse({'answer': 'Пользователь успешно добавлен!', 'user' : user_obj.username, 'user_id' : user_obj.id, 'file_id': file.pk})
        except User.DoesNotExist as e:
            print(e)
            return JsonResponse({'answer':'Нет такого пользователя'})

