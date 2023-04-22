from email.policy import default
from .models import *
from rest_framework import serializers



class CompanySerializer(serializers.Serializer):
    id = serializers.ReadOnlyField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(default='')
    city = serializers.CharField(max_length=50)
    address = serializers.CharField()

    def create(self, validated_data):
        return Company.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.city = validated_data.get('city', instance.city)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance


    class Meta: 
        model = Company
        fields = '__all__'


class VacancySerializer(serializers.ModelSerializer):
    # company = CompanySerializer()

    class Meta:
        model = Vacancy
        fields = '__all__'

    # def create(self, validated_data):
    #     company_data = validated_data.pop('company')
    #     company = Company.objects.create(**company_data)
    #     vacancy = Vacancy.objects.create(company=company, **validated_data)
    #     return vacancy
