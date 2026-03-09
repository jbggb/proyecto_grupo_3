"""Vistas para reportes"""
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from app.decorators import admin_login_required


@method_decorator(admin_login_required, name='dispatch')
class ReportesView(View):
    def get(self, request):
        return render(request, 'Reportes/reportes.html')


reportes = ReportesView.as_view()
