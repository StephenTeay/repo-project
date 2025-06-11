# projects/views.py
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

@login_required
def download_file(request, file_id):
    project_file = get_object_or_404(ProjectFile, pk=file_id)
    
    # Check if user has permission to download
    if not project_file.project.is_approved and not request.user.role in ['STAFF', 'ADMIN']:
        raise PermissionDenied
    
    response = FileResponse(project_file.file)
    response['Content-Disposition'] = f'attachment; filename="{project_file.file.name}"'
    return response
