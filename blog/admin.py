from django.contrib import admin

from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin
from import_export.resources import ModelResource

from .models import Post, Comment, OrderHeader, OrderDetail,BinTransfer,MyModel,CustomUser,AdjustmentLine

from import_export import resources
from import_export.admin import ImportExportActionModelAdmin

from import_export.admin import ExportActionMixin,ImportExportModelAdmin

from django.contrib.admin import SimpleListFilter
from django.contrib.auth.models import User

class OrderHeaderFilter(SimpleListFilter):
    """
    This filter is being used in django admin panel in profile model.
    """
    title = 'Customer Filter'
    parameter_name = 'orderheaader__customer'

    def lookups(self, request, model_admin):
        return (
            ('business', 'Business'),
            ('non_business', 'non-business')
        )


    def queryset(self, request, queryset):
        user = User.objects.get(username=request.user)

        if user.groups.filter(name='accounting').exists():
            return queryset

        else:

            return queryset.filter(customer=user.customuser.customer)





class OrderHeaderResource(resources.ModelResource):

    class Meta:
        model = OrderHeader


class OrderHeaderAdmin(ImportExportModelAdmin):
    resource_class = OrderHeaderResource
    list_filter = (OrderHeaderFilter,)



admin.site.register(OrderHeader, OrderHeaderAdmin)

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(CustomUser)
admin.site.register(OrderDetail)
admin.site.register(BinTransfer)
admin.site.register(MyModel)
admin.site.register(AdjustmentLine)
