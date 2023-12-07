from django.forms import ModelForm
from .models import (
    Provideer,
    Product,
    RemissionNote,
    SaleDetails,
    Bill,
    Client
)


class ProvideerForm(ModelForm):
    class Meta:
        model = Provideer
        fields = [
            "name",
            "second_name",
            "phone",
            "product_sold",
            "street",
            "cp",
            "state",
        ]


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "lot",
            "description",
            "generic",
            "administration",
            "unit_price",
            "expiration_date",
        ]


class RemessionNoteForm(ModelForm):
    class Meta:
        model = RemissionNote
        fields = [
            "payment_type",
            "hour_delivery",
            "day_delivery",
            "amount",
            "provider",
        ]


class RemissionNoteAdminForm(ModelForm):
    class Meta:
        model = RemissionNote
        exclude = ("subtotal",)


class SaleDetailsForm(ModelForm):
    class Meta:
        model = SaleDetails
        exclude = ("get_subtotal",)
        
class BillForm(ModelForm):
    class Meta:
        model = Bill
        fields = "__all__"
        
class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = "__all__"