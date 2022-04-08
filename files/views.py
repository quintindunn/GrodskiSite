from django.http import FileResponse, HttpResponse


# Create your views here.
def get_file(request, pk_dynamic):
    return FileResponse(open(f"files/static/files/{pk_dynamic}", 'rb'))
