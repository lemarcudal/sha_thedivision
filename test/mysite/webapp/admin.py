from django.contrib import admin
from webapp.models import Post
from .forms import PostForm
# Register your models here.
# new code below------------
class webappAdmin(admin.ModelAdmin):
	list_display = ["title","timestamp", "updated"]
	list_filter = ["updated", "timestamp"]
	search_fields = ["title", "guide", "IGN"]
	form = PostForm

admin.site.register(Post, webappAdmin)

