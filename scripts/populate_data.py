from api.employees.models import Employee
from api.worksites.models import Worksite
from api.managements.models import Management
from api.products.models import Category, Type, Product
from api.stocks.models import Stock, WorksiteMaxStock
from authentication.users.models import CustomUser
from django.contrib.auth import get_user_model


def run():
    # Clear
    CustomUser.objects.all().delete()
    Employee.objects.all().delete()
    Worksite.objects.all().delete()
    Management.objects.all().delete()
    Category.objects.all().delete()
    Type.objects.all().delete()
    Product.objects.all().delete()
    Stock.objects.all().delete()
    WorksiteMaxStock.objects.all().delete()

    # Employees
    employee1 = Employee.objects.create(employee_id=1, first_name="Bogdan", last_name="SMIRDEC", position="administrator", threshold=3)
    employee1.save()

    employee2 = Employee.objects.create(employee_id=2, first_name="Ibish", last_name="POVATAJ", position="director", threshold=3)
    employee2.save()

    employee3 = Employee.objects.create(employee_id=3, first_name="Damien", last_name="GEERTS", position="studies", manager=employee2, threshold=0)
    employee3.save()

    employee4 = Employee.objects.create(
        employee_id=4, first_name="Valmir", last_name="POVATAJ", position="site_director", manager=employee2, threshold=3
    )
    employee4.save()

    employee5 = Employee.objects.create(
        employee_id=5, first_name="Ermir", last_name="POVATAJ", position="site_supervisor", manager=employee4, threshold=1
    )
    employee5.save()

    employee6 = Employee.objects.create(
        employee_id=6, first_name="Matthieu", last_name="BOBLIN", position="site_supervisor", manager=employee4, threshold=2
    )
    employee6.save()

    employee7 = Employee.objects.create(
        employee_id=7, first_name="Clément", last_name="ALTMANN", position="site_supervisor", manager=employee4, threshold=2
    )
    employee7.save()

    employee8 = Employee.objects.create(
        employee_id=8, first_name="Florian", last_name="BATICLE", position="site_supervisor", manager=employee4, threshold=1
    )
    employee8.save()

    employee9 = Employee.objects.create(
        employee_id=9, first_name="Mendim", last_name="GECAJ", position="site_foreman", manager=employee4, threshold=0
    )
    employee9.save()

    employee10 = Employee.objects.create(
        employee_id=10, first_name="Diamant", last_name="MEHAJ", position="site_foreman", manager=employee4, threshold=0
    )
    employee10.save()

    employee11 = Employee.objects.create(
        employee_id=11, first_name="Yasin", last_name="DURKAL", position="site_foreman", manager=employee4, threshold=0
    )
    employee11.save()

    employee12 = Employee.objects.create(
        employee_id=12, first_name="Esat", last_name="KRASNIQI", position="site_foreman", manager=employee4, threshold=1
    )
    employee12.save()

    employee13 = Employee.objects.create(
        employee_id=13, first_name="Edin", last_name="BEHIC", position="site_foreman", manager=employee4, threshold=0
    )
    employee13.save()

    employee14 = Employee.objects.create(
        employee_id=14, first_name="Rasim", last_name="HALIM", position="site_foreman", manager=employee4, threshold=0
    )
    employee14.save()

    employee15 = Employee.objects.create(
        employee_id=15, first_name="Théo", last_name="LA PALOMBARA", position="site_supervisor", manager=employee4, threshold=1
    )
    employee15.save()

    # CustomUser
    User = get_user_model()
    user1 = User.objects.create_superuser(
        email="bogdan.smirdec@gmail.com", password="cobapp-password", user_id=1, employee=employee1, is_validated=True
    )
    user1.save()

    user2 = User.objects.create(user_id=2, email="damien@example.com", employee=employee3, is_validated=True)
    user2.set_password("motdepasse")
    user2.save()

    user3 = User.objects.create(user_id=3, email="valmir@example.com", employee=employee4, is_validated=True)
    user3.set_password("motdepasse")
    user3.save()

    user4 = User.objects.create(user_id=4, email="ermir@example.com", employee=employee5, is_validated=True)
    user4.set_password("motdepasse")
    user4.save()

    user5 = User.objects.create(user_id=5, email="mendim@example.com", employee=employee9, is_validated=True)
    user5.set_password("motdepasse")
    user5.save()

    # Worksites
    worksite1 = Worksite.objects.create(
        worksite_id=1,
        sector="GO",
        client="Immobilière IDF",
        name="Passage Alexandre",
        address="150, Avenue Georges Clémenceau",
        postal_code="92000",
        city="Nanterre",
        status="finitions",
    )
    worksite1.save()

    worksite2 = Worksite.objects.create(
        worksite_id=2,
        sector="GO",
        client="Corem Promotion",
        name="Confluence",
        address="9, rue Paul Vaillant Couturier",
        postal_code="94140",
        city="Alfortville",
        status="finitions",
    )
    worksite2.save()

    worksite3 = Worksite.objects.create(
        worksite_id=3,
        sector="GO",
        client="Cogedim",
        name="Les Jardins de Valésia",
        address="5, rue Saint Germain",
        postal_code="60800",
        city="Crépy-en-Valois",
        status="gros_oeuvre",
    )
    worksite3.save()

    worksite4 = Worksite.objects.create(
        worksite_id=4, sector="GO", client="Immobilière IDF", name="Clorofil", address="tbd", postal_code="93240", city="Stains", status="finitions"
    )
    worksite4.save()

    worksite5 = Worksite.objects.create(
        worksite_id=5,
        sector="GO",
        client="tbd",
        name="Rives de Vesle - lot 1",
        address="tbd",
        postal_code="51100",
        city="Reims",
        status="gros_oeuvre",
    )
    worksite5.save()

    worksite6 = Worksite.objects.create(
        worksite_id=6,
        sector="GO",
        client="tbd",
        name="Rives de Vesle - lot 2",
        address="tbd",
        postal_code="51100",
        city="Reims",
        status="gros_oeuvre",
    )
    worksite6.save()

    worksite7 = Worksite.objects.create(
        worksite_id=7,
        sector="GO",
        client="tbd",
        name="Rives de Vesle - lot 3",
        address="tbd",
        postal_code="51100",
        city="Reims",
        status="gros_oeuvre",
    )
    worksite7.save()

    worksite8 = Worksite.objects.create(
        worksite_id=8,
        sector="GO",
        client="tbd",
        name="Rives de Vesle - lot 4",
        address="tbd",
        postal_code="51100",
        city="Reims",
        status="gros_oeuvre",
    )
    worksite8.save()

    worksite9 = Worksite.objects.create(
        worksite_id=9,
        sector="GO",
        client="Pichet",
        name="Lot 29",
        address="ZAC de l'Arc Sportif",
        postal_code="92025",
        city="Colombes",
        status="gros_oeuvre",
    )
    worksite9.save()

    worksite10 = Worksite.objects.create(
        worksite_id=10,
        sector="GO",
        client="Pichet",
        name="Lot 31",
        address="ZAC de l'Arc Sportif",
        postal_code="92025",
        city="Colombes",
        status="gros_oeuvre",
    )
    worksite10.save()

    # Management
    management1 = Management.objects.create(worksite=worksite1, employee=employee4)
    management1.save()

    management2 = Management.objects.create(worksite=worksite2, employee=employee4)
    management2.save()

    management3 = Management.objects.create(worksite=worksite3, employee=employee4)
    management3.save()

    management4 = Management.objects.create(worksite=worksite4, employee=employee4)
    management4.save()

    management5 = Management.objects.create(worksite=worksite5, employee=employee4)
    management5.save()

    management6 = Management.objects.create(worksite=worksite6, employee=employee4)
    management6.save()

    management7 = Management.objects.create(worksite=worksite7, employee=employee4)
    management7.save()

    management8 = Management.objects.create(worksite=worksite8, employee=employee4)
    management8.save()

    management9 = Management.objects.create(worksite=worksite9, employee=employee4)
    management9.save()

    management10 = Management.objects.create(worksite=worksite10, employee=employee4)
    management10.save()

    # Categories
    category1 = Category.objects.create(category_id=1, name="coffrage")
    category1.save()

    category2 = Category.objects.create(category_id=2, name="sécurité")
    category2.save()

    category3 = Category.objects.create(category_id=3, name="machine")
    category3.save()

    category4 = Category.objects.create(category_id=4, name="outillage")
    category4.save()

    category5 = Category.objects.create(category_id=5, name="consommable")
    category5.save()

    # Types
    type1 = Type.objects.create(type_id=1, name="Banches", category=category1, threshold=3)
    type1.save()

    type2 = Type.objects.create(type_id=2, name="Plancher", category=category1, threshold=3)
    type2.save()

    type3 = Type.objects.create(type_id=3, name="Escalib", category=category2, threshold=2)
    type3.save()

    type4 = Type.objects.create(type_id=4, name="Protections collectives", category=category2, threshold=2)
    type4.save()

    type5 = Type.objects.create(type_id=5, name="Pelles", category=category3, threshold=3)
    type5.save()

    type6 = Type.objects.create(type_id=6, name="Electroportatif", category=category4, threshold=3)
    type6.save()

    type7 = Type.objects.create(type_id=7, name="Maçonnerie", category=category4, threshold=1)
    type7.save()

    type8 = Type.objects.create(type_id=8, name="Nettoyage", category=category4, threshold=0)
    type8.save()

    type9 = Type.objects.create(type_id=9, name="Matériaux", category=category5, threshold=1)
    type9.save()

    type10 = Type.objects.create(type_id=10, name="Plâtrerie", category=category5, threshold=1)
    type10.save()

    # Products
    product1 = Product.objects.create(
        product_id=1,
        category=category1,
        type=type1,
        name="Paire de panneaux 250",
        brand="Outinord",
        model="B8000 Evo 4",
        packaging=2,
        weight=780,
        height=280,
        length=250,
    )
    product1.save()

    product2 = Product.objects.create(
        product_id=2,
        category=category1,
        type=type2,
        name="Poutrelle primaire 90",
        brand="Alphi-Topdalle",
        model="topdallePP90",
        packaging=50,
        weight=5.4,
        length=90,
    )
    product2.save()

    product3 = Product.objects.create(
        product_id=3,
        category=category2,
        type=type3,
        name="Module",
        brand="Mills-Escalib",
        model="Module",
        packaging=1,
        weight=395,
        height=252,
        length=1,
        width=1,
    )
    product3.save()

    product4 = Product.objects.create(
        product_id=4,
        category=category2,
        type=type4,
        name="Lisses GC",
        packaging=50,
        weight=8,
        length=400,
    )
    product4.save()

    product5 = Product.objects.create(
        product_id=5,
        category=category3,
        type=type5,
        name="Volvo EC920D",
        brand="Volvo",
        model="EC920D",
        packaging=1,
        weight=24600,
    )
    product5.save()

    product6 = Product.objects.create(
        product_id=6,
        category=category4,
        type=type6,
        name="Perforateur TE-70",
        brand="Hilti",
        model="TE-70",
        packaging=1,
        weight=10,
    )
    product6.save()

    product7 = Product.objects.create(
        product_id=7,
        category=category4,
        type=type7,
        name="Marteau",
        brand="Leborgne",
        model="Nanovib",
        packaging=1,
        weight=1,
        height=35,
    )
    product7.save()

    product8 = Product.objects.create(
        product_id=8,
        category=category4,
        type=type8,
        name="Balais rouge & manche",
        packaging=1,
        weight=1,
    )
    product8.save()

    product9 = Product.objects.create(
        product_id=9,
        category=category5,
        type=type9,
        name="Finimur",
        brand="Technique Béton",
        model="FINIMUR FIN",
        packaging=1,
        weight=25,
    )
    product9.save()

    product10 = Product.objects.create(
        product_id=10,
        category=category4,
        type=type10,
        name="Carreau de plâtre 5cm",
        brand="Caroplatre",
        model="plein",
        packaging=1,
        weight=3,
        height="66",
        length="50",
        width="5",
    )
    product10.save()

    # Stock
    worksites = Worksite.objects.all()
    for i in range(len(worksites)):
        worksite_stock = Stock.objects.create(stock_id=i + 1, worksite=worksites[i], product=product1, quantity=2)
        worksite_stock.save()
        worksite_max_stock = WorksiteMaxStock.objects.create(max_stock_id=i + 1, worksite=worksites[i], product=product1, quantity=10)
        worksite_max_stock.save()
