import io
import requests
from zipfile import ZipFile
import base64
from django.shortcuts import render, HttpResponse, redirect
from classes.models import Class, Page, Category
from bs4 import BeautifulSoup
from pathlib import Path
# Create your views here.


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


def view_subject(request, pk_dynamic):
    # Check that user specified correct class and has permissions.

    subject = Class.objects.filter(subject_id=pk_dynamic).first()
    if not subject:
        return render(request, "classes/errors.html", context={"not_found": True})
    if subject not in request.user.classes.all():
        return render(request, "classes/errors.html", context={"not_found": False, "no_perms": True})

    path = request.GET.get('path')
    ctx = {"pk": pk_dynamic, "subject": subject}
    if path:
        path = Path(path)
        if len(path.parts) > 2:
            page = "/" + path.parts[2].replace("\\", "/")
        else:
            page = ''
        category = Category.objects.filter(path=str(path.parent).replace("\\", "/")).first()

        if category and category in subject.subcategories.all():
            for subpage in category.subpages.all():
                if subpage.path == page:
                    soup = BeautifulSoup(subpage.content, features="html.parser")
                    head = soup.find("style")
                    content = ''.join(map(str, soup.find("body").children))
                    ctx['content'] = str(head) + str(content).replace("&lt;iframe", "<iframe").replace("&gt;", ">")
                    return render(request, template_name="classes/class_page_view_subpage.html", context=ctx)
    return render(request, template_name="classes/class_page_view_main.html", context=ctx)


def new_page(request):
    ctx = {"subjects": Class.objects.all(),
           "quarter": Category.objects.all()}

    if request.GET.get("redirect"):
        ctx['redirect'] = request.GET.get('redirect')

    print(request.POST)
    if request.method == "POST":
        redirect_ = request.POST.get("redirect")
        subject = request.POST.get("subject")
        category = request.POST.get("category")
        pageTitle = request.POST.get("pageTitle")
        documentURL = request.POST.get("documentURL")
        if not (redirect_ and subject and category and pageTitle and documentURL):
            return render(request, template_name="classes/new_page.html", context=ctx)
        page_path = "/" + pageTitle.replace(" ", "-").lower().replace("/", "-").replace("\\", "-")

        if not all((pageTitle, page_path, documentURL)):
            print("Missing")
            return HttpResponse(request, "400")
        html = google_doc_to_page(documentURL)
        page = Page(content=html, title=pageTitle, path=page_path)
        page.save()
        category_objects = Category.objects.filter(path=category)
        subject_object = Class.objects.filter(subject_id=subject).first()

        for category_ob in category_objects:
            if category_ob in subject_object.subcategories.all():
                category = category_ob
                break
        category.subpages.add(page)
        category.save()
        if redirect_:
            return redirect(redirect_)
    return render(request, template_name="classes/new_page.html", context=ctx)


def new_category(request):
    ctx = {"subjects": Class.objects.all()}
    if request.method == "GET":
        return render(request, "classes/new_category.html", context=ctx)
    if request.method == "POST":
        name = request.POST.get("category")
        subject = request.POST.get("subject")
        if not (name and subject):
            return redirect(request.GET.get("redirect"))
        subject_object = Class.objects.filter(subject_id=subject).first()
        category_path = "/" + name.replace(" ", "-").lower().replace("/", "-").replace("\\", "-")

        category = Category(name=name, path=category_path)
        category.save()
        subject_object.subcategories.add(category)
        subject_object.save()
        return redirect(request.GET.get("redirect"))