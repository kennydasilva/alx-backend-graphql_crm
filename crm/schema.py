import re
import graphene
from graphene_django import DjangoObjectType
from django.db import transaction
from django.utils import timezone

from .models import Customer, Product, Order


class CustomerType(DjangoObjectType):
    class Meta:
        model=Customer
        fields="_all_"

class ProductType(DjangoObjectType):
    class Meta:
        model=Product
        fields="_all_"

class OrderType(DjangoObjectType):
    class Meta:
        model=Order
        fields="_all_"



#mutations

class createCustomer(graphene.Mutation):
    customer=graphene.Field(CustomerType)
    message=graphene.String()

    class Arguments:
        name=graphene.String(required=True)
        email=graphene.String(required=True)
        phone=graphene.String()

    def mutate(self, info, name, email, phone=None):
        if customer.objects.filter(email=email).exists():
            raise Exception("Email already exists")
        
        if phone:
            pattern= r"^(\+\d{10,15}|d{3}-\d{4})$"
            if not re.match(pattern, phone):
                raise Exception("Invalid phone format")
            
        customer=Customer.ojects.create(
            name=name,
            email=email,
            phone=phone
        )

        return createCustomer(
            customer=customer, 
            message="Customer created successfully"
        )