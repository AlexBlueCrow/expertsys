from . import models
from rest_framework import serializers


class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AppUser
        fields = '__all__'

class ExpertInfoSerializer(serializers.ModelSerializer):
    expertise = serializers.CharField(source='expertise.name')
    class Meta:
        model = models.ExpertInfo
        fields = '__all__'


class KeySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Key
        fields = '__all__'
    
class ExpertToGroupSerializer(serializers.ModelSerializer):
    expert = ExpertInfoSerializer(many=False)
    class Meta:
        model = models.ExpertToGroup
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    member = ExpertToGroupSerializer(many=True)
    class Meta:
        model = models.Group
        fields = '__all__'




class DomainSerializer3(serializers.ModelSerializer):
    
    class Meta:
        model = models.Domain
        fields = '__all__'

    

class DomainSerializer2(serializers.ModelSerializer):
    sub_domain = DomainSerializer3(many=True)

    class Meta:
        model = models.Domain
        fields = '__all__'




class DomainSerializer1(serializers.ModelSerializer):
    sub_domain = DomainSerializer2(many=True)
    
    class Meta:
        model = models.Domain
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    has_experts = serializers.SerializerMethodField()
    
    
    class Meta:
        model = models.Project
        fields = ('id','title','budget','num','time_create','timespan','address','has_experts')

    def get_has_experts(self, obj):
        if obj.group:
            print(obj.group)
            return True
        else:
            return False

