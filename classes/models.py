from django.db import models
# Create your models here.
#     parent_subject = models.OneToOneField(Class, on_delete=models.CASCADE, null=True)


class Page(models.Model):
    content = models.TextField(
        max_length=4294967295,
        verbose_name="Page Content (HTML)",
        default="",
        blank=True,
        null=True
    )

    title = models.CharField(max_length=63, verbose_name="Page Title", default="", null=True, blank=True)
    path = models.CharField(max_length=127, verbose_name="URL", default="", null=True, blank=True)

    def __str__(self):
        return f"{self.title} //{self.path}"


class Category(models.Model):
    name = models.CharField(max_length=31, verbose_name="Category", default="", null=True, blank=True)
    path = models.CharField(max_length=31, default="", null=False, blank=False)

    subpages = models.ManyToManyField(Page, blank=True)

    def __str__(self):
        return f"{self.name}"


class Class(models.Model):
    subject_id = models.CharField(max_length=127, default="NULL")
    subject_name = models.CharField(max_length=127, default="NULL")
    background_image_url = models.CharField(max_length=32768, default="", null=True, blank=True)

    subcategories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.subject_name
