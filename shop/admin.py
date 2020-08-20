from django.contrib import admin
from . models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(ItemDetails)
admin.site.register(OrderItem)

class ItemImagesInline(admin.TabularInline):
  model = ItemImages
  extra = 3

class ItemDetailsInline(admin.TabularInline):
  model = ItemDetails
  extra = 1
class ItemsAdmin(admin.ModelAdmin):
  inlines = [
    ItemImagesInline,
    ItemDetailsInline,
  ]

admin.site.register(Items, ItemsAdmin)
admin.site.register(ItemImages)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(OwnerInfo)
admin.site.register(CattleInfo)
admin.site.register(MonthlyPackage)

