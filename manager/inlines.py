from django.contrib.contenttypes.admin import GenericTabularInline

from manager import models


class ReadOnlyAdminInlineMixin:
    extra = 0
    can_delete = False

    def get_readonly_fields(self, request, obj=None):
        # join fields from readonly_fields and fields
        readonly_fields = list(super().get_readonly_fields(request, obj) or [])
        fields = list(self.fields or [])

        return list(set(readonly_fields + fields))

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class AuditLogsAdminInline(ReadOnlyAdminInlineMixin, GenericTabularInline):
    model = models.AuditLog
    ct_field = 'target_type'
    ct_fk_field = 'target_id'
    extra = 0
    readonly_fields = fields = (
        'created_at',
        'action',
    )

    ordering = ('-id',)

    can_delete = False

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('target_type')
