import django_filters


class ManagerOptionFilterSet(django_filters.FilterSet):
    key = django_filters.CharFilter()

    name = django_filters.CharFilter()
