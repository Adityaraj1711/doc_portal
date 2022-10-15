from datetime import datetime, timedelta

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.db import models
from .utils import render_to_pdf
from .models import Patient


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        obj = Patient.objects.get(id=kwargs.get('user_id'))
        create_time = obj.create_time
        follow_up_days = obj.follow_up_days
        follow_up = datetime.date(create_time) + timedelta(days=follow_up_days)
        follow_up = follow_up.strftime("%d/%m/%Y")
        address = obj.address
        if address is None or address == "None":
            address = ""
        email = obj.email_id
        if email is None or email == "None":
            email = " - "
        prescription = obj.prescription.replace('\n', '</br>')
        pre_pres = obj.previous_prescription_data.replace('\n', '</br>')
        all = {
            "sal": obj.sal,
            "name": obj.name,
            "age": str(obj.age),
            "gender": obj.gender,
            "address": address,
            "city": obj.city,
            "contact": obj.contact,
            "referred_by": obj.referred_by,
            "email_id": email,
            "payment_mode": obj.payment_mode,
            "diagnosis": obj.diagnosis,
            "prescription": prescription,
            "previous_prescription_data": pre_pres,
            "procedure": obj.procedure,
            "comorbidities": obj.comorbidities,
            "days": str(follow_up_days),
            "follow_up": str(follow_up),
            "inv_date": str(datetime.date(create_time).strftime("%d/%m/%Y"))
        }
        pdf = render_to_pdf('pdf_template.html', all)
        return HttpResponse(pdf, content_type='application/pdf')


def index(request):
    obj = Patient.objects.filter(
        create_time__lt=datetime.date(datetime.now())
    ).delete()
    return render(request, 'index.html')
