import json
from django.http import HttpResponse
from django.shortcuts import render
from django.apps import apps

# Create your views here.
def renderView(request):
    if request.method == "GET":
        models=[str(model._meta) for model in apps.get_models()]
        return  render(request,"index.html",{"title":"Document Upload Plugin","models":models})

#ajax views
def getModelFields(request):
    """function to return the model fields"""
    try:
        model=request.GET.get("model",None)
        if model is None:
            model_fields=[]
        app=model.split(".")[0]
        model_name=model.split(".")[1]
        model = apps.get_model(app_label=app,model_name=model_name)
        fields=model._meta.get_fields()
        return HttpResponse(json.dumps({"fields":[str(field) for field in fields],"message":"success","status_code":200}),content_type="application/json",status=200)
    except LookupError:
        #raise look up error if model not found
        return HttpResponse(
            json.dumps({"fields": [], "message": "error, model not found", "status_code": 404}),
            content_type="application/json", status=404)



def uploadExcelSheet(request):
    """function to upload the excel sheet"""
    if request.method=="GET":
        return render(request,"upload.html",{"title":"Upload File"})

    if request.method =="POST":
        """function to handle the post request to upload the excel and process it"""

