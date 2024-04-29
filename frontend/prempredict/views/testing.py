from django.http import HttpResponse
from django.views.generic import View
from ..models import *

class TestingGet(View):
    def get(self, request, *args, **kwargs):
        testresult = list(TestTable.objects.filter().values())
        return HttpResponse(testresult, status=200)
    
class TestingInsert(View):
    def get(self, request, *args, **kwargs):
        if request.GET.get("name") is None or request.GET.get("id") is None :
            return HttpResponse("Either ID or Name is not specified", status=200)
        testresult = TestTable(id=int(request.GET.get("id")), name=str(request.GET.get("name")))
        testresult.save()
        print(testresult)
        return HttpResponse(testresult, status=200)
    
class TestingUpdate(View):
    def get(self, request, *args, **kwargs):
        testresult = list(TestTable.objects.filter().values())
        print(testresult)
        return HttpResponse(testresult, status=200)
    
class TestingDelete(View):
    def get(self, request, *args, **kwargs):
        if request.GET.get("id") is None:
            return HttpResponse("No ID specified", status=200)
        testresult = TestTable.objects.filter(id=int(request.GET.get("id"))).delete()
        print(testresult)
        return HttpResponse(testresult, status=200)