from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'userFullName', 'userWorkArea', 'userRole', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'userRole', 'userWorkArea')
    search_fields = ('email', 'username', 'userFullName', 'userFirstName', 'userLastName')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('基本資訊', {'fields': ('username', 'userFirstName', 'userLastName', 'userFullName', 'userWorkArea', 'userRole')}),
        ('個人資訊', {'fields': ('userIdentityCard', 'userBirthday', 'userLocalPhone', 'userMobilePhone', 'userPublicOrPrivate')}),
        ('地址資訊', {'fields': ('userCountry', 'userTownship', 'userVillage', 'userNeighbor', 'userStreet', 'userSection', 'userLane', 'userAlley', 'userNumber', 'userFloor')}),
        ('權限', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('重要日期', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'userFullName', 'userRole', 'is_staff', 'is_active'),
        }),
    )
