from django.db import models
from django.conf import settings
# Create your models here.
from django.utils import timezone

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
# image
# from django_resized import ResizedImageField


class Category(models.Model):
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    img = models.FileField(
        upload_to='pics/category')
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        # enforcing that there can not be two categories under a parent with same slug

        # __str__ method elaborated later in post.  use __unicode__ in place of

        # __str__ if you are using python 2
        ordering = ('name',)
        unique_together = ('slug', 'parent',)
        verbose_name = 'category'
        verbose_name_plural = "categories"

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])


class Web(models.Model):
    TYPE_CHOICES = (('.dst', '.DST'),
                    ('.emb', '.EMB'),)

    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.CASCADE)

    design_code = models.CharField(max_length=50, default=None)
    name = models.CharField(max_length=100)
    needle = models.IntegerField()
    stitch = models.IntegerField()
    area = models.IntegerField()
    image = models.FileField(
        upload_to='pics/Product_image')
    price = models.FloatField(default=0)
    # image = models.FileField(
    #     upload_to='pics')
    #
    # image1 = ResizedImageField(size=[500, 300], upload_to='pics')
    design_type = models.CharField(
        max_length=15, choices=TYPE_CHOICES, default='.emb')
    description = models.CharField(max_length=255, blank=True, default='')
    # file = models.FileField(
    #     _("upload Design file here"), upload_to='pics/File')

    slug = models.SlugField(max_length=200)
    Publish = models.BooleanField()
    Exclusive = models.BooleanField()
    New = models.BooleanField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    published = models.DateTimeField(default=timezone.now)
    wishlist = models.ManyToManyField(
        User, related_name='userwishlist', blank=True)
    # def __init__(self):
    #     # if check_something():
    #     self.fields['publish'].initial = True

    def __str__(self):
        return self.name

    def get_cat_list(self):
        k = self.category  # for now ignore this instance method

        breadcrumb = ["dummy"]
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent
        for i in range(len(breadcrumb)-1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i-1:-1])
        return breadcrumb[-1:0:-1]

    @staticmethod
    def get_all_products_by_categoryid(category_id):

        if category_id:
            return Web.objects.filter(category_id=category_id)
        else:
            return Web.get_all_products()


# class SearchForm(forms.Form):
#     q = forms.CharField(label=_('Search files'), required=False)
class PostImage(models.Model):
    parent_img = models.ForeignKey(Web, default=None, on_delete=models.CASCADE)
    images = models.FileField(upload_to='pics/Product_image')

    def __str__(self):
        return self.parent_img.name


class PostFile(models.Model):
    parent_file = models.ForeignKey(
        Web, default=None, on_delete=models.CASCADE)
    file = models.FileField(upload_to='pics/Product_file')

    def __str__(self):
        return self.parent_file.name


class Search(models.Model):
    keyword = models.CharField(max_length=200)
    count = models.IntegerField(default=0)

    # def __str__(self):
    #     return self.keyword

    # def save(self, searchquery):
    #     self.keyword = searchquery


class Slider(models.Model):
    sliderimg = models.FileField(
        upload_to='pics/slider')
    first_small_heading = models.CharField(max_length=100)
    second_heading = models.CharField(max_length=100)
    third_heading = models.CharField(max_length=100)
    button_text = models.CharField(max_length=100)
    link = models.URLField(max_length=200)

    def __str__(self):
        return self.third_heading
