# accounts/views.py
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')
    
class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

# projects/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Project, ProjectFile
from .forms import ProjectForm, ProjectFileForm

class ProjectListView(ListView):
    model = Project
    template_name = 'projects/list.html'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(is_approved=True)
        # Add filtering logic here
        return queryset

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['files'] = self.object.files.all()
        return context

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create.html'
    success_url = reverse_lazy('project_list')
    
    def form_valid(self, form):
        form.instance.submitted_by = self.request.user
        return super().form_valid(form)

class ProjectFileUploadView(LoginRequiredMixin, CreateView):
    model = ProjectFile
    form_class = ProjectFileForm
    template_name = 'projects/upload_file.html'
    
    def form_valid(self, form):
        form.instance.project = Project.objects.get(pk=self.kwargs['project_id'])
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.kwargs['project_id']})

class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'admin/dashboard.html'
    
    def test_func(self):
        return self.request.user.role == 'ADMIN'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pending_projects'] = Project.objects.filter(is_approved=False)
        context['recent_uploads'] = ProjectFile.objects.order_by('-uploaded_at')[:10]
        return context
