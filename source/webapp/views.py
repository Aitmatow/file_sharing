from urllib.parse import urlencode

from django.db.models import Q

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, DeleteView

from webapp.forms import SimpleSearchForm, FileForm
from webapp.models import File


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
    form_class = FileForm

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if self.request.user.id == None:
            user = None
        else:
            user = self.request.user
        if form.is_valid():
            File.objects.create(
                file=form.cleaned_data['file'],
                description=form.cleaned_data['description'],
                created_by=user
            )
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class FileDelete(DeleteView):
    template_name = 'file/file_delete.html'
    model = File
    success_url = reverse_lazy('file_list')
