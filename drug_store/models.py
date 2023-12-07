from django.db import models
from django.contrib.auth.models import User
from django.db import transaction

class Product(models.Model):
    ADMINISTRATION_CHOICES = [
        ("oral", "Oral"),
        ("intramuscular", "Intramuscular"),
        ("intravenosa", "Intravenosa"),
        ("sublingual", "Sublingual")
    ]
    name = models.CharField(max_length=100, null=False, verbose_name="Nombre")
    lot = models.CharField(max_length=10, verbose_name="Lote")
    purchase_date = models.DateField(auto_now_add=True, null=False, verbose_name="Fecha de Compra")
    expiration_date = models.DateField(null=False, verbose_name="Fecha de Caducidad")
    description = models.TextField(max_length=500, null=False, verbose_name="Descripción")
    generic = models.BooleanField(default=False, null=False, verbose_name="Genérico")
    administration = models.CharField(max_length=30, null=False, choices=ADMINISTRATION_CHOICES, default="oral", verbose_name="Administración")
    prescription = models.BooleanField(default=False, verbose_name="Prescripción")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, verbose_name="Precio Unitario")
    stock = models.IntegerField(null=False, verbose_name="Cantidad", default=0)

    def __str__(self):
        generic_status = "Genérico" if self.generic else "No Genérico"
        prescription_status = "Receta" if self.prescription else "Sin Receta"
        return f"{self.name} Cantidad {self.stock} - {generic_status} - ${self.unit_price} - {prescription_status}"

    class Meta:
        verbose_name_plural = "Productos"


class Provideer(models.Model):
    name = models.CharField(max_length=70, null=False, verbose_name="Nombre")
    second_name = models.CharField(max_length=100, null=False, verbose_name="Apellido")
    phone = models.CharField(max_length=10, null=False, verbose_name="Teléfono")
    product_sold = models.ManyToManyField(Product, verbose_name="Producto")
    street = models.CharField(max_length=40, null=False, verbose_name="Calle")
    cp = models.CharField(max_length=5, null=False, verbose_name="Código Postal")
    state = models.CharField(max_length=40, null=False, verbose_name="Estado")

    def __str__(self):
        products_str = ", ".join([str(product) for product in self.product_sold.all()])
        return f"{self.name} {self.second_name} - Productos: {products_str}"

    class Meta:
        verbose_name_plural = "Proveedores"

class RemissionNote(models.Model):
    PAYMENT_CHOICES = [
        ("tarjeta", "Tarjeta"),
        ("efectivo", "Efectivo"),
    ]
    payment_type = models.CharField(
        max_length=10,
        choices=PAYMENT_CHOICES,
        default="tarjeta",
        verbose_name="Tipo de Pago"
    )
    hour_order = models.TimeField(verbose_name="Hora de Orden")
    day_order = models.DateField(verbose_name="Fecha de Orden")
    hour_delivery = models.TimeField(null=False, verbose_name="Hora de Entrega")
    day_delivery = models.DateField(null=False, verbose_name="Fecha de Entrega")
    subtotal = models.IntegerField(verbose_name="Subtotal")
    amount = models.IntegerField(verbose_name="Cantidad")
    provider = models.ForeignKey(Provideer, on_delete=models.CASCADE, verbose_name="Proveedor")

    def save(self, *args, **kwargs):
        # Calcula el subtotal multiplicando el precio por la cantidad
        subtotal = sum(product.unit_price * self.amount for product in self.provider.product_sold.all())
        self.subtotal = subtotal

        with transaction.atomic():
            super().save(*args, **kwargs)
            self.provider.product_sold.update(stock=models.F('stock') + self.amount)

    def __str__(self):
        return f"Nota de Remisión - Proveedor: {self.provider.name} - ${self.subtotal} {self.get_payment_type_display()}"

    class Meta:
        verbose_name_plural = "Pedidos Proveedores"

class Employee(models.Model):
    name = models.CharField(max_length=50, null=False, verbose_name="Nombre")
    second_name = models.CharField(max_length=50, null=False, verbose_name="Apellido")
    three_name = models.CharField(max_length=50, null=False, verbose_name="Segundo Apellido")
    phone_number = models.CharField(max_length=10, null=False, verbose_name="Teléfono")

    def __str__(self):
        return f"Empleado: {self.name} {self.second_name}"

    class Meta:
        verbose_name_plural = "Empleados"

class Client(models.Model):
    name = models.CharField(max_length=50, null=False, verbose_name="Nombre")
    second_name = models.CharField(max_length=50, null=False, verbose_name="Apellido")
    three_name = models.CharField(max_length=50, null=False, verbose_name="Segundo Apellido")
    phone_number = models.CharField(max_length=10, null=False, verbose_name="Teléfono")
    rfc = models.CharField(max_length=13, null=False, verbose_name="RFC")

    def __str__(self):
        return f"Cliente: {self.name}"

    class Meta:
        verbose_name_plural = "Clientes"

class SaleDetails(models.Model):
    sale_date = models.DateField(auto_now_add=True, verbose_name="Fecha de Venta")
    sale_hour = models.TimeField(auto_now_add=True, verbose_name="Hora de Venta")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Empleado")
    product = models.ManyToManyField(Product, verbose_name="Productos")
    quantity_sold = models.PositiveIntegerField(default=1, null=False, verbose_name="Cantidad Vendida")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, verbose_name="Precio Unitario")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=False, verbose_name="Subtotal")

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity_sold * self.unit_price

        super().save(*args, **kwargs)

        for product in self.product.all():
            product.stock -= self.quantity_sold  
            product.save()

    def __str__(self):
        products_str = ", ".join([str(product) for product in self.product.all()])
        return f"Detalle de Venta - Productos: {products_str} - Cantidad: {self.quantity_sold} - {self.employee}"

    class Meta:
        verbose_name_plural = "Detalles de ventas"

class Bill(models.Model):
    rfc_client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Cliente RFC")
    products_purchased = models.ManyToManyField(SaleDetails, verbose_name="Detalles de Venta")

    def __str__(self):
        details_str = ", ".join([str(detail) for detail in self.products_purchased.all()])
        return f"Factura - Cliente: {self.rfc_client.name} - Detalles de Venta: {details_str}"

    class Meta:
        verbose_name_plural = "Factura"