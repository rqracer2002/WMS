from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views



urlpatterns = [
    url(r'^polls/(?P<pk>\d+)$',views.get_img, name="polls"),
    url(r'^$',views.home_view,name='home'),
    url(r'^mymodelform/(?P<pk>\d+)$', views.MyModelFormView.as_view(), name='mymodelform'),
    url(r'^orders/$',views.OrderHeaderListView.as_view(),name='orderheader_list'),
    url(r'^about/$',views.AboutView.as_view(),name='about'),
    url(r'^post/(?P<pk>\d+)$', views.PostDetailView.as_view(), name='post_detail'),
    url(r'^order_details/(?P<pk>\d+)$', views.OrderHeaderDetailView.as_view(), name='orderheader_detail'),
    url(r'^orderdetail_detail/(?P<pk>\d+)$', views.OrderPickingDetailView.as_view(), name='orderdetail_detail'),
    url(r'^post/new/$', views.CreatePostView.as_view(), name='post_new'),
    url(r'^orderdetail/new/$', views.CreateOrderDetailView.as_view(), name='orderdetail_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.PostUpdateView.as_view(), name='post_edit'),
    url(r'^drafts/$', views.DraftListView.as_view(), name='post_draft_list'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.PostDeleteView.as_view(), name='post_remove'),
    url(r'^post/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish'),
    # url(r'^orderdetail_detail/(?P<pk>\d+)/bintransfer_publish/$', views.bintransfer_publish, name='bintransfer_publish'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
    url(r'^filedownload/(?P<pk>\d+)$', views.FileDownloadView, name='file_download'),
    url(r'^buildadjustment/$', views.BuildAdjustmentPageView.as_view(), name='adjustment_line'),
]

urlpatterns+=staticfiles_urlpatterns()
