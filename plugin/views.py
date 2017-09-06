import base64

import os
import xlrd
import json
import random
import string

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.apps import apps
from duploadPlugin.settings import MEDIA_ROOT

# Create your views here.
from duploadPlugin import settings


def getFields(model=None):
    if model is None:
        return[]
    app=model.split(".")[0]
    model_name=model.split(".")[1]
    model = apps.get_model(app_label=app,model_name=model_name)
    fields=list({"name":i.name,"null_not_allowed":not i.null} for i in model._meta.get_fields() if not i.name == model._meta.pk.name)
    return fields


def renderView(request):
    if request.method == "GET":
        models=[str(model._meta) for model in apps.get_models()]
        return  render(request,"index.html",{"title":"Document Upload Plugin","models":models})
    if request.method == "POST":
        """function to handle the post request to upload the excel and process it"""
        # get the file
        file_path = uploadFile(request)
        #process the file
        wb=xlrd.open_workbook(filename=file_path)
        #all sheets
        # sheet_names=wb.sheet_names
        #get first sheet by index
        sheet=wb.sheet_by_index(0)
        #columns in the sheet
        first_row = sheet.row(0)
        #selected model
        data = request.POST
        model=data.get("model")
        model_fields = getFields(model=model)
        #dump all data in session
        request.session["file_path"] = file_path
        request.session["model_fields"] = model_fields
        request.session["sheet_fields"] = [i.value for i in first_row]
        request.session["model"] = model
        return redirect("upload_data", permanent=True)

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
        context={
            "model_fields": request.session.get("model_fields"),
            "sheet_columns":request.session.get("sheet_fields"),
            "title": "Upload Data",
            "model":request.session.get("model"),
                 }
        return render(request,"upload.html",context)

    if request.method == "POST":
        """function handle the request data, save the model according to the mapping select by the user"""
        model = request.session.get("model")
        app = model.split(".")[0]
        model_name = model.split(".")[1]
        model = apps.get_model(app_label=app, model_name=model_name)
        file_path = request.session.get("file_path")
        wb = xlrd.open_workbook(filename=file_path)
        sheet = wb.sheet_by_index(0)
        header_column=None
        #mapping of the rows:
        data = request.POST
        model_fields = getFields(app+'.'+model_name)
        for rownum in range(sheet.nrows):
            row = sheet.row_slice(rownum, start_colx=0, end_colx=None)
            if rownum==0:
                header_column=[i.value for i in row]
            rowdata = dict(zip(header_column,row))
            if not rownum == 0:
                model_data={}
                for field in model_fields:
                    if field.get("name") in data:
                        # try:
                            model_data.update({field.get("name").split(".")[-1]:rowdata[data[field.get("name")]].value})
                        # except:
                        #     pass
                #get the model instance
                model = apps.get_model(app_label=app, model_name=model_name)()
                #set the attributes
                for i in model_data.items():
                    setattr(model, i[0], i[1])
                #save the model
                model.save()
        return redirect("success_view",permanent=True)



def randomname_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def uploadFile(request):
    file = request.FILES.get("document")
    file_name = request.FILES.get("document").name
    type_of_file = file_name.split(".")[1]
    file_full_path = os.path.join(MEDIA_ROOT, randomname_generator() + "." + type_of_file)
    fout = open(file_full_path, "wb+")
    for chunk in file.chunks():
        fout.write(chunk)
    fout.close()
    return file_full_path

def SuccessView(request):
    """function to upload the data"""
    if request.method=="GET":
        try:
            del request.session["file_path"]
            del request.session["model_fields"]
            del request.session["sheet_fields"]
            del request.session["model"]
        except:
            pass
        return render(request,"success.html",{"title":"Success | Data Upload plugin"})


