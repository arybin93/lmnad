
from django.shortcuts import render
import pandas as pd
import json
import os

def index(request):
    #template = loader.get_template('index.html')
    names = ['{}'.format(x) for x in range(1, 105)]  # максимум 104 записи в одной строке
    names[0] = "lat"
    names[1] = "lon"
    current_file = os.path.abspath(os.path.dirname(__file__))
    csv_path = os.path.join(current_file, "summer.csv")
    data = pd.read_csv(csv_path, names=names, comment="#")
    return render(request, 'default.html', context={"datas": json.dumps(json.loads(data.to_json(orient="split")))})

