from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .summariser import generate_summary
from .mapgeist.api import text_mind_map
from .mapgeist.api.visualization import visualize_tree_2D
from .multiquestion import *
# Create your views here.

def summariser(requests):
    if requests.method == "POST":
        input_data = requests.POST["original_text"]
        out_put = generate_summary(input_data, 2)
        template = loader.get_template('index.html')
        mindmap, root = text_mind_map(input_data)
        visualize_tree_2D(mindmap, root, 'static/images/mindmap.png')

        keywords = get_nouns_multipartite(input_data)
        model = Summarizer()
        result = model(input_data, min_length=30, max_length = 500 , ratio = 0.4)
        summarized_text = model(input_data, min_length=60, max_length = 500 , ratio = 0.4)
        filtered_keys=[]
        for keyword in keywords:
            if keyword.lower() in summarized_text.lower():
                filtered_keys.append(keyword)
        sentences = tokenize_sentences(summarized_text)
        keyword_sentence_mapping = get_sentences_for_keyword(filtered_keys, sentences)
        key_distractor_list = {}
        for keyword in keyword_sentence_mapping:
            try:
                wordsense = get_wordsense(keyword_sentence_mapping[keyword][0],keyword)
                if wordsense:
                    distractors = get_distractors_wordnet(wordsense,keyword)
                    if len(distractors) ==0:
                        distractors = get_distractors_conceptnet(keyword)
                    if len(distractors) != 0:
                        key_distractor_list[keyword] = distractors
                else:
                    
                    distractors = get_distractors_conceptnet(keyword)
                    if len(distractors) != 0:
                        key_distractor_list[keyword] = distractors
            except:
                continue
        index = 1
        result_text = ""
        for each in key_distractor_list:
            sentence = keyword_sentence_mapping[each][0]
            pattern = re.compile(each, re.IGNORECASE)
            output = pattern.sub( " _______ ", sentence)
            # print ("%s)"%(index),output)
            result_text += "%s)"%(index) + output +  "\n" 
            choices = [each.capitalize()] + key_distractor_list[each]
            top4choices = choices[:4]
            random.shuffle(top4choices)
            optionchoices = ['a','b','c','d']
            for idx,choice in enumerate(top4choices):
                result_text += "\t" + optionchoices[idx] + ")" + " " + str(choice) + "\n"
            result_text += "\nMore options: " +  str(choices[4:20]) + "\n\n"
            index = index + 1
        context = {
            'summerize': out_put,
            'original' : input_data,
            'mindmap': "1",
            "result_text": result_text
        }
        return HttpResponse(template.render(context, requests))
