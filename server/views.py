from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
import json
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt, csrf_protect
##from server.settings import MEDIA_ROOT, MEDIA_URL
from .models import AppUser,ExpertInfo,ExpertToGroup,Project,Domain,Group,ExpertToGroup,DomainToExpertInfo
from .serializers import AppUserSerializer,ExpertInfoSerializer,DomainSerializer1,DomainSerializer2,DomainSerializer3,ProjectSerializer,ExpertToGroupSerializer,GroupSerializer
##import jwt
from rest_framework_jwt.settings import api_settings
import csv as csvreader
from rest_framework.authtoken.models import Token
from .tools import JSONResponse
from django.http import QueryDict
from django.utils import timezone
from django.db.models import Q
from .tools import JSONResponse, wxlogin ,setDomainNames

# Create your views here.

@csrf_exempt
def expertInfo_api(request):
    if request.method == 'POST':
        data_unicode = request.body.decode("UTF-8")
        data = json.loads(data_unicode)
        code = data['code']
        name =data['name']
        IDnum = data['IDnum']
        phone = data['phone']
        domicile = data['domicile']
        company = data['company']
        remarks = data['remarks']
        education = data['education']
        ##uploaderID = request.POST.get('uploaderID')   
        user = wxlogin(code)
        if(True):
            new_expert = ExpertInfo.objects.create(
            name = name,
            IDnum = IDnum,
            phone = phone,
            domain_1 = data['domains'][0]['code'],
            education = education,
            domicile = domicile,
            company = company,
            remarks = remarks,
            status = 'new',
            uploaderID = user.id
            )

            print(data['domains'])

            for domain in data['domains']:
                domain_obj = Domain.objects.get(code = domain['code'])
                obj = DomainToExpertInfo.objects.create(
                    domain = domain_obj,
                    expert = new_expert
                )

            if(len(data['domains'])>=2):
                new_expert.domain_2 = data['domains'][1]['code']
            if(len(data['domains'])>=3):
                new_expert.domain_3 = data['domains'][2]['code']
            if(len(data['domains'])>=4):
                new_expert.domain_4 = data['domains'][3]['code']
            if(len(data['domains'])>=5):
                new_expert.domain_5 = data['domains'][4]['code']

            new_expert.save()

            exp_serializer = ExpertInfoSerializer(new_expert,many=False)

            return JSONResponse({'code':201,'data':exp_serializer.data,'msg':'专家信息创建成功'})
        else:
            return JSONResponse({'code':400,'msg':'创建失败'})

    if request.method=="GET":
        id = request.GET.get('id')
        print(id)
        expert = ExpertInfo.objects.get(id=id)
        expert_ser = ExpertInfoSerializer(expert,many = False)
        print(expert_ser.data)
        return JSONResponse({'code':200,'data':expert_ser.data,'msg':'success'})            

def domains(request):
    root_domains = Domain.objects.filter(level = 1)
    root_serial = DomainSerializer1(root_domains,many = True)

    return JSONResponse({'code':201, 'data':root_serial.data,'msg':'test'})

@csrf_exempt
def project_api(request):
    if request.method == "POST":
        data_unicode = request.body.decode("UTF-8")
        data = json.loads(data_unicode)
        print(data)
        code=data['code']
        title=data['title']
        budget = data['budget']
        num = data['num']
        timespan = data['timespan']
        address = data['address']
        user = wxlogin(code)

        if True:
            new_pro = Project.objects.create(
                creator = user,
                title = title,
                budget = budget,
                num = num,
                timespan = timespan,
                address = address
            )
            new_pro.save()
            new_group = Group.objects.create(
                project = new_pro
            )
            new_group.save()


            return JSONResponse({'code':201,'msg':'项目信息创建成功'})
        else:
            return JSONResponse({'code':400,'msg':'创建失败'})

    if request.method == "GET":
        code = request.GET.get('code')
        id = request.GET.get('id')
        project_obj = Project.objects.get(id=id)
        project_ser = ProjectSerializer(project_obj,many=False)
        
        p_data= project_ser.data

        creator = project_obj.creator.name
        p_data['time_create'] = p_data['time_create'][0:10]
        p_data['creator'] = creator

        group_obj = Group.objects.get(project=project_obj)
        group_ser = GroupSerializer(group_obj,many=False)
        print(group_ser.data)

        
        return JSONResponse({'code':201, 'project':p_data, 'group':group_ser.data ,'msg':'project_detail'})  

