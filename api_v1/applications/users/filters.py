import django_filters


class UserOptionFilterSet(django_filters.FilterSet):
    key = django_filters.CharFilter()

    name = django_filters.CharFilter()
