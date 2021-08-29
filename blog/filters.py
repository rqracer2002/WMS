import django_filters
from django import forms
from blog.models import Post, Comment, OrderHeader,OrderDetail,BinTransfer

class OrderHeaderFilter(django_filters.FilterSet):
    customer = django_filters.CharFilter(field_name="customer",lookup_expr='contains',label="Customer",widget=forms.TextInput(attrs={
            'placeholder': 'Search place', 'class': 'mx-0'}))
    ordnumber = django_filters.CharFilter(field_name="ordnumber",lookup_expr='contains',label="Customer")
    max_orderdate = django_filters.NumberFilter(field_name="orderdate",lookup_expr='lte',label="Date LTE")
    min_orderdate = django_filters.NumberFilter(field_name="orderdate",lookup_expr='gte',label="Date GTE")
    # orderdate__gt = django_filters.NumberFilter(lookup_expr='gt',label="Date GTE")

    class Meta:
        model = OrderHeader
        fields = {
            # 'customer': ['contains'],
            # 'orderdate': ['lte','gte'],
        }
        # customer = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control-sm','placeholder':"Another input"}))