def projects(request):
    if request.method == "GET":
        code = request.GET.get('code')
        print(code)
        user = wxlogin(code)

        projects = Project.objects.filter(creator = user)
        
        ser_projects = ProjectSerializer(projects, many=True)
        for item in ser_projects.data:
            item['time_create'] = item['time_create'][0:10]
        
        return JSONResponse({'code':201,'data':ser_projects.data,'msg':'project_list'})

def createPool(request):
    exclude_company = request.GET.get('exclude_company')
    domainId = request.GET.get('domain')
    print(exclude_company)
    print(domainId)
    domain_obj = Domain.objects.get(id=domainId)
    experts = ExpertInfo.objects.filter(
        ~Q(company__icontains = exclude_company)|
        Q(domain_1__icontains = domainId)|
        Q(domain_2__icontains = domainId)|
        Q(domain_3__icontains = domainId)|
        Q(domain_4__icontains = domainId)|
        Q(domain_5__icontains = domainId)
    )
    experts_ser = ExpertInfoSerializer(experts,many=True)
    print(experts_ser.data)
    return JSONResponse({'code':201,'data':experts_ser.data,'msg':'success'})

def searchExperts(request):
    keyword = request.GET.get('keyword')
    print(keyword)
    if True:
        experts = ExpertInfo.objects.filter(
            Q(name__icontains = keyword)|
            Q(company__icontains = keyword)|
            Q(domain_1__icontains = keyword)|
            Q(domain_2__icontains = keyword)|
            Q(domain_3__icontains = keyword)|
            Q(domain_4__icontains = keyword)|
            Q(domain_5__icontains = keyword)
        )
        
        ser_exp = ExpertInfoSerializer(experts,many=True)
        
        ser_exp = setDomainNames(ser_exp)
        print(ser_exp.data)

        return JSONResponse({'code':201,'data':ser_exp.data,'msg':'experts_info'})
    else:
        return JSONResponse({'code':400,'data':'','msg':'no_match'})


@csrf_exempt
def groupMember(request):
    if request.method == "POST":
        data_unicode = request.body.decode("UTF-8")
        data = json.loads(data_unicode)
       
        code=data['code']
        projectId=data['projectId']
        experts = data['expertsList']
        expertiseId = data['expertiseId']
        
        count = len(experts)
        fail_num = 0
        
        user = wxlogin(code)
        project = Project.objects.get(id=projectId)
        group = project.group
        domain = Domain.objects.get( id=expertiseId)

        members = ExpertToGroup.objects.filter(group=group)
        id_list = []
        for member in members:
            id_list.append(member.expert.id)

        for person in experts:
            if person['id'] in id_list:
                fail_num+=1
                continue
            else:
                expert = ExpertInfo.objects.get(id=person['id'])
                new_member = ExpertToGroup.objects.create(
                    group= group,
                    expert = expert,
                    expertise = domain.name,
                )
                new_member.save()
                member_ser = ExpertToGroupSerializer(new_member,many=False)
                print('------')
                print(member_ser.data)


        return JSONResponse({'code':201,'msg':'','success':'','fail':fail_num})
    

def accountInfo(request):
    if request.method == "GET":
        code = request.GET.get('code')
        user = wxlogin(code)
        
        user_ser = AppUserSerializer(user,many=False)
        data = user_ser.data
        del data['openid']
        print(data)
        return JSONResponse({'code':201, 'data':data })



