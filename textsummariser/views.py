from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .summariser import generate_summary
# Create your views here.

def summariser(requests):
    if requests.method == "POST":
        input_data = requests.POST["original_text"]
        out_put = generate_summary(input_data, 2)
        template = loader.get_template('index.html')
        context = {
            'summerize': out_put,
            'original' : input_data
        }
        return HttpResponse(template.render(context, requests))
