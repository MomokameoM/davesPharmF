from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from datetime import datetime
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
def get_bill(request):
    bills = Bill.objects.all()
    return render(request, "bills.html", {"bills": bills})

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
        return render(request, "create_product.html")
    elif request.method == "POST":
        try:
            name = request.POST.get('name')
            lot = request.POST.get('lot')
            description = request.POST.get('description')
            generic = bool(request.POST.get('generic'))
            unit_price = float(request.POST.get('unit_price'))
            expiration_date = request.POST.get('expiration_date')

            # Guardar los datos en la base de datos
            new_product = Product.objects.create(
                name=name,
                lot=lot,
                description=description,
                generic=generic,
                unit_price=unit_price,
                expiration_date=expiration_date,
                
            )

            return redirect("products")
        except ValueError:
            return render(
                request,
                "create_product.html",
                {"error": "Error al crear el producto"},
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
    clients = Client.objects.all()  # Obtén la lista de clientes
    sale_details = SaleDetails.objects.all()  # Obtén todos los detalles de la venta

    if request.method == "POST":
        try:
            rfc_client_id = request.POST.get("rfc_client_ic")
            sale_date_str = request.POST.get("sale_date")
            
            # Verificar si sale_date_str es None o está vacío
            if sale_date_str:
                # Convertir la cadena de fecha a un objeto de fecha
                sale_date = datetime.strptime(sale_date_str, "%Y-%m-%d").date()
            else:
                sale_date = None

            quantity_sold = float(request.POST.get("quantity_sold", 0))
            subtotal = float(request.POST.get("subtotal", 0))
            unit_price = float(request.POST.get("unit_price", 0))

            # Obtener el objeto Client usando el ID proporcionado
            client = Client.objects.get(id=rfc_client_id)

            # Crear la factura utilizando el objeto Client y otros datos
            bill = Bill.objects.create(
                rfc_client=client,
                sale_date=sale_date,
                quantity_sold=quantity_sold,
                subtotal=subtotal,
                unit_price=unit_price
            )

            # Guardar la instancia de Bill en la base de datos
            bill.save()

            return redirect("bills")
        except ValueError:
            return render(request, "create_bill.html", {"error": "Error al crear factura", "clients": clients, "sale_details": sale_details})
    else:
        return render(request, "create_bill.html", {"clients": clients, "sale_details": sale_details})



@login_required
def delete_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == "POST":
        client.delete()
        return redirect("clients")

@login_required
def get_clients(request):
    clients = Client.objects.all()
    return render(request, "clients.html", {"clients": clients})

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