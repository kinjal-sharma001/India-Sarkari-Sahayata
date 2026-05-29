import django_filters
from django.db.models import Q

from .models import Scheme


class SchemeFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(field_name="category_id")
    state = django_filters.CharFilter(field_name="state")
    is_active = django_filters.BooleanFilter(field_name="is_active")
    eligibility = django_filters.CharFilter(method="filter_eligibility")

    class Meta:
        model = Scheme
        fields = ["category", "state", "is_active", "eligibility"]

    def filter_eligibility(self, queryset, name, value):
        del name
        value = (value or "").strip()
        if not value:
            return queryset
        return queryset.filter(Q(eligibility__icontains=value) | Q(tags__icontains=value))

