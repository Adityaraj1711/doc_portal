from django.contrib import admin
from .models import *
from django.contrib.admin import DateFieldListFilter
from .utils import ExportCsvMixin, ExportAllCsvMixin, BulkSaveMixin
from import_export import resources
from src.models import Patient, Procedure, Comorbiditie
from import_export.fields import Field
from import_export.admin import ImportExportModelAdmin
from import_export.instance_loaders import CachedInstanceLoader
from django.contrib import admin, messages
from django.shortcuts import redirect
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.html import format_html
from django.urls import reverse


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'first_name', 'last_name', 'aadhar', 'date_of_birth']
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'first_name', 'last_name', 'aadhar', 'date_of_birth')}),
    )
    fieldsets = UserAdmin.fieldsets

class PatientResource(resources.ModelResource):
    create_time = Field(attribute='create_time', column_name='create_time')
    sal = Field(attribute='sal', column_name='sal')
    name = Field(attribute='name', column_name='name')
    age = Field(attribute='age', column_name='age')
    gender = Field(attribute='gender', column_name='gender')
    address = Field(attribute='address', column_name='address')
    city = Field(attribute='city', column_name='city')
    contact = Field(attribute='contact', column_name='contact')
    referred_by = Field(attribute='referred_by', column_name='referred_by')
    email_id = Field(attribute='email_id', column_name='email_id')
    payment_mode = Field(attribute='payment_mode', column_name='payment_mode')
    prescription = Field(attribute='prescription', column_name='prescription')
    diagnosis = Field(attribute='diagnosis', column_name='diagnosis')
    previous_prescription_data = Field(attribute='previous_prescription_data', column_name='previous_prescription_data')
    follow_up_days = Field(attribute='follow_up_days', column_name='follow_up_days')
    procedure = Field(attribute='procedure', column_name='procedure')
    comorbidities = Field(attribute='comorbidities', column_name='comorbidities')
    class Meta:
        model = Patient

class PatientAdmin(ImportExportModelAdmin):
    resource_class = PatientResource
    change_form_template = 'src/templates/admin/change_form.html'
    # change_list_template = 'src/templates/admin/change_list.html'
    list_per_page = 50
    list_max_show_all = False
    search_fields = ('name', 'address', 'city', 'payment_mode', 'diagnosis')
    list_display = ('name', 'seen_by_doctor', 'city', 'payment_mode', 'diagnosis', 'create_time',
                    'follow_up_days', 'referred_by', 'print_field')
    ordering = ('-seen_by_doctor', '-create_time')
    actions = (ExportCsvMixin.export_as_csv, ExportAllCsvMixin.export_all_as_csv,)

    def print_field(self, obj):
        return format_html(
            "<button><a href='/pdf/{}' target=_blank>Print</a></button>",
            obj.id
        )

    def get_search_fields(self, request):
        if request.user.is_superuser:
            self.search_fields = ('name', 'address', 'city', 'payment_mode', 'diagnosis')
        return self.search_fields

    def get_readonly_fields(self, request, obj=None):
        self.read_only_fields = super().get_readonly_fields(request)
        if request.user.is_superuser:
            self.read_only_fields = ()
        else:
            self.read_only_fields = ('follow_up_days', 'or_days', 'procedure', 'seen_by_doctor', 'prescription',
                                'diagnosis', 'comorbidities')
        return self.read_only_fields

    def save_model(self, request, obj, form, change):
        super(PatientAdmin, self).save_model(request, obj, form, change)
        #messages.warning(request, "Payment is pending, please complete the leftover payment to avoid future disturbance!")
        if request.user.is_superuser:
            obj.seen_by_doctor = True
            obj.save()

    # def response_add(self, request, obj):
    #     return redirect('/pdf/' + str(obj.id))
    #
    # def response_change(self, request, obj):
    #     return redirect('/pdf/' + str(obj.id))


class ProcedureAdmin(admin.ModelAdmin):
    class Meta:
        model = Procedure


class ComorbiditieAdmin(admin.ModelAdmin):
    class Meta:
        model = Comorbiditie

admin.site.base_template = 'src/templates/admin/base.html'
admin.site.login_template = 'src/templates/admin/login.html'
admin.site.index_template = 'src/templates/admin/index.html'
admin.site.base_site_template = 'src/templates/admin/base_site.html'
admin.site.site_header = "Prescription Management Portal"
admin.site.site_title = "Prescription Management Portal"
admin.site.index_title = "Welcome to Prescription Management Portal"
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Comorbiditie, ComorbiditieAdmin)
admin.site.register(Procedure, ProcedureAdmin)
