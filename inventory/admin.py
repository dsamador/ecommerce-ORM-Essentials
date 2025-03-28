from django.contrib import admin
from .models import (ProductImage, Category, 
                    AttributeValue, ProductType, 
                    Attribute, Product, ProductLine, 
                    SeasonalEvents, StockControl, Product_ProductType
                    )
# Register your models here.


""" models = [
    ProductImage, Category, AttributeValue, ProductType, 
    Attribute, Product, ProductLine, SeasonalEvents, 
    StockControl, Product_ProductType
]

for model in models:
    admin.site.register(model) """

class CategoryAdmin(admin.ModelAdmin):
  #prepopulated_fields = {"slug":("name",)}
  list_display  = ("id", "name", "slug")
  search_fields = ["name", "slug"]
  list_display_links = ("id",)
  list_editable = ("name",)

admin.site.register(Category, CategoryAdmin)

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
  list_display = ['id', 'name', 'parent']
  list_filter = ("name",)

class AttributeValueInLine(admin.StackedInline):
  model = AttributeValue
  extra = 1

class AttributeAdmin(admin.ModelAdmin):
  inlines = [AttributeValueInLine]

admin.site.register(Attribute, AttributeAdmin)