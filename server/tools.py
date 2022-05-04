import json
import requests
##import requests
from django.http import HttpResponse, HttpResponseNotFound
from rest_framework.renderers import JSONRenderer
from .models import Key,AppUser,Domain
from .serializers import KeySerializer,AppUserSerializer
 


def tryprint(content):
    on = False
    if on:
        try:
            print(content)
            return
        except:
            return
    else:
        return

def getDomainName(code):
    try:
        obj = Domain.objects.get(code = code)
        return obj.name
    except:
        return ""

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)



def getKeys():
    key = Key.objects.get()
    key_ser = KeySerializer(key,many=False)
  
    return key_ser.data



def wxlogin(code):
    key = getKeys()
    appid = key['appid']
    secret = key['secret']
   
    wxLoginURL = 'https://api.weixin.qq.com/sns/jscode2session?' + 'appid=' + \
        appid+'&secret='+secret+'&js_code='+code+'&grant_type='+'authorization_code'
    res = json.loads(requests.get(wxLoginURL).content)
    if 'errcode' in res:
        return HttpResponse(res['errcode'])
    openid = res['openid']
    user = AppUser.objects.get_or_create(
        openid=openid,
    )
    user = AppUser.objects.get(openid=openid)
    return user

def getDomainName(code):
    domain = Domain.objects.get(code=code)
    return domain.name

def setDomainNames(ser_exp):
    for exp in ser_exp.data:
        print('----')
        print(exp)
        if(exp['domain_1']!=''):
            exp['domain_1'] = getDomainName(exp['domain_1'])
            print(exp['domain_1'])
        if(exp['domain_2']!=''):
            try:
                exp['domain_2'] = getDomainName(exp['domain_2'])
            except:
                return
        if(exp['domain_3']!=''):
            try:
                exp['domain_3'] = getDomainName(exp['domain_3'])
            except:
                return
        if(exp['domain_4']!=''):
            try:
                exp['domain_4'] = getDomainName(exp['domain_4'])
            except:
                return
        if(exp['domain_5']!=''):
            try:
                exp['domain_5'] = getDomainName(exp['domain_5'])
            except:
                return
    
    return ser_exp