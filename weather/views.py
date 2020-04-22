from django.shortcuts import render
from secrets import key
import requests
import json
# Create your views here.
def index(request):
    url = 'https://corona.lmao.ninja/v2/countries/{}'
    if request.method == 'POST':
        c = request.POST.get('country').strip()
        country_form = ''.join(ch for ch in c if ch.isalnum() or ch == ' ')
        if len(country_form) == 0:
            country_form = 'invalid'
        try:
            r_form = requests.get(url.format(country_form)).json()
            covid_cases = {
                'country' : r_form['country'],
                'cases' : r_form['cases'],
                'critical' : r_form['critical'],
                'active': r_form['active'],
                'recovered' : r_form['recovered'],
                'flag' : r_form['countryInfo']['flag'],
                'deaths' : r_form['deaths']
            }
        except json.decoder.JSONDecodeError:
            covid_cases = {
                'country' : 'INVALID COUNTRY OR INPUT FORMAT',
                'cases' : 'N/A',
                'critical' : 'N/A',
                'active': 'N/A',
                'recovered' : 'N/A',
                'flag' : 'https://raw.githubusercontent.com/NovelCOVID/API/master/assets/flags/unknow.png',
                'deaths' : 'N/A'
            }
        except KeyError:
            covid_cases = {
                'country' : 'INVALID COUNTRY OR INPUT FORMAT',
                'cases' : 'N/A',
                'critical' : 'N/A',
                'active': 'N/A',
                'recovered' : 'N/A',
                'flag' : 'https://raw.githubusercontent.com/NovelCOVID/API/master/assets/flags/unknow.png',
                'deaths' : 'N/A'
            }
    else:
        country = 'USA'
        r = requests.get(url.format(country)).json()
        covid_cases = {
            'country' : r['country'],
            'cases' : r['cases'],
            'critical' : r['critical'],
            'active': r['active'],
            'recovered' : r['recovered'],
            'flag' : r['countryInfo']['flag'],
            'deaths' : r['deaths']
        }
    graph_url = 'https://corona.lmao.ninja/v2/historical/{}'
    # graph_context = request.session['context']
    # graph_country = graph_context['covid_cases']['country']
    graph_country = covid_cases['country']
    graphData = requests.get(graph_url.format(graph_country)).json()
    try:
        cases = graphData['timeline']['cases']
        deaths = graphData['timeline']['deaths']
        recovered = graphData['timeline']['recovered']
        casesGraph = [[k, v] for k, v in cases.items()]
        # print('cases:', casesGraph)
        deathsGraph = [[k, v] for k, v in deaths.items()]
        # print('deaths:', deathsGraph)
        recoveredGraph = [[k, v] for k, v in recovered.items()]
        # print('recovered:', recoveredGraph)
        dataset = []
        for k in cases.keys():
            if k in deaths.keys() and k in recovered.keys():
                dataset.append([k, cases[k], deaths[k], recovered[k]])
    except KeyError:
        dataset = [0, 0, 0, 0]

    #casesContext = {'dataset': dataset}
    pieData = requests.get('https://corona.lmao.ninja/v2/countries?sort=cases').json()
    pieCountry = covid_cases['country']
    topTenList = []
    for i in range(10):
        if pieCountry != pieData[i]['country']:
            topTenList.append([pieData[i]['country'], pieData[i]['cases']])

    if(pieCountry is not 'INVALID COUNTRY OR INPUT FORMAT'):
        topTenList.append([pieCountry, covid_cases['cases']])
    
    print(topTenList)


    context = {'covid_cases': covid_cases, 'dataset': dataset, 'pie_data': topTenList }
    # request.session['context'] = context
    return render(request, 'weather/newWeather.html', context)



# def graph(request):
#     url = 'https://corona.lmao.ninja/v2/historical/{}'
#     context = request.session['context']
#     country = context['covid_cases']['country']
#     graphData = requests.get(url.format(country)).json()
#     try:
#         cases = graphData['timeline']['cases']
#         deaths = graphData['timeline']['deaths']
#         recovered = graphData['timeline']['recovered']
#         casesGraph = [[k, v] for k, v in cases.items()]
#         print('cases:', casesGraph)
#         deathsGraph = [[k, v] for k, v in deaths.items()]
#         print('deaths:', deathsGraph)
#         recoveredGraph = [[k, v] for k, v in recovered.items()]
#         print('recovered:', recoveredGraph)
#         dataset = []
#         for k in cases.keys():
#             if k in deaths.keys() and k in recovered.keys():
#                 dataset.append([k, cases[k], deaths[k], recovered[k]])
#     except KeyError:
#         dataset = [0, 0, 0, 0]
        
#     casesContext = {'dataset' : dataset }
    
#     return render(request, 'weather/graph_page.html' , casesContext)


def info(request):
    return render(request, 'weather/infoPage.html')
