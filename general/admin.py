from django.contrib import admin
from django.contrib.auth.models import Group
from django_admin_listfilter_dropdown.filters import ChoiceDropdownFilter
from rangefilter.filters import DateRangeFilter

from general.filters import AuthorFilter, PostFilter
from general.models import Comment, Post, Reaction, User

admin.site.unregister(Group)

@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "username",
        "email",
        "is_staff",
        "is_superuser",
        "is_active",
        "date_joined",
    )

    readonly_fields = (
    "date_joined",
    "last_login",
)
    fieldsets = (
    (
        "Личные данные", {
            "fields": (
                "first_name",
                "last_name",
                "email",
            )
        }
    ),
    (
        "Учетные данные", {
            "fields": (
                "username",
                "password",
            )
        }
    ),
    (
        "Статусы", {
            
            "fields": (
                "is_staff",
                "is_superuser",
                "is_active",
            )
        }
    ),
    (
        None, {
            "fields": (
                "friends",
            )
        }
    ),
    (
        "Даты", {
            "fields": (
                "date_joined",
                "last_login",
            )
        }
    )

)
    search_fields = (
    "id",
    "username",
    "email",
)
    list_filter = (
    "is_staff",
    "is_superuser",
    "is_active",
    ("date_joined", DateRangeFilter),
)
    

@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "title",
        "get_body",
        "created_at",
        "get_comment_count",
    )
    readonly_fields = (
        "created_at",
    )
    def get_body(self, obj):
        max_length = 64
        if len(obj.body) > max_length:
            return obj.body[:61] + "..."
        return obj.body

    get_body.short_description = "body"
    
    def get_comment_count(self, obj):
        return obj.comments.count()
    get_comment_count.short_description = "comment count"
 
    search_fields = (
    "id",
    "title",
)    
    list_filter = (
        ("created_at", DateRangeFilter),
        AuthorFilter,
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("comments")
    



@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "post",
        "body",
        "created_at",
    )
    list_display_links = (
        "id",
        "body",
        "author"
    )
    search_fields = (
)
    list_filter = (
        PostFilter,
        AuthorFilter,
    )
    raw_id_fields = (
    "author",
)
    


@admin.register(Reaction)
class ReactionModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "post",
        "value",
    )
    list_filter = (
    PostFilter,
    AuthorFilter,
    ("value",ChoiceDropdownFilter),
)
    autocomplete_fields = (
    "author",
    "post",
)
    

