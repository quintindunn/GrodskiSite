from django.shortcuts import HttpResponse
import requests
from zipfile import ZipFile
import io
import base64
from classes.models import Class, Category, Page


def google_doc_to_page(url):
    url = url.split("/document/")[1].replace("d/", "").split("/")[0]
    url = f"https://docs.google.com/document/export?format=zip&id={url}"
    r = requests.get(url)
    file = io.BytesIO(r.content)
    zipfile = ZipFile(file)
    html_file = [zipfile.open(i.filename).read().decode() for i in zipfile.filelist if i.filename.endswith(".html")][0]
    images = [i.filename for i in zipfile.filelist if
              i.filename.endswith(".png") or
              i.filename.endswith(".jpg") or
              i.filename.endswith(".jpeg")
    ]
    encoded_images = {}
    for image in images:
        image_content = zipfile.open(image).read()
        encoded_images[image] = "data:image/png;base64," + base64.b64encode(image_content).decode()

    for image, b64 in encoded_images.items():
        html_file = html_file.replace(f"src=\"{image}\"", f"src=\"{b64}\"")

    return html_file


def new_page(request):
    page_title = request.GET.get("pageTitle")
    path = request.GET.get("path")
    document_share_url = request.GET.get("documentURL")
    subject = request.GET.get("subject")
    category = request.GET.get("category")
    if not all((page_title, path, document_share_url)):
        print("Missing")
        return HttpResponse(request, "400")
    html = google_doc_to_page(document_share_url)
    page = Page(content=html, title=page_title, path=path)
    page.save()
    category_objects = Category.objects.filter(path=category)
    subject_object = Class.objects.filter(subject_id=subject).first()

    for category_ob in category_objects:
        if category_ob in subject_object.subcategories.all():
            category = category_ob
            break
    category.subpages.add(page)
    category.save()
    return HttpResponse(request, "page")


