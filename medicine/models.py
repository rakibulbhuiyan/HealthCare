from django.db import models

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    category = models.ForeignKey(Category, related_name="subcategories", on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)

    def __str__(self):
        return f"{self.name} (Sub of {self.category.name})"


class Medicine(models.Model):
    sub_category = models.ForeignKey(Subcategory, related_name='medicines', on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.IntegerField(default=1)

    def __str__(self):
        return self.name

    
class CartItem(models.Model):
    medicine=models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    added_at=models.DateTimeField(auto_now_add=True)

    def __self__(self):
        return f"{self.quantity} x {self.medicine.name}"

class Address(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    address_line = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    address_type = models.CharField(max_length=50, choices=[('Delivery', 'Delivery'), ('Billing', 'Billing')])

    def __str__(self):
        return f"{self.address_type} - {self.address_line}"

class Checkout(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    delivery_address = models.ForeignKey(Address, related_name='delivery_address', on_delete=models.SET_NULL, null=True)
    billing_address = models.ForeignKey(Address, related_name='billing_address', on_delete=models.SET_NULL, null=True)
    payment_method = models.CharField(max_length=50, choices=[('Bkash', 'Bkash'), ('Nagad', 'Nagad')])
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    coupon_voucher = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    order_summary = models.TextField()

    def __str__(self):
        return f"Order for {self.user.username} - Total: {self.total}"



# Diet Chart

class DietCategory(models.Model):
    name = models.CharField(max_length=100) 
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='diet_categories/')

    def __str__(self):
        return self.name

class DietPlan(models.Model):
    diet_category = models.ForeignKey(DietCategory, related_name='plans', on_delete=models.CASCADE)
    file_or_image = models.FileField(upload_to='diet_plans/')

    def __str__(self):
        return f"{self.file_or_image.name if self.file_or_image else 'No File'}"