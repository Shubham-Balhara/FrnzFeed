from django.conf.urls import url 
from . import views


urlpatterns = [
	url(r'^$',views.index,name='index'),
	url(r'^signup/$',views.signup,name='signup'),
	url(r'^friends/(?P<pk>[0-9]+)/$',views.friends,name='friends'),
	url(r'^profile/(?P<pk>[0-9]+)/$',views.profile,name='profile'),
	url(r'^friends/profile/(?P<name>[a-zA-Z0-9]+)/',views.fprofile,name='f-profile'),
	url(r'^profile/(?P<user_id>[0-9]+)/add/$',views.add_profile,name='add-profile'),
	url(r'^profile/post/add/$',views.add_post,name='add-post'),
	url(r'^profile/(?P<pk>[0-9]+)/update/$',views.UpdateUserProfile.as_view(),name='update-profile'),
	url(r'^profile/(?P<pk>[0-9]+)/status/$',views.UpdateStatus.as_view(),name='status'),
	url(r'^friends/(?P<pk>[0-9]+)/sent/$',views.sent_friend,name='sent-friend'),
	url(r'^notification/$',views.notify,name='notification'),
	url(r'^notification/confirm/(?P<name>[a-zA-Z0-9]+)/$',views.confirm_yes,name='confirm-yes'),
	url(r'^notification/remove/(?P<name>[a-zA-Z0-9]+)/$',views.remove_yes,name='remove-yes'),
	url(r'^notification/confirm_no/(?P<name>[a-zA-Z0-9]+)/$',views.confirm_no,name='confirm-no'),
	url(r'^post/(?P<pk>[0-9]+)/like/$',views.like_yes,name='like-yes'),
	url(r'^chatroom/(?P<frnd>[a-zA-Z0-9]+)/$',views.chatroom,name='chatroom'),
	url(r'^post/(?P<pk>[0-9]+)/$',views.show_post,name='show_post'),
	url(r'^post/comment/(?P<pk>[0-9]+)/$',views.add_comment,name='add_comment'),
]