from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from uuid import uuid4


# Model for product details
class Product(models.Model):
    product_name = models.CharField(max_length=999)  # Product name
    brand = models.CharField(max_length=999, default='')  # Brand of the product
    available_quantity = models.IntegerField(default=0)  # Total available stock for the product
    
    def __str__(self):
        # Representación en cadena del producto con su nombre y marca
        return f'{self.product_name} ({self.brand})'
    
    def save(self, *args, **kwargs):
        # Verificar si ya existe un producto con el mismo nombre y marca (excluyendo el actual si está siendo editado)
        if Product.objects.filter(product_name=self.product_name, brand=self.brand).exclude(pk=self.pk).exists():
            # Lanzar una excepción si ya existe el producto con ese nombre y marca
            raise ValidationError(f'Ya existe un producto con el nombre "{self.product_name}" y la marca "{self.brand}".')
        
        # Si no hay duplicados, guardar el producto normalmente
        super().save(*args, **kwargs)

    # Update the available quantity based on total product entries
    def update_available_quantity(self):
        # Sum all the quantities from related product entries
        self.available_quantity = sum(entry.entered_amount for entry in self.product_entries.all())
        self.save()

# Model for product entries (for tracking lot quantities and prices)
class ProductEntry(models.Model):
    product = models.ForeignKey(Product, related_name='product_entries', on_delete=models.CASCADE)  # Reference to the product
    entered_amount = models.IntegerField()  # Quantity of product entered in this batch
    entry_price = models.DecimalField(max_digits=10, decimal_places=2)  # Price per unit in this batch
    entry_date = models.DateField(default=timezone.now)  # Date of product entry

    class Meta:
        get_latest_by = 'entry_date'  # Añadir esta línea
    
    def __str__(self):
        return f'Entry for {self.product.product_name} on {self.entry_date}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.update_available_quantity()  # Update stock when new entry is saved

# Model for product sales
class Sale(models.Model):
    sale_id = models.UUIDField(default=uuid4, editable=False, unique=True)  # ID único para cada venta
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link sale to a product
    quantity_sold = models.PositiveIntegerField()  # Quantity sold
    sale_date = models.DateTimeField(default=timezone.now)  # Date of the sale
    
    def total_sale(self):
        # Use the product's current price, assuming price consistency
        return self.product.selling_price * self.quantity_sold

    # Reduce available stock after sale
    def save(self, *args, **kwargs):
        if self.quantity_sold > self.product.available_quantity:
            raise ValueError("Cannot sell more than available quantity")
        super().save(*args, **kwargs)
        self.product.available_quantity -= self.quantity_sold
        self.product.save()

    def short_sale_id(self):
        return str(self.sale_id)[:7]

class Customer(models.Model):
    firstname = models.CharField(max_length=255)  # Nombre del cliente
    lastname = models.CharField(max_length=255)  # Apellido del cliente
    email = models.EmailField()  # Correo del cliente
    phone = models.CharField(max_length=20)  # Teléfono del cliente
    address = models.CharField(max_length=500)  # Dirección del cliente
    id_or_nit = models.CharField(max_length=20, unique=True)  # CC o NIT (identificación única)
    city = models.CharField(max_length=255)  # Ciudad del cliente

    def __str__(self):
        return f'{self.firstname} {self.lastname} - {self.id_or_nit}'


# Modelo para la factura
class Invoice(models.Model):
    company_name = models.CharField(max_length=100, default="torresytorres")
    city = models.CharField(max_length=100, default="Popayán - Cauca")
    nit = models.CharField(max_length=15, default="9999999999")
    address = models.CharField(max_length=200, default="calle 8 99 99 barrio Bello Horizonte")
    phone = models.CharField(max_length=15, default="3143143144")
    email = models.EmailField(default="torresytorres@gmail.com")
    invoice_id = models.AutoField(primary_key=True)
    issue_date = models.DateTimeField(default=timezone.now)
    items = models.ManyToManyField(Sale)  # Relacionas la factura con las ventas
    due_date = models.DateTimeField(default=timezone.now() + timedelta(days=15))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[('Cash', 'Efectivo'), ('Transaction', 'Transacción')])

    def __str__(self):
        return f"Invoice {self.invoice_id}"

# Modelo para los detalles de la factura (productos en la factura)
class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='invoice_items')
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=200)
    description = models.TextField()
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Item {self.product_name} for Invoice {self.invoice.invoice_id}"
