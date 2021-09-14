from django.db import models
from django.utils import timezone
from django.urls import reverse
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
# from django.conf import settings

from django.contrib.auth.models import AbstractUser

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.base_user import BaseUserManager


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer = models.CharField(max_length=100)
    REQUIRED_FIELDS = []
















class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk})


    def __str__(self):
        return self.title



class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments',on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return self.text

class OrderHeader(models.Model):
    orduniq = models.DecimalField(max_digits=19, decimal_places=0)
    ordnumber = models.CharField(max_length=22, unique=True)
    customer = models.CharField(max_length=12)
    orderdate = models.DecimalField(max_digits=9, decimal_places=0)
    expirydate = models.DecimalField(max_digits=9, decimal_places=0)
    pod = models.CharField(max_length=10,default = '',blank = True)
    submit = models.CharField(max_length=10,default = 'Submit',blank = True)

    def __str__(self):
        return self.customer+" "+self.ordnumber


    # def commitquantity(self):
    #     self.committedquantity = timezone.now()
    #     self.save()

    # def approve_comments(self):
    #     return self.comments.filter(approved_comment=True)
    #
    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk})


    # def __str__(self):
    #     return self.ordnumber

class OrderDetail(models.Model):
    orderheader = models.ForeignKey('blog.OrderHeader', related_name='orderdetail',on_delete=models.CASCADE)
    linenumber = models.IntegerField()
    itemnumber = models.CharField(max_length=24)
    orderedquantity = models.DecimalField(max_digits=19, decimal_places=4)
    committedquantity = models.DecimalField(max_digits=19, decimal_places=4)

    # def commitquantity(self):
    #     self.committedquantity = timezone.now()
    #     self.save()

    def get_absolute_url(self):
        return reverse("orderheader_list")

    # def __str__(self):
    #     return self.orderheader

class BinTransfer(models.Model):
    time = models.DecimalField(max_digits=9, decimal_places=0, default = 0,blank = True)
    srctype = models.IntegerField( default = 0,blank = True)
    doctype = models.IntegerField( default = 0,blank = True)
    srcloc = models.CharField(max_length=6, default = '',blank = True)
    destloc = models.CharField(max_length=6, default = '',blank = True)
    srcbin = models.CharField(max_length=10, default = '',blank = True)
    destbin = models.CharField(max_length=10, default = '',blank = True)
    quantitytran = models.DecimalField(max_digits=19, decimal_places=4,blank = True)
    comment = models.CharField(max_length=250, default = '',blank = True)
    itemno = models.CharField(max_length=24, default = '',blank = True)
    itemdesc = models.CharField(max_length=60, default = '',blank = True)



    def publish(self):
        # self.committedquantity = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse("orderheader_list")

    # def __str__(self):
    #     return self.orderheader

class MyModel(models.Model):
    # file will be uploaded to MEDIA_ROOT/uploads
    orderheader = models.ForeignKey('blog.OrderHeader', related_name='mymodel',on_delete=models.CASCADE,default=00000,null=True)
    upload = models.FileField(upload_to='media/')

    class meta:
        permissions = (
        ("can_add_data","can add a new data"),
        )


    def save(self):
        # Opening the uploaded image
        im = Image.open(self.upload)

        output = BytesIO()

        # Resize/modify the image
        im = im.resize((1008,756))

        # after modifications, save it to the output
        im.save(output, format='JPEG', quality=100)
        output.seek(0)

        # change the imagefield value to be the newley modifed image value
        self.upload = InMemoryUploadedFile(output, 'FileField', "%s.jpg" % self.upload.name.split('.')[0], 'image/jpeg',
                                        sys.getsizeof(output), None)

        super(MyModel, self).save()

# ct = ContentType.objects.get_for_model(MyModel)
# permission1 = Permission.objects.create(
# codename='can_view_MyModel',
# name='View MyModel',
# content_type=ct,)


# class UsersAdmin(admin.ModelAdmin):
#     rafael = User.objects.get(username='rafael')
#
#     rafael.user_permissions.add(1)
#
#     rafael.save()

class AdjustmentLine(models.Model):
    reserved_sku = models.CharField(max_length=30,default = '',blank = True)
    reserved_desc = models.CharField(max_length=30,default = '',blank = True)
    reserved_quant = models.CharField(max_length=9)
    optima_sku = models.CharField(max_length=30,default = '',blank = True)
    optima_desc = models.CharField(max_length=30,default = '',blank = True)
    optima_quant = models.DecimalField(max_digits=9, decimal_places=0)
    in_transit_quant = models.DecimalField(max_digits=9, decimal_places=0)
    transfer_quant = models.DecimalField(max_digits=9, decimal_places=0,blank = True)

    def __str__(self):
        return self.reserved_sku+"-&-"+self.optima_sku
