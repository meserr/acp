from django.shortcuts import render, redirect
from .models import Peptides
import os
import numpy as np
import pandas as pd
import csv
import xlrd
from sklearn.neighbors import KNeighborsClassifier
from AnticancerWebApp.forms import ReadFileForm

# Create your views here.

def index(request):
    search = Peptides.objects.all()
    peptides = []

    for item in search:
        peptides.append(Peptides(peptide=str(item.peptide), label=item.label, length=item.length))

    print(peptides)
    Peptides.objects.all().delete()
    return render(request, "index.html", {"peptides": peptides})

def anasayfa(request):
    search = Peptides.objects.all()
    peptides = []

    for item in search:
        peptides.append(Peptides(peptide=str(item.peptide), label=item.label, length=item.length))

    Peptides.objects.all().delete()
    return render(request, "anasayfa.html", {"peptides": peptides})

def contact(request):
    return render(request, "contact.html")
def iletisim(request):
    return render(request, "iletisim.html")

def information(request):
    return render(request, "info.html")
def yardim(request):
    return render(request, "yardim.html")

def searchFile(request):
    peptides = []
    fastapeptides = []
    peptit = ""
    cleanPeptides = []

    form = ReadFileForm()
    if request.method == 'POST':
        form = ReadFileForm(request.POST, request.FILES)
        if form.is_valid():

            content = request.FILES['file'].readlines()
            for item in content:
                fastapeptides.append(str(item))

            for item in fastapeptides:
                if 0 < 1:
                    if ">" not in item:
                        index = 2
                        while index < len(item) - 3:
                            peptit += item[index]
                            index += 1
                        cleanPeptides.append(peptit)
                        peptit = ""
                else:
                    if ">" not in item:
                        cleanPeptides.append(item)

            if cleanPeptides:  # csv dosyasının oluşması için metot
                peptitToCSV(cleanPeptides)

            result = findClass(peptides=cleanPeptides)
            for key, val in result.items():
                if val == 'TRUE':
                    newPeptit = Peptides(peptide=key, label=True, length=len(key))
                    peptides.append(newPeptit)
                elif val == 'FALSE':
                    newPeptit = Peptides(peptide=key, label=False, length=len(key))
                    peptides.append(newPeptit)

            return render(request, 'searchFile.html', locals(), {"peptides": peptides})

    return render(request, 'searchFile.html', locals(), {"peptides": peptides})
def dosyaarama(request):
    peptides = []
    fastapeptides = []
    peptit = ""
    cleanPeptides = []

    form = ReadFileForm()
    if request.method == 'POST':
        form = ReadFileForm(request.POST, request.FILES)
        if form.is_valid():

            content = request.FILES['file'].readlines()
            for item in content:
                fastapeptides.append(str(item))

            for item in fastapeptides:
                if 0 < 1:
                    if ">" not in item:
                        index = 2
                        while index < len(item) - 3:
                            peptit += item[index]
                            index += 1
                        cleanPeptides.append(peptit)
                        peptit = ""
                else:
                    if ">" not in item:
                        cleanPeptides.append(item)

            if cleanPeptides:  # arff dosyasının oluşması için metot
                peptitToCSV(cleanPeptides)

            result = findClass(peptides=cleanPeptides)
            for key, val in result.items():
                if val == 'TRUE':
                    newPeptit = Peptides(peptide=key, label=True, length=len(key))
                    peptides.append(newPeptit)
                elif val == 'FALSE':
                    newPeptit = Peptides(peptide=key, label=False, length=len(key))
                    peptides.append(newPeptit)

            return render(request, 'dosyaarama.html', locals(), {"peptides": peptides})

    return render(request, 'dosyaarama.html', locals(), {"peptides": peptides})



