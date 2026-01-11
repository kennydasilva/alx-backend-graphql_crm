import django_filters
from .models import Customer, Product, Order
from django.d.models import Q

#customer filter
class CustomerFilter(django_filters.FilterSet):
    name_icontains=django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    email_icontains=django_filters.CharFilter(field_name="email", lookup_expr="icontains")
    created_at_gte=django_filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_at_lte=django_filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")
    phone_pattern=django_filters.CharFilter(method="filter_phone_pattern")

    class Meta:
        model=Customer
        fields=[]

    def filter_phone_pattern(self, queryset, name, value):
        return queryset.filter(phone_startswith=value)
    

#product filter
#class ProductFilter(django_filters.FilterSet)