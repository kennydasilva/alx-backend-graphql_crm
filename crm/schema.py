import re
import graphene
from graphene_django import DjangoObjectType
from django.db import transaction
from django.utils import timezone

from .models import Customer, Product, Order
from graphene_django.filter import DjangoFilterConnectionField
from .filters import CustomerFilter, ProductFilter, OrderFilter




class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = "__all__"


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = "__all__"


class Query(graphene.ObjectType):
    hello = graphene.String()
    
    def resolve_hello(self, info):
        return "CRM API is alive"
    
    all_customers = DjangoFilterConnectionField(
        CustomerType, filterset_class=CustomerFilter
    )
    all_products = DjangoFilterConnectionField(
        ProductType, filterset_class=ProductFilter
    )
    all_orders = DjangoFilterConnectionField(
        OrderType, filterset_class=OrderFilter
    )


#inputs
class CreateCustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()

class CreateProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    price = graphene.Decimal(required=True)
    stock = graphene.Int(default_value=0)

class CreateOrderInput(graphene.InputObjectType):
    customer_id = graphene.ID(required=True)
    product_ids = graphene.List(graphene.ID, required=True)
    order_date = graphene.DateTime()

#mutations

class CreateCustomer(graphene.Mutation):
    customer = graphene.Field(CustomerType)
    message = graphene.String()

    class Arguments:
        input = CreateCustomerInput(required=True)

    def mutate(self, info, input):
        if Customer.objects.filter(email=input.email).exists():
            raise Exception("Email already exists")

        if input.phone:
            pattern = r"^(\+\d{10,15}|\d{3}-\d{3}-\d{4})$"
            if not re.match(pattern, input.phone):
                raise Exception("Invalid phone format")

        customer = Customer(
            name=input.name,
            email=input.email,
            phone=input.phone
        )

        customer.save()

        return CreateCustomer(
            customer=customer,
            message="Customer created successfully"
        )

    


#bulkcreateCustomers
class BulkCustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()


class BulkCreateCustomers(graphene.Mutation):
    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    class Arguments:
        input = graphene.List(BulkCustomerInput, required=True)

    def mutate(self, info, input):
        created = []
        errors = []

        with transaction.atomic():
            for idx, data in enumerate(input):
                try:
                    if Customer.objects.filter(email=data.email).exists():
                        raise Exception("Email already exists")

                    customer = Customer(
                        name=data.name,
                        email=data.email,
                        phone=data.phone
                    )

                    customer.save()
                    created.append(customer)

                except Exception as e:
                    errors.append(f"Row {idx + 1}: {str(e)}")

        return BulkCreateCustomers(customers=created, errors=errors)



#create Product
class CreateProduct(graphene.Mutation):
    product = graphene.Field(ProductType)

    class Arguments:
         input = CreateProductInput(required=True)

    def mutate(self, info, input):
        if input.price <= 0:
            raise Exception("Price must be positive")

        if input.stock < 0:
            raise Exception("Stock cannot be negative")

        product = Product(
            name=input.name,
            price=input.price,
            stock=input.stock
        )

        product.save()

        return CreateProduct(product=product)


# Create Order

class CreateOrder(graphene.Mutation):
    order = graphene.Field(OrderType)

    class Arguments:
        input = CreateOrderInput(required=True)

    def mutate(self, info, input):
        if not input.product_ids:
            raise Exception("At least one product must be selected")

        try:
            customer = Customer.objects.get(id=input.customer_id)
        except Customer.DoesNotExist:
            raise Exception("Invalid customer ID")

        products = Product.objects.filter(id__in=input.product_ids)
        if products.count() != len(input.product_ids):
            raise Exception("Invalid product ID")

        total = sum([p.price for p in products])

        order = Order(
            customer=customer,
            total_amount=total,
            order_date=input.order_date or timezone.now()
        )

        order.save()

        order.products.set(products)

        return CreateOrder(order=order)



class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()


