import django_filters
from django.db.models import Q

from .models import Scholarship


class ScholarshipFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(field_name="is_active")
    category = django_filters.CharFilter(field_name="category", lookup_expr="icontains")
    level = django_filters.CharFilter(field_name="level", lookup_expr="icontains")
    provider = django_filters.CharFilter(field_name="provider", lookup_expr="icontains")
    eligibility = django_filters.CharFilter(method="filter_eligibility")
    deadline_before = django_filters.DateFilter(field_name="deadline", lookup_expr="lte")
    deadline_after = django_filters.DateFilter(field_name="deadline", lookup_expr="gte")

    class Meta:
        model = Scholarship
        fields = [
            "is_active",
            "category",
            "level",
            "provider",
            "eligibility",
            "deadline_before",
            "deadline_after",
        ]

    def filter_eligibility(self, queryset, name, value):
        del name
        value = (value or "").strip()
        if not value:
            return queryset
        return queryset.filter(Q(eligibility__icontains=value) | Q(tags__icontains=value))

