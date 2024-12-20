from django import forms
from .models import Product, ProductEntry, Customer, Sale, Product, Invoice, InvoiceItem
from django.core.exceptions import ValidationError

# Form for creating or editing products
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'brand']  # Only the product name and brand will be added manually
        
        labels = {
            'product_name': 'Nombre del Producto',
            'brand': 'Marca',
        }

        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo: tornillo'}),
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo: radica'}),
        }

    
    # Sobrescribir el método clean para agregar la validación personalizada
    def clean(self):
        cleaned_data = super().clean()
        product_name = cleaned_data.get('product_name')
        brand = cleaned_data.get('brand')
        # Verificar si ya existe un producto con el mismo nombre y marca
        if Product.objects.filter(product_name=product_name, brand=brand).exists():
            raise ValidationError(f'Ya existe un producto con el nombre "{product_name}" y la marca "{brand}".')
        return cleaned_data

# Form for adding new product entries (tracking batches)
class ProductEntryForm(forms.ModelForm):
    class Meta:
        model = ProductEntry
        fields = ['product', 'entered_amount', 'entry_price', 'entry_date']
        
        labels = {
            'product': 'Nombre del Producto',
            'entered_amount': 'Cantidad',
            'entry_price': 'Precio',
            'entry_date': 'Fecha de Ingreso',
        }

        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'entered_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad'}),
            'entry_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),
            'entry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

# Form for handling sales
class SaleForm(forms.Form):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Productos"
    )
    quantities = forms.CharField(
        widget=forms.TextInput,
        label="Cantidades"
    )

class UploadFileForm(forms.Form):
    file = forms.FileField()

class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['firstname', 'lastname', 'email', 'address', 'phone', 'id_or_nit', 'city'] # Campos a capturar del cliente
        
        labels = {
            'firstname': 'Nombres',
            'lastname': 'Apellidos',
            'email': 'Correo electrónico',
            'address': 'Dirección',
            'phone': 'Número de Celular',
            'id_or_nit': 'CC o NIT',
            'city': 'Ciudad',
        }
        
        widgets = {
            'firstname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ej: Pedro Pablo'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ej: Pérez Bravo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ej: pedropablo@gmail.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ej: 3143143141'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ej: Calle 12 12 12'}),
            'id_or_nit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ej: 1061777888'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ej: Popayán'}),
        }

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['payment_method', 'total_amount']

class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['product_id', 'product_name', 'description', 'quantity', 'unit_price', 'total_price']
