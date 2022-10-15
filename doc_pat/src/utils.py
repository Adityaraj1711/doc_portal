import csv
from django.http import HttpResponse

from io import StringIO, BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template, render_to_string
from django.template import Context
from django.http import HttpResponse
# from cgi import escape


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), dest=result, encoding="utf-8")
    # # template = get_template(template_src)
    # # context = Context(context_dict)
    # html = render_to_string(template_src, context_dict)
    # # print(template, '***#')
    # # print(context, '***#')
    # # html = template.render(context)
    # result = StringIO()
    #
    # pdf = pisa.pisaDocument(StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors')


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


class ExportAllCsvMixin:
    def export_all_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        print(self.model.objects.all())
        for obj in self.model.objects.all():
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_all_as_csv.short_description = "Export All data"


class BulkSaveMixin:
    """
    Overridden to store instance so that it can be imported in bulk.
    https://github.com/django-import-export/django-import-export/issues/939#issuecomment-509435531
    """
    bulk_instances = []

    def save_instance(self, instance, using_transactions=True, dry_run=False):
        self.before_save_instance(instance, using_transactions, dry_run)
        if not using_transactions and dry_run:
            # we don't have transactions and we want to do a dry_run
            pass
        else:
            self.bulk_instances.append(instance)
        self.after_save_instance(instance, using_transactions, dry_run)

    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        if self.bulk_instances:
            try:
                self._meta.model.objects.bulk_create(self.bulk_instances)
            except Exception as e:
                # Be careful with this
                # Any exceptions caught here will be raised.
                # However, if the raise_errors flag is False, then the exception will be
                # swallowed, and the row_results will look like the import was successful.
                # Setting raise_errors to True will mitigate this because the import process will
                # clearly fail.
                # To be completely correct, any errors here should update the result / row_results
                # accordingly.
                logger.error("caught exception during bulk_import: %s", str(e), exc_info=1)
                raise e
            finally:
                self.bulk_instances.clear()
