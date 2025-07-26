from django.contrib import admin
from .models import City, Township, YfCase

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Township)
class TownshipAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    list_filter = ('city',)
    search_fields = ('name', 'city__name')
    ordering = ('city__name', 'name')

@admin.register(YfCase)
class YfCaseAdmin(admin.ModelAdmin):
    list_display = ('yfcaseCaseNumber', 'yfcaseCompany', 'yfcaseCity', 'yfcaseTownship', 'yfcaseCaseStatus', 'user', 'yfcaseTimestamp')
    list_filter = ('yfcaseCaseStatus', 'yfcaseCity', 'yfcaseTownship', 'user', 'yfcaseTimestamp')
    search_fields = ('yfcaseCaseNumber', 'yfcaseCompany', 'yfcaseStreet', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('yfcaseTimestamp', 'yfcaseUpdated')
    date_hierarchy = 'yfcaseTimestamp'
    ordering = ('-yfcaseTimestamp',)
    
    fieldsets = (
        ('基本資訊', {
            'fields': ('yfcaseCaseNumber', 'yfcaseCompany', 'yfcaseCaseStatus', 'user')
        }),
        ('地址資訊', {
            'fields': ('yfcaseCity', 'yfcaseTownship')
        }),
        ('詳細地址', {
            'fields': ('yfcaseStreet', 'yfcaseSection', 'yfcaseLane', 'yfcaseAlley', 'yfcaseNumber', 'yfcaseFloor')
        }),
        ('其他資訊', {
            'fields': ('yfcaseBigSection', 'yfcaseSmallSection', 'yfcaseVillage', 'yfcaseNeighbor')
        }),
        ('時間資訊', {
            'fields': ('yfcaseTimestamp', 'yfcaseUpdated'),
            'classes': ('collapse',)
        }),
    )
