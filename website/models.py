from django.db import models

# Ckeditor support
from ckeditor.fields import RichTextField

# Image croppig support and thumbnails engine
from image_cropping import ImageRatioField
from easy_thumbnails.files import get_thumbnailer

# WebLayout models
from weblayout.models import Template

# Config variables
from frankie_web_platform.settings import GALLERY_IMAGE_LARGE, GALLERY_IMAGE_MEDIUM, GALLERY_IMAGE_SMALL


class StaticPage(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, unique=True)
    url = models.CharField(max_length=256, unique=True)
    first_text = RichTextField(null=True, blank=True)
    second_text = RichTextField(null=True, blank=True)
    gallery = models.ForeignKey('Gallery', null=True, blank=True)
    meta_description = models.CharField(max_length=256,
                                        null=True, blank=True)
    title = models.CharField(max_length=256)
    meta_canonical = models.CharField(max_length=256,
                                      null=True, blank=True)
    meta_robots = models.CharField(max_length=256,
                                   null=True, blank=True)
    h1 = models.CharField(max_length=256,
                          null=True, blank=True)
    description = models.CharField(max_length=256,
                                   null=True, blank=True)
    is_news = models.BooleanField()
    first_image = models.ImageField(
        upload_to="static_page/", null=True, blank=True)
    second_image = models.ImageField(
        upload_to="static_page/", null=True, blank=True)
    template = models.ForeignKey(Template)
    creation_date = models.DateField(auto_now_add=True, blank=True)
    last_edit_date = models.DateField(auto_now=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'static_pages'
        verbose_name = 'Static Page'
        verbose_name_plural = 'Static Pages'


class GalleryImagePosition(models.Model):
    id = models.AutoField(primary_key=True)
    image_original = models.ImageField(
        upload_to="image_positions/galleries/")
    cropping_large = ImageRatioField('image_original', GALLERY_IMAGE_LARGE)
    cropping_medium = ImageRatioField('image_original', GALLERY_IMAGE_MEDIUM)
    cropping_small = ImageRatioField('image_original', GALLERY_IMAGE_SMALL)

    name = models.CharField(max_length=256, unique=True)
    title = models.CharField(max_length=256)
    creation_date = models.DateField(auto_now_add=True, blank=True)
    last_edit_date = models.DateField(auto_now=True, blank=True)
    weight = models.IntegerField()
    active = models.BooleanField(default=True)
    description = models.CharField(max_length=256, null=True, blank=True)
    gallery = models.ForeignKey('Gallery')

    def __str__(self):
        return self.name

    def original_image(self):
        return str.format("/media/{0}", self.image_original, self.title)

    original_image.short_description = 'Original'
    original_image.allow_tags = True

    def original_image_admin(self):
        return str.format("<img src=/media/{0} alt='Original Image: {1}' width=100/>", self.image_original, self.title)

    def large_image(self):
        url = get_thumbnailer(self.image_original).get_thumbnail({
            'size': (GALLERY_IMAGE_LARGE[:GALLERY_IMAGE_LARGE.index('x')],
                     GALLERY_IMAGE_LARGE[GALLERY_IMAGE_LARGE.index('x') + 1:]),
            'box': self.cropping_large,
            'crop': True,
            'detail': True,
        }).url
        return url
    large_image.allow_tags = True

    def small_image(self):
        url = get_thumbnailer(self.image_original).get_thumbnail({
            'size': (GALLERY_IMAGE_SMALL[:GALLERY_IMAGE_SMALL.index('x')],
                     GALLERY_IMAGE_SMALL[GALLERY_IMAGE_SMALL.index('x') + 1:]),
            'box': self.cropping_small,
            'crop': True,
            'detail': True,
        }).url
        return url
    small_image.allow_tags = True

    def medium_image(self):
        url = get_thumbnailer(self.image_original).get_thumbnail({
            'size': (GALLERY_IMAGE_MEDIUM[:GALLERY_IMAGE_MEDIUM.index('x')],
                     GALLERY_IMAGE_MEDIUM[GALLERY_IMAGE_MEDIUM.index('x') + 1:]),
            'box': self.cropping_medium,
            'crop': True,
            'detail': True,
        }).url
        return url
    medium_image.allow_tags = True

    def large_image_admin(self):
        url = get_thumbnailer(self.image_original).get_thumbnail({
            'size': (GALLERY_IMAGE_LARGE[:GALLERY_IMAGE_LARGE.index('x')],
                     GALLERY_IMAGE_LARGE[GALLERY_IMAGE_LARGE.index('x') + 1:]),
            'box': self.cropping_large,
            'crop': True,
            'detail': True,
        }).url
        return str.format('<img src={0} width=100 />', url)
    large_image_admin.allow_tags = True

    def small_image_admin(self):
        url = get_thumbnailer(self.image_original).get_thumbnail({
            'size': (GALLERY_IMAGE_SMALL[:GALLERY_IMAGE_SMALL.index('x')],
                     GALLERY_IMAGE_SMALL[GALLERY_IMAGE_SMALL.index('x') + 1:]),
            'box': self.cropping_small,
            'crop': True,
            'detail': True,
        }).url
        return str.format('<img src={0} width=100 />', url)
    small_image_admin.allow_tags = True

    def medium_image_admin(self):
        url = get_thumbnailer(self.image_original).get_thumbnail({
            'size': (GALLERY_IMAGE_MEDIUM[:GALLERY_IMAGE_MEDIUM.index('x')],
                     GALLERY_IMAGE_MEDIUM[GALLERY_IMAGE_MEDIUM.index('x') + 1:]),
            'box': self.cropping_medium,
            'crop': True,
            'detail': True,
        }).url
        return str.format('<img src={0} width=100 />', url)
    medium_image_admin.allow_tags = True

    class Meta:
        db_table = 'gallery_image_positions'
        verbose_name = 'Gallery Image Position'
        verbose_name_plural = 'Gallery Image Positions'


class BannerImagePosition(models.Model):
    id = models.AutoField(primary_key=True)
    image_original = models.ImageField(
        upload_to="image_positions/banners/")
    image_small = models.ImageField(
        upload_to="image_positions/banners/", null=True, blank=True)
    image_medium = models.ImageField(
        upload_to="image_positions/banners/", null=True, blank=True)
    image_large = models.ImageField(
        upload_to="image_positions/banners/", null=True, blank=True)
    name = models.CharField(max_length=256, unique=True)
    title = models.CharField(max_length=256)
    creation_date = models.DateField(auto_now_add=True, blank=True)
    last_edit_date = models.DateField(auto_now=True, blank=True)
    weight = models.IntegerField()
    active = models.BooleanField(default=True)
    description = models.CharField(max_length=256, null=True, blank=True)
    banner = models.ForeignKey('Banner')

    def __str__(self):
        return self.name

    def original_image_admin(self):
        return str.format("<img src=/media/{0} alt='Original Image: {1}' width=100/>", self.image_original, self.title)

    original_image_admin.short_description = 'Original'
    original_image_admin.allow_tags = True

    def original_image(self):
        return str.format("/media/{0}", self.image_original)

    def large_image(self):
        return str.format("/media/{0}", self.image_large)

    def small_image(self):
        return str.format("/media/{0}", self.image_small)

    def medium_image(self):
        return str.format("/media/{0}", self.image_medium)

    def large_image_admin(self):
        return str.format('<img src=/media/{0} width=100 />', self.image_large)
    large_image_admin.allow_tags = True

    def small_image_admin(self):
        return str.format('<img src=/media/{0} width=100 />', self.image_small)
    small_image_admin.allow_tags = True

    def medium_image_admin(self):
        return str.format('<img src=/media/{0} width=100 />', self.image_medium)
    medium_image_admin.allow_tags = True

    class Meta:
        db_table = 'banner_image_positions'
        verbose_name = 'Banner Image Position'
        verbose_name_plural = 'Banner Image Positions'


class Gallery(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, unique=True)
    creation_date = models.DateField(auto_now_add=True, blank=True)
    last_edit_date = models.DateField(auto_now=True, blank=True)
    first_image = models.ImageField(
        upload_to="galleries_covers/", null=True, blank=True)
    second_image = models.ImageField(
        upload_to="galleries_covers/", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'galleries'
        verbose_name = 'Gallery'
        verbose_name_plural = 'Galleries'

    def first_image_admin(self):
        return str.format("<img src=/media/{0} alt = 'gallery first image', width = 100>", self.first_image)
    first_image_admin.allow_tags = True

    def second_image_admin(self):
        return str.format("<img src=/media/{0} alt = 'gallery second image', width = 100>", self.second_image)
    second_image_admin.allow_tags = True


class Banner(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, unique=True)
    creation_date = models.DateField(auto_now_add=True, blank=True)
    last_edit_date = models.DateField(auto_now=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'banners'
        verbose_name = 'Banner'
        verbose_name_plural = 'Banners'


class Banners:
    def __init__(self):
        self.banners = {}

    def append(self, banner_name, image_positions):
        self.banners[banner_name] = image_positions

    def __getitem__(self, item):
        return self.banners[item]
