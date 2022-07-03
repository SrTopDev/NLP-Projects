from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .summariser import generate_summary
from .mapgeist.api import text_mind_map
from .mapgeist.api.visualization import visualize_tree_2D
# Create your views here.

def summariser(requests):
    if requests.method == "POST":
        input_data = requests.POST["original_text"]
        out_put = generate_summary(input_data, 2)
        template = loader.get_template('index.html')
        mindmap, root = text_mind_map(input_data)
        visualize_tree_2D(mindmap, root, 'static/images/mindmap.png')
        context = {
            'summerize': out_put,
            'original' : input_data,
            'mindmap': "1"
        }
        return HttpResponse(template.render(context, requests))
