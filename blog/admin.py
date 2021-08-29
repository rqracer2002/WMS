from django.contrib import admin

from .models import Post, Comment, OrderHeader, OrderDetail,BinTransfer,MyModel


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(OrderHeader)
admin.site.register(OrderDetail)
admin.site.register(BinTransfer)
admin.site.register(MyModel)
