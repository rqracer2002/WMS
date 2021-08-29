from django.db import models
from django.utils import timezone
from django.urls import reverse


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
