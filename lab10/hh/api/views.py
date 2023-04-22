
from ast import Delete
from http.client import REQUEST_URI_TOO_LONG
from urllib import request
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .serializers import *
from .models import Company, Vacancy
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view



# Create your views here.


def index(request):
    return HttpResponse('CHECKK')

@api_view(['GET', 'POST'])
def companies_list(request):
    if request.method == 'GET':
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data, status=200)

    elif request.method == 'POST': 
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CompaniesAPIView(APIView):
    def get(self, request):
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data, status=200)
    
    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


@api_view(['GET', 'PUT', 'DELETE'])
def about_company(request, company_id):
    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist as err:
        return Response({'message': str(err)}, status=400)

    if request.method == 'GET':
        serializer = CompanySerializer(company)
        return Response(serializer.data, status=200)

    elif request.method == 'PUT':
        serializer =CompanySerializer(data=request.data, instance=company)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    
    elif request.method == 'DELETE':
        company.delete()
        return Response({'message': 'delete company ' + str(company)})


class AboutCompanyAPIView(APIView):
    def get_company(self, company_id):
        try:
            company = Company.objects.get(id=company_id)
            return company
        except Company.DoesNotExist as err:
            return Response({'massage': str(err)}, status=400)
        
    def get(self, request, company_id=None):
        company = self.get_company(company_id)
        serializer = CompanySerializer(company)
        return Response(serializer.data, status=200)
    
    def put(self, request, company_id=None):
        company = self.get_company(company_id)
        serializer = CompanySerializer(data=request.data, instance=company)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)
    
    def delete(self, request, company_id=None):
        company = self.get_company(company_id)
        company.delete()
        return Response({'message': 'delete company ' + str(company)})


@api_view(['GET'])
def company_vacancies(request, company_id):
    if request.method == 'GET':
        try:
            company = Company.objects.get(id=company_id)
            vacancies = company.companies.all()
            serializer = VacancySerializer(vacancies, many=True)
            return Response(serializer.data, status=200)
        except Company.DoesNotExist as err:
            return Response({'message': str(err)}, status=400)


class CompanyVacanciesAPIView(APIView):
    def get_vacancies(self, company_id):
        try:
            company = Company.objects.get(id=company_id)
            vacancies = company.companies.all()
            return vacancies
        except Company.DoesNotExist as err:
            return Response({'message': str(err)}, status=400)

    def get(self, request, company_id=None):
        vacancies = self.get_vacancies(company_id)
        serializer = VacancySerializer(vacancies, many=True)
        return Response(serializer.data, status=200)


@api_view(['GET', 'POST'])
def vacancies_list(request):
    if request.method == 'GET':
        vacancies = Vacancy.objects.all()
        serializer = VacancySerializer(vacancies, many=True)
        return Response(serializer.data, status=200)

    if request.method == 'POST': 
        serializer = VacancySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class VacanciesAPIView(APIView):
    def get(self, request):
        vacancies = Vacancy.objects.all()
        return Response(VacancySerializer(vacancies, many=True).data)
    
    def post(self, request):
        serializer = VacancySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    


@api_view(['GET', 'PUT', 'DELETE'])
def about_vacancy(request, vacancy_id):
    try:
        vacancy = Vacancy.objects.get(id=vacancy_id)
    except Vacancy.DoesNotExist as err:
        return Response({'massage': str(err)}, status=400)
    
    if request.method == 'GET':
        serializer = VacancySerializer(vacancy)
        return Response(serializer.data, status=200)
    
    elif request.method == 'PUT': 
        serializer = VacancySerializer(data=request.data, instance=vacancy)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)
    
    elif request.method == 'DELETE':
        vacancy.delete()
        return Response({'message': 'delete vacancy ' + str(vacancy)})


class AboutVacancyAPIView(APIView):
    def get_vacancy(self, vacancy_id):
        try:
            vacancy = Vacancy.objects.get(id=vacancy_id)
            return vacancy
        except Vacancy.DoesNotExist as err:
            return Response({'massage': str(err)}, status=400)
        
    def get(self, request, vacancy_id=None):
        vacancy = self.get_vacancy(vacancy_id)
        serializer = VacancySerializer(vacancy)
        return Response(serializer.data, status=200)
    
    def put(self, request, vacancy_id=None):
        vacancy = self.get_vacancy(vacancy_id)
        serializer = VacancySerializer(data=request.data, instance=vacancy)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, vacancy_id=None):
        vacancy = self.get_vacancy(vacancy_id)
        vacancy.delete()
        return Response({'message': 'delete vacancy ' + str(vacancy)})




@api_view(['GET'])
def vacancies_top_ten(request):
   if request.method == 'GET':
       
    vacancies = Vacancy.objects.all().order_by('-salary')[:10] 
    serializer = VacancySerializer(vacancies, many=True)
    return Response(serializer.data, status=200)