import os
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from blog.models import Post, Comment, OrderHeader,OrderDetail,BinTransfer,MyModel
from django.utils import timezone
from blog.forms import PostForm, CommentForm, OrderPickingForm,UploadFileForm,MyModelForm
from django.views.generic.edit import FormMixin
from .filters import OrderHeaderFilter
import django_filters
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView,FormView)

from django.urls import reverse_lazy,reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django import forms
from .myscripts import myname, myvalidator
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.views import generic
from sortable_listview import SortableListView




class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm

    model = Post

class CreateOrderDetailView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/orderheader_list.html'
    form_class = OrderPickingForm




    model = BinTransfer


class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm

    model = Post


class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'

    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

class OrderHeaderFilter(django_filters.FilterSet):
    customer = django_filters.CharFilter(field_name="customer",lookup_expr='contains',label="Customer",widget=forms.TextInput(attrs={
            'placeholder': 'Customer', 'class': 'form-control-sm'}))
    ordnumber = django_filters.CharFilter(field_name="ordnumber",lookup_expr='contains',label="Order Number",widget=forms.TextInput(attrs={
            'placeholder': 'Order Number', 'class': 'form-control-sm'}))
    max_orderdate = django_filters.NumberFilter(field_name="orderdate",lookup_expr='gte',label="Date GTE",widget=forms.TextInput(attrs={
            'placeholder': 'Min Order Date', 'class': 'form-control-sm'}))
    min_orderdate = django_filters.NumberFilter(field_name="orderdate",lookup_expr='lte',label="Date LTE",widget=forms.TextInput(attrs={
            'placeholder': 'Max Order Date', 'class': 'form-control-sm'}))
    # orderdate__gt = django_filters.NumberFilter(lookup_expr='gt',label="Date GTE")
    class Meta:
        model = OrderHeader
        fields = {
            # 'customer': ['contains'],
            # 'orderdate': ['lte','gte'],
        }

class OrderHeaderListView(LoginRequiredMixin,SortableListView):
    paginate_by = 150
    template_name = 'orderheader_list.html'
    model = OrderHeader
    login_url = 'accounts/login/'




    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     filter = OrderHeaderFilter(self.request.GET, queryset)
    #     return filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        filter = OrderHeaderFilter(self.request.GET, queryset)
        # MyModel = MyModel
        context["filter"] = filter
        context['mymodel'] = MyModel.objects.all()
        return context

    # def dispatch(self, request, *args, **kwargs):
    #     global orderheaderid
    #     # self.request._body = 'My Name is Rafael'
    #     print(self.request.path_info)
    #     print(self.request.method)
    #     print(self.request.encoding)
    #     print(self.request.body)
    #     orderheaderid = self.request.path_info.split("/", 1)
    #     print(type(int(orderheaderid[2])))
    #     return super(OrderHeaderDetailView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        descending = OrderHeaderFilter(self.request.GET, queryset=queryset).qs
        return descending.order_by('-orderdate')
        # return OrderHeader.objects.filter(orderdate__lte=20210831).order_by('-orderdate')




