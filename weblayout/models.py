from django.db import models

# MPTT Modes and trees
from mptt.models import MPTTModel, TreeForeignKey

# CKeditor support
from ckeditor.fields import RichTextField


class Language(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    short_name = models.CharField(max_length=2)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class MainMenuItemData(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey("MainMenu")
    language = models.ForeignKey(Language)
    url = models.CharField(max_length=256, default=None, null=True, blank=True)
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class ExtraMenuItemData(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey("ExtraMenu")
    language = models.ForeignKey(Language)
    url = models.CharField(max_length=256, default=None, null=True, blank=True)
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class AdditionalMenuItemData(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey("AdditionalMenu")
    language = models.ForeignKey(Language)
    url = models.CharField(max_length=256, default=None, null=True, blank=True)
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Template(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, unique=True)
    path = models.CharField(max_length=256, unique=True)
    creation_date = models.DateField(auto_now_add=True, blank=True)
    last_edit_date = models.DateField(auto_now=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'templates'
        verbose_name = 'Template'
        verbose_name_plural = 'Templates'


class MainMenu(MPTTModel):
    URL_TYPES = (
        ('splitter', 'None'),
        ('static_page', 'Static Page'),
        ('category', 'Category'),
        ('product', 'Product'),
        ('pre_filter', 'PreFilter'),
        ('custom', 'External Link')
    )
    id = models.AutoField(primary_key=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', )
    url_type = models.CharField(max_length=256, choices=URL_TYPES)

    first_image = models.ImageField(
        upload_to="main_menu/", null=True, blank=True)
    second_image = models.ImageField(
        upload_to="main_menu/", null=True, blank=True)

    def __data(self) -> [MainMenuItemData]:
        return MainMenuItemData.objects.filter(item=self).all()

    def __str__(self):
        data = MainMenuItemData.objects.filter(item=self).first()
        return data.__str__()

    def get_url(self) -> [str]:
        data = self.__data()
        urls = {}
        for item in data:
            if self.url_type == 'splitter':
                pass
            elif self.url_type == 'static_page':
                urls[item.language.short_name] = str.format('/{0}', item.url)
            elif self.url_type == 'category':
                urls[item.language.short_name] = str.format('/catalogue/{0}', item.url)
            elif self.url_type == 'product':
                urls[item.language.short_name] = str.format('/product/{0}', item.url)
            elif self.url_type == 'pre_filter':
                urls[item.language.short_name] = str.format('/catalogue/{0}', item.url)
            elif self.url_type == 'custom':
                urls[item.language.short_name] = item.url
        return urls

    def get_name(self) -> [str]:
        data = self.__data()
        names = {}
        for item in data:
            names[item.language.short_name] = item.name
        return names


    class MPTTMeta:
        order_insertion_by = ['url_type']

    class Meta:
        db_table = 'main_menu'
        verbose_name = 'Main Menu Element'
        verbose_name_plural = 'Main Menu'


class ExtraMenu(MPTTModel):
    URL_TYPES = (
        ('splitter', 'None'),
        ('static_page', 'Static Page'),
        ('category', 'Category'),
        ('product', 'Product'),
        ('pre_filter', 'PreFilter'),
        ('custom', 'External Link')
    )
    id = models.AutoField(primary_key=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', )
    url_type = models.CharField(max_length=256, choices=URL_TYPES)
    first_image = models.ImageField(
        upload_to="extra_menu/", null=True, blank=True)
    second_image = models.ImageField(
        upload_to="extra_menu/", null=True, blank=True)

    def __data(self) -> [ExtraMenuItemData]:
        return ExtraMenuItemData.objects.filter(item=self).all()

    def __str__(self):
        data = ExtraMenuItemData.objects.filter(item=self).first()
        return data.__str__()

    def get_url(self) -> [str]:
        data = self.__data()
        urls = {}
        for item in data:
            if self.url_type == 'splitter':
                pass
            elif self.url_type == 'static_page':
                urls[item.language.short_name] = str.format('/{0}', item.url)
            elif self.url_type == 'category':
                urls[item.language.short_name] = str.format('/catalogue/{0}', item.url)
            elif self.url_type == 'product':
                urls[item.language.short_name] = str.format('/product/{0}', item.url)
            elif self.url_type == 'pre_filter':
                urls[item.language.short_name] = str.format('/catalogue/{0}', item.url)
            elif self.url_type == 'custom':
                urls[item.language.short_name] = item.url
        return urls

    def get_name(self) -> [str]:
        data = self.__data()
        names = {}
        for item in data:
            names[item.language.short_name] = item.name
        return names

    class MPTTMeta:
        order_insertion_by = ['url_type']

    class Meta:
        db_table = 'extra_menu'
        verbose_name = 'Extra Menu Element'
        verbose_name_plural = 'Extra Menu'


class AdditionalMenu(MPTTModel):
    URL_TYPES = (
        ('splitter', 'None'),
        ('static_page', 'Static Page'),
        ('category', 'Category'),
        ('product', 'Product'),
        ('pre_filter', 'PreFilter'),
        ('custom', 'External Link')
    )
    id = models.AutoField(primary_key=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    url_type = models.CharField(max_length=256, choices=URL_TYPES)
    first_image = models.ImageField(
        upload_to="additional_menu/", null=True, blank=True)
    second_image = models.ImageField(
        upload_to="additional_menu/", null=True, blank=True)

    def __data(self) -> [AdditionalMenuItemData]:
        return AdditionalMenuItemData.objects.filter(item=self).all()

    def __str__(self):
        data = AdditionalMenuItemData.objects.filter(item=self).first()
        return data.__str__()

    def get_url(self) -> [str]:
        data = self.__data()
        urls = {}
        for item in data:
            if self.url_type == 'splitter':
                pass
            elif self.url_type == 'static_page':
                urls[item.language.short_name] = str.format('/{0}', item.url)
            elif self.url_type == 'category':
                urls[item.language.short_name] = str.format('/catalogue/{0}', item.url)
            elif self.url_type == 'product':
                urls[item.language.short_name] = str.format('/product/{0}', item.url)
            elif self.url_type == 'pre_filter':
                urls[item.language.short_name] = str.format('/catalogue/{0}', item.url)
            elif self.url_type == 'custom':
                urls[item.language.short_name] = item.url
        return urls

    def get_name(self) -> [str]:
        data = self.__data()
        names = {}
        for item in data:
            names[item.language.short_name] = item.name
        return names

    class MPTTMeta:
        order_insertion_by = ['url_type']

    class Meta:
        db_table = 'additional_menu'
        verbose_name = 'Additional Menu Element'
        verbose_name_plural = 'Additional Menu'


class SystemElement(models.Model):
    ELEMENT_TYPE = (
        ('Header', 'Header'),
        ('Footer', 'Footer'),
        ('Script', 'Script')
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16, choices=ELEMENT_TYPE, unique=True)
    body = RichTextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'system_elements'
        verbose_name = 'System Element'
        verbose_name_plural = 'System Elements'