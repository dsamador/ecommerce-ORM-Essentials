from django.db import models
import uuid
from django.utils.text import slugify

#python manage.py makemigrations: Sirve para hacer el archivo que pasara a ser SQL
#python manage.py migrate: para hacer la migracion a la base de datos
#python manage.py showmigrations --list: para ver las migraciones listadas, las que tienen X estan hechas
#python manage.py migrate inventory 002_xxxx: sirve para hacer rollback a una migracion especifica
#python manage.py createsuperuser: sirve para hacer el super user
#  

# Create your models here.
class Category(models.Model):
  name      = models.CharField(max_length=100, 
                               unique=True, 
                               verbose_name="First Name", 
                               help_text="Enter a category")
  slug      = models.SlugField(unique=True, null=True, blank=True)
  is_active = models.BooleanField(default=False)
  parent = models.ForeignKey('self', on_delete=models.PROTECT)

  class Meta:
    verbose_name = "Inventory Category"
    verbose_name_plural = "Categories"

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.name)
      super().save(*args, **kwargs)    

  def __str__(self):
    return self.name
  

class ProductType(models.Model):
  name   = models.CharField(max_length=100)
  parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

class Product(models.Model):

  IN_STOCK     = "IS"
  OUT_OF_STOCK = "OOS"
  BACKORDERED  = "BO"

  STOCK_STATUS = {
    IN_STOCK: "In Stock",
    OUT_OF_STOCK: "Out of Stock",
    BACKORDERED: "Backordered"
  }

  pid          = models.CharField(max_length=255, null=False, blank=False)
  name         = models.CharField(max_length=255, unique=True)
  slug         = models.SlugField(unique=True)
  description  = models.TextField(null=True)
  id_digital   = models.BooleanField(default=False)
  created_at   = models.DateTimeField(auto_now_add=True, editable=False)
  updated_at   = models.DateTimeField(auto_now=True, editable=False)
  is_active    = models.BooleanField(default=False)
  stock_status = models.CharField(max_length=3, 
                                 choices=STOCK_STATUS, 
                                 default=OUT_OF_STOCK)
  category       = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
  seasonal_event = models.ForeignKey("SeasonalEvents", on_delete=models.SET_NULL, null=True, blank=True)
  product_type   = models.ManyToManyField(ProductType, related_name="product_type") 

class Attribute(models.Model):
  name        = models.CharField(max_length=100)
  description = models.TextField(null=True)

class AttributeValue(models.Model):
  attribute_value = models.CharField(max_length=100)
  attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, null=True, blank=True)

class ProductLine(models.Model):
  price     = models.DecimalField(decimal_places=2, max_digits=10)
  sku       = models.UUIDField(default=uuid.uuid4)
  stock_qty = models.IntegerField(default=0)
  is_active = models.BooleanField(default=False)
  order     = models.IntegerField()
  weight    = models.FloatField()
  product   = models.ForeignKey(Product, on_delete=models.PROTECT)
  attribute_values = models.ManyToManyField(Attribute, related_name="attribute_values")

class ProductImage(models.Model):
  name             = models.CharField(max_length=100)
  alternative_text = models.CharField(max_length=100)
  url              = models.ImageField()
  order            = models.IntegerField()
  product_line     = models.ForeignKey(ProductLine, on_delete=models.CASCADE)

class SeasonalEvents(models.Model):
  start_date = models.DateTimeField()
  end_date   = models.DateTimeField()
  name       = models.CharField(max_length=100, unique=True)

class ProductLine_AttributeValue(models.Model):
  attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)
  product_line    = models.ForeignKey(ProductLine, on_delete=models.CASCADE)

class Product_ProductType(models.Model):
  product      = models.ForeignKey(Product, on_delete=models.CASCADE)
  product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)

class StockControl(models.Model):
  stock_qty     = models.IntegerField()
  name          = models.CharField(max_length=100)
  stock_product = models.OneToOneField(Product, on_delete=models.CASCADE)