from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "nickname", "phone_number", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    search_fields = ("email", "nickname", "phone_number")
    readonly_fields = ["is_staff",  ]

    # 상세 페이지에서 보여줄 필드 그룹
    fieldsets = (
        (None, {
            "fields": ("email", "password"),
        }),
        ("개인 정보", {
            "fields": ("nickname", "name", "phone_number"),
        }),
        ("권한", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
        }),
    )

    # 새 사용자 생성 폼
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "nickname",
                "name",
                "password1",
                "password2",
                "is_active",
                "is_staff",
            ),
        }),
    )
    ordering = ("email",)
