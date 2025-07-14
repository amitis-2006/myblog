from django.contrib import admin
from . models import Post
from . models import Profile
from django.contrib.admin.sites import AdminSite
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'published', 'slug', 'view_count')
    list_filter = ('status','published', 'author','content')
    search_fields = ('title' , 'content')
    prepopulated_fields = {'slug':('title',)}
    list_editable = ('status',)
    exclude = ('author',)
    date_hierarchy = 'published'
    ordering = ('published','status')
    list_display_links = ('slug',)
    #actions = ['publish_posts']
    class Media:
        css = {
            'all': ('css/admin_mobile_fix.css',)
        }

    def publish_posts(self, request, queryset):
        update= queryset.update(status=Post.Status.PUBLISHED)
        self.message_user(request, f'{update} published')
    publish_posts.short_description= 'Approval and publication'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        if not change or not obj.author_id:
            obj.author = request.user
        obj.save()

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.author != request.user:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.author != request.user:
            return False
        return True

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','address','phone','full_name')
    search_fields = ('user__username','full_name','phone')
    class Media:
        css = {
            'all': ('css/admin_mobile_fix.css',)
        }


class MyAdminSite(admin.AdminSite):
    class Media:
        css = {
            'all': ('css/admin_mobile_fix.css',)
        }