class OrderHeaderDetailView(LoginRequiredMixin,FormMixin,DetailView):
    model = OrderDetail
    form_class = OrderPickingForm
    login_url = '/login/'
    redirect_field_name = 'blog/orderheader_detail.html'


    def dispatch(self, request, *args, **kwargs):
        global orderheaderid
        # self.request._body = 'My Name is Rafael'
        print(self.request.path_info)
        print(self.request.method)
        print(self.request.encoding)
        print(self.request.body)
        orderheaderid = self.request.path_info.split("/", 2)
        print(type(int(orderheaderid[2])))
        return super(OrderHeaderDetailView, self).dispatch(request, *args, **kwargs)

    def post(self,request, *args, **kwargs):
        form = OrderPickingForm(request.POST)
        if form.is_valid():
            form.save()
            print(self.kwargs.get('pk')+"is the pk in post request")
     # //return whatever you want to show on successful form submission
        else:
            print("do not save")
     # //return bound form as html with errors
        return HttpResponseRedirect(reverse('orderheader_detail',args=[self.kwargs.get('pk')]))




    template_name = 'orderheader_detail.html'

    def get_object(self, queryset=None):
        print(self.kwargs.get('pk')+"is the pk in get object")
        return get_object_or_404(OrderHeader, pk=self.kwargs.get('pk'))

    def get_queryset(self):
        # OrderDetail = OrderDetail.object.get(pk)
        # OrderDetail1 = get_object_or_404(OrderHeader, pk=pk)
        print(self.kwargs.get('pk')+"is the pk in get queryset")
        return OrderDetail.objects.filter(orderheader_id = self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
    # Add in the publisher
        # print(self.get_queryset())
        print(self.kwargs.get('pk')+"is the pk in get context data")
        context['details'] = self.get_queryset()
        return context


class OrderPickingDetailView(LoginRequiredMixin,FormMixin,DetailView):
    model = OrderDetail
    form_class = OrderPickingForm


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


class MyModelFormView(LoginRequiredMixin,FormView):
    # specify the Form you want to use

    form_class = MyModelForm
    # def get_queryset(self):
    #     return OrderDetail.objects.all()

    template_name = "mymodel_form.html"
    success_url = '/about/'

    # def post(self,request, *args, **kwargs):
    #     print("HELLO")
    #     form = MyModelForm(request.POST)
    #     if myvalidator(self.kwargs.get('pk')) == "valid":
    #         if form.is_valid():
    #             form.save()
    #             print(self.kwargs.get('pk')+"is the pk in post request")
    #      # //return whatever you want to show on successful form submission
    #         else:
    #             print("do not save")
    #     else:
    #         print("This order already has a POD attached.")
    #  # //return bound form as html with errors
    #     return HttpResponseRedirect(reverse('orderheader_detail',args=[self.kwargs.get('pk')]))




    # def get(self,request, *args, **kwargs):
    #     orderheader = OrderHeader()
    #     print(orderheader)





    def post(self,request, *args, **kwargs):
        form = MyModelForm(request.POST,request.FILES)
        print(self.kwargs.get('pk'))
        if myvalidator(self.kwargs.get('pk')) == "valid":
            if form.is_valid():
                instance = form.save(commit=False)

                instance.orderheader_id = self.kwargs.get('pk')
                myname(instance.orderheader_id)
                instance.save()
                return HttpResponseRedirect(reverse('orderheader_list'))
                # print(self.kwargs.get('pk')+"is the pk in post request")
         # //return whatever you want to show on successful form submission
            else:
                print("do not save")
        else:
            print("This order already has a POD attached.")
            return HttpResponseRedirect(reverse('orderheader_list'))
     # //return bound form as html with errors

@login_required
def get_img(request, pk):
    path = settings.MEDIA_ROOT
    mymodel = get_object_or_404(MyModel, orderheader_id=pk)
    print(mymodel.upload)
    img_list = os.listdir(path + "/media")
    print(img_list[0])
    base_image = "http://192.168.1.147:8000/blog/" + str(mymodel.upload)
    content = {"base_image": str(mymodel.upload), "ord_head_pk": pk}
    return render(request, 'get_img.html', content)

@login_required
def FileDownloadView(request, pk):
    upload_object = get_object_or_404(MyModel, orderheader_id=pk)
    # upload_object = MyModel.objects.get(id=pk)
    upload_file = upload_object.upload
    fsock = open('blog/static/blog/'+str(upload_file), 'rb')
    response = HttpResponse(fsock, content_type='image/jpeg')
    response['Content-Disposition'] = "attachment; %s.jpg" % \
                                     (upload_object.upload)
    return response


#######################################
## Functions that require a pk match ##
#######################################

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

# @login_required
# def bintransfer_publish(request):
#     bintransfer = get_object_or_404(BinTransfer)
#     if request.method == "POST":
#         form = OrderPickingForm(request.POST)
#
#         # form = OrderPickingForm(request.POST)
#         # bintransfer = form.save(commit=False)
#         bintransfer.save()
#     else:
#         form = OrderPickingForm()
#     return render(request, 'blog/orderheader_list.html', {'form': form})

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)
@login_required
def home_view(request):


    return redirect('orderheader_list')
