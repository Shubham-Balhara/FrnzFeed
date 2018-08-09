from django.contrib import admin
from .models import UserProfile, Post, Friend, Rqst, Like, Clients, Messages, Comments

admin.site.register(UserProfile)
admin.site.register(Post,
	list_display = ['quote','likes','date'],
	)
admin.site.register(Friend,
	list_display = ['name']
	)
admin.site.register(Rqst,
	list_display=['sender','receiver'],
	)
admin.site.register(
	Like,
	list_display=['post','user_id'],
	)
admin.site.register(
	Clients,
	list_display=['name','ch_name'],
	)
admin.site.register(
	Messages,
	list_display = ['to','frm','message']
	)
admin.site.register(
	Comments,
	list_display = ['comment']
	)