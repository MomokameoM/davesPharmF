from django.contrib import admin
from .forms import SaleDetailsForm, RemissionNoteAdminForm
from .models import (
    Product,
    Provideer,
    Client,
    RemissionNote,
    Bill,
    Employee,
    SaleDetails,
)

class SaleDetailsAdmin(admin.ModelAdmin):
    form = SaleDetailsForm
    exclude = ("subtotal",)
    list_display = ('get_products', 'quantity_sold', 'unit_price', 'get_subtotal', 'sale_date', 'sale_hour', 'employee')

    def get_products(self, obj):
        return ", ".join([str(product) for product in obj.product.all()])
    get_products.short_description = 'Productos'

    def get_subtotal(self, obj):
        if obj.quantity_sold is not None and obj.unit_price is not None:
            return obj.quantity_sold * obj.unit_price
        else:
            return None
    get_subtotal.short_description = 'Subtotal'

class RemissionNoteAdmin(admin.ModelAdmin):  
    form = RemissionNoteAdminForm
    

admin.site.register(SaleDetails, SaleDetailsAdmin)
admin.site.register(Product)
admin.site.register(Provideer)
admin.site.register(Client)
admin.site.register(RemissionNote, RemissionNoteAdmin)  
admin.site.register(Bill)
admin.site.register(Employee)
