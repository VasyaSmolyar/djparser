from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.core.paginator import Paginator
from .models import Site,Node
from .forms import SiteForm
from .parse import parser
import json

# Create your views here.
def index(request):
    if request.method == 'GET':
        form = SiteForm()
        sites = Site.objects.order_by('-pub_date').all()
        return render(request,'index.html',{'sites' : sites,'form' : form})
    else:
        sites = Site.objects.order_by('-pub_date').all()
        form = SiteForm(request.POST)
        if form.is_valid():
            site = Site.objects.create(**form.cleaned_data)
            site.save()
            return redirect(reverse('djparser:index'))
        else:
            return render(request,'index.html',{'sites' : sites,'form' : form, 'err' : form.errors})

def delete(request,sid):
    site = get_object_or_404(Site,pk = sid)
    Node.objects.filter(site=site).delete()
    site.delete()
    return redirect(reverse('djparser:index'))

def parse(request,sid):
    site = get_object_or_404(Site,pk = sid)
    pobj = json.load(open('parser.json'))
    try:
        res = parser(site.url,site.query,pobj['headers'],pobj['proxies'])
    except Exception as e:
        form = SiteForm()
        sites = Site.objects.order_by('-pub_date').all()
        return render(request,'index.html',{'sites' : sites,'form' : form, 'err' : e})
    nodes = Node.objects.filter(site=site).all()
    vals = [n.val for n in nodes]
    inf = []
    for i in res:
        if i not in vals:
            node = Node.objects.create(site=site,val=i)
            node.save()
            inf.append(i)
    return render(request,'parser.html',{'site' : site,'res' : inf })

def result(request,sid):
    site = get_object_or_404(Site,pk = sid)
    res = Node.objects.filter(site=site).order_by('-pub_date').all()
    inf = [r.val for r in res]
    print(len(inf))
    pag = Paginator(inf,10)
    if 'page' in request.GET:
        page = request.GET['page']
    else:
        page = 1
    inf = pag.get_page(page)
    return render(request,'result.html',{'site' : site,'res' : inf })

def setting(request):
    try:
        pobj = json.load(open('parser.json'))
    except OSError:
        pobj = {
            "headers" : {
                "User-Agent" : "",
                "Cookie" : ""
            },
            "proxies" : {
                "http" : "",
                "https" : ""
            }
        }
        json.dump(pobj,open('parser.json','w'))
    ans = {
        'agent' : pobj['headers']['User-Agent'],
        'cookie' : pobj['headers']['Cookie'],
        'http' : pobj['proxies']['http'],
        'https' : pobj['proxies']['https'],
    }
    if request.method == "GET":
        return render(request,'setting.html',ans)
    else:
        pobj['headers']['User-Agent'] = request.POST['User-Agent']
        pobj['headers']['Cookie'] = request.POST['Cookie']
        pobj['proxies']['http'] = request.POST['http']
        pobj['proxies']['https'] = request.POST['https']
        json.dump(pobj,open('parser.json','w'))
        ans = {
            'agent' : pobj['headers']['User-Agent'],
            'cookie' : pobj['headers']['Cookie'],
            'http' : pobj['proxies']['http'],
            'https' : pobj['proxies']['https'],
            'ok' : 'Данные парсера обновлены'
        }
        return render(request,'setting.html',ans)