def searchMultiplePeptides(request):
    if request.method == 'GET':
        return redirect("/")
    else:
        peptit = request.POST.get("peptides")
        peptides = [l for l in peptit.split("\n") if l]

    if peptides: #csv dosyasının oluşması için metot
        peptitToCSV(peptides)

    result = findClass(peptides=peptides)
    print(result)
    for key, val in result.items():
        if val == 'TRUE':
            newPeptit = Peptides(peptide=key, label=True, length=len(key))
            newPeptit.save()
        elif val == 'FALSE':
            newPeptit = Peptides(peptide=key, label=False, length=len(key))
            newPeptit.save()

    return redirect("/")
def cokluarama(request):
    if request.method == 'GET':
        return redirect("/tr")
    else:
        peptit = request.POST.get("peptides")
        peptides = [l for l in peptit.split("\n") if l]

    if peptides: #csv dosyasının oluşması için metot
        peptitToCSV(peptides)

    result = findClass(peptides=peptides)
    print(result)
    for key, val in result.items():
        print(key)
        print(val)
        if val == 'TRUE':
            newPeptit = Peptides(peptide=key, label=True, length=len(key))
            newPeptit.save()
        elif val == 'FALSE':
            newPeptit = Peptides(peptide=key, label=False, length=len(key))
            newPeptit.save()
    return redirect("/tr")

def findClass(peptides):
    result = {}
    data = pd.read_csv(os.getcwd()+"/acp/pc_pev.csv")
    data_test = pd.read_csv(os.getcwd()+"/acp/pc_pev_test.csv")
    x_train = data.drop(['ACP'], axis=1)
    y_train = data.ACP.values
    x_test = data_test
    knn = KNeighborsClassifier()
    knn.fit(x_train, y_train)
    prediction = knn.predict(x_test)
    i = 0
    while i < len(peptides):
        if prediction[i] == 1:
            predictionValue = 'TRUE'
        elif prediction[i] == 0:
            predictionValue = 'FALSE'
        result[peptides[i]] = predictionValue
        i += 1
    return result

def get_Varyans(list):
    return np.var(list)

def get_Value_List(aminoacid):
    cell_value_list = []
    wb = xlrd.open_workbook(os.getcwd() + "/acp/TaylorVenn.xlsx")
    sh = wb.sheet_by_name('Sayfa2')
    for i in range(20):
        cell_value_class = sh.cell(i, 0).value
        if cell_value_class == aminoacid:
            for j in range(1, 11):
                cell_value_list.append(sh.cell(i, j).value)
    print(cell_value_list)
    return cell_value_list

def peptitToCSV(peptitArray):
    att = {}
    oldAtt = {}
    attlist = []
    # özelliklerin excelden alınması
    attpath = os.getcwd() + "/acp/pc_pev_att.xlsx"
    dataatt = pd.read_excel(open(attpath, 'rb'), sheet_name='Sayfa1', header=None, keep_default_na=False)
    attarray = dataatt.values


    # pc_pev yönteminin uygulanması
    for value in peptitArray:
        for attribute in attarray:
            for key in attribute:
                att[key] = 0
        val = str(value).strip()
        index = 0

        while index < len(val) - 1:
            aminoacid = val[index]
            try:
                varyans = get_Varyans(get_Value_List(aminoacid))
                frekans = len([pos for pos, char in enumerate(val) if char == aminoacid])
                att[aminoacid] = varyans * frekans
            except:
                pass
            index += 1
        index = 0
        oldAtt = att.copy()
        attlist.append(oldAtt)
    #oluşan özellik listesinin değerleri csv dosyasına yazdırılıp return işlemi yapılacak
    path = os.getcwd() + "/acp/pc_pev_test.csv"
    attString = ""
    dataString = ""
    if os.path.exists(path):
        os.remove(path)
    with open(path, 'w') as csv_file:
        writer = csv.writer(csv_file)
        for attribute in attarray:
            for val in attribute:
                attString += val

        writer.writerow(attString)

        for dictionary in attlist:
            writer.writerow(dictionary.values())
