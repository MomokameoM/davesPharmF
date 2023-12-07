from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import (
    Product,
    Provideer,
    Client,
    RemissionNote,
    Bill,
    SaleDetails,
)

from .forms import RemessionNoteForm, ProductForm, BillForm, ClientForm, SaleDetailsForm



@login_required
def signout(request):
    logout(request)
    return redirect("home")

def signin(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "login.html",
                {
                    "error": "Nombre de usuario o contraseña incorrectos.",
                },
            )

        login(request, user)
        return redirect("products")

def signup(request):
    if request.method == "GET":
        return render(request, "register.html")
    elif request.method == "POST":
        if request.POST["password"] == request.POST["confirm_password"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password"]
                )
                user.save()
                login(request, user)
                return redirect("signin")
            except IntegrityError:
                return render(
                    request,
                    "register.html",
                    {"error": "El nombre de usuario ya existe."},
                )
        return render(
            request,
            "register.html",
            {"error": "Las contraseñas no coinciden."},
        )

@login_required
def get_products(request):
    products = Product.objects.all()
    return render(request, "products.html", {"products": products})

@login_required
def get_products_generics(request):
    products = Product.objects.filter(generic=True)
    return render(request, "products_generic.html", {"products": products})

@login_required
def get_products_no_generics(request):
    products = Product.objects.filter(generic=False)
    return render(request, "products_no_generic.html", {"products": products})

@login_required
def products_required_prescription(request):
    products = Product.objects.filter(prescription=True)
    return render(request, "products_prescription.html", {"products": products})

@login_required
def products_no_prescription(request):
    products = Product.objects.filter(prescription=False)
    return render(request, "products_no_prescription.html", {"products": products})

@login_required
def create_product(request):
    if request.method == "GET":
        return render(request, "create_product.html", {"form": ProductForm})
    else:
        try:
            form = ProductForm(request.POST)
            if form.is_valid():
                new_product = form.save(commit=False)
                new_product.user = request.user
                new_product.save()
                return redirect("products")
            else:
                return render(
                    request,
                    "create_product.html",
                    {"form": form, "error": "Error al crear el producto"},
                )
        except ValueError:
            return render(
                request,
                "create_product.html",
                {"form": ProductForm, "error": "Error al crear el producto"},
            )

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        product.delete()
        return redirect("products")


def home(request):
    return render(request, "home.html")


@login_required
def create_remission_note(request):
    if request.method == "GET":
        return render(request, "create_remission_note.html", {"form": RemessionNoteForm})
    else:
        try:
            form = RemessionNoteForm(request.POST)
            if form.is_valid():
                form.save()
                redirect("remission_notes")
            else:
                render(request, "create_remission_note.html", {"error": "Error al crear la nota de remision", "form": RemessionNoteForm})
        except ValueError:
            return render(request, "create_remission_note.html", {"form": RemessionNoteForm, "error": "Error al crear la nota de remision"})

@login_required
def delete_remission_note(request, remission_note_id):
    remission_note = get_object_or_404(RemissionNote, pk=remission_note_id)
    if request.method == "POST":
        remission_note.delete()
        return redirect("remission_notes")

@login_required
def remission_note_edit(request, remission_note_id):
    if request.method == "GET":
        remission_note = get_object_or_404(
                RemissionNote,
                pk=remission_note_id
        )
        form = RemessionNoteForm(instance=remission_note)
        return render(
            request,
            "remission_note_detail.html",
            {"remission_note": remission_note, "form": form},
        )
    else:
        try:
            remission_note = get_object_or_404(
                RemissionNote,
                pk=remission_note_id,
            )
            form = RemessionNoteForm(request.POST, instance=remission_note)
            form.save()
            return redirect("remission_notes")
        except ValueError:
            return render(
                request,
                "remission_notes_details.html",
                {"remission_note": remission_note, "form": form, "error": "Error al editar la nota de remision"},
            )

@login_required
def get_remission_notes(request):
    remission_notes = RemissionNote.objects.order_by("-subtotal")
    return render(request, "remission_notes.html", {"remission_notes": remission_notes})

@login_required
def get_provideers(request):
    provideers = Provideer.objects.all()
    return render(request, "provideers.html", {"prodiveers": provideers})

@login_required
def create_bill(request):
    if request.method == "GET":
        return render(request, "create_bill.html", {"form": BillForm})
    else:
        try:
            form = BillForm(request.POST)
            if form.is_valid():
                form.save()
                redirect("bills")
            else:
                render(request, "create_bill.html", {"error": "Error al factura", "form": BillForm})
        except ValueError:
            return render(request, "create_bill.html", {"form": BillForm, "error": "Error al crear factura"})
        
@login_required
def get_bill(request):
    bills = Bill.objects.all()
    return render(request, "bills.html", {"bills":bills})

def edit_bill(request, bill_id):
    if request.method == "GET":
        bill = get_object_or_404(
                Bill,
                pk=bill_id
        )
        form = RemessionNoteForm(instance=bill)
        return render(
            request,
            "bill_details.html",
            {"bill": bill, "form": form},
        )
    else:
        try:
            bill = get_object_or_404(
                Bill,
                pk=bill_id,
            )
            form = Bill(request.POST, instance=bill)
            form.save()
            return redirect("bill")
        except ValueError:
            return render(
                request,
                "bill_details.html",
                {"bill": bill, "form": form, "error": "Error al editar la factura"},
            )
            
@login_required
def get_clients(request):
    clients = Client.objects.all()
    return render(request, "clients.html", {"clients": clients})

@login_required
def create_client(request):
    if request.method == "GET":
        return render(request, "create_client.html", {"form": ClientForm})
    else:
        try:
            form = ClientForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("clients")
            else:
                return render(request, "create_client.html", {"error": "Error al crear el cliente", "form": ClientForm})
        except ValueError:
            return render(request, "create_client.html", {"form": ClientForm, "error": "Error al crear el cliente"})

@login_required
def edit_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == "GET":
        form = ClientForm(instance=client)
        return render(request, "edit_client.html", {"form": form, "client": client})
    else:
        try:
            form = ClientForm(request.POST, instance=client)
            if form.is_valid():
                form.save()
                return redirect("clients")
            else:
                return render(request, "edit_client.html", {"error": "Error al editar el cliente", "form": form, "client": client})
        except ValueError:
            return render(request, "edit_client.html", {"form": form, "error": "Error al editar el cliente", "client": client})

@login_required
def delete_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == "POST":
        client.delete()
        return redirect("clients")
    
@login_required
def get_sale_details(request):
    sale_details = SaleDetails.objects.order_by('-subtotal')
    return render(request, "sale_details.html", {"sale_details": sale_details})

@login_required
def create_sale_details(request):
    if request.method == "GET":
        return render(request, "create_sale_details.html", {"form": SaleDetailsForm})
    else:
        try:
            form = SaleDetailsForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("sale_details")
            else:
                return render(request, "create_sale_details.html", {"error": "Error al crear los detalles de venta", "form": SaleDetailsForm})
        except ValueError:
            return render(request, "create_sale_details.html", {"form": SaleDetailsForm, "error": "Error al crear los detalles de venta"})