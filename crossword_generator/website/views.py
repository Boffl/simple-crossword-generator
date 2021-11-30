from django.shortcuts import render
import sys
sys.path.append("..")
import numpy as np
from Database.crossword_generation_15_11_21 import crossword_generator
from .models import Words3
from .helper import div_crossword


# Create your views here.

def index(request):
    """ Main Page """

    """ Import Data """
    word_list, definition_list = [], []
    for i in range(1, 15):
        # get a random word from the Database
        temp_obj = Words3.objects.order_by('?').first()
        temp_name = temp_obj.word
        temp_def = temp_obj.definition
        # save the data to lists
        word_list.append(temp_name)
        definition_list.append([i, temp_def])

    """ Create Crosword Object """
    obj = crossword_generator(word_list)
    h, w = obj.size()
    stupidlist = []

    """ Render HTML Prompt List """
    prompt_words = list(np.zeros((int(h+1), int(w+1))))
    prompt_list = "<h3>Prompts:</h3> "
    j = int(1)
    for i in range(len(word_list)):
        if word_list[i] in obj.word_indices:
            prompt_list = prompt_list + str(j) + "   " + definition_list[i][1] + "<br>"
            in1, in2 = obj.word_indices[word_list[i]][0]
            stupidlist.append([in1, in2])
            prompt_words[in1][in2] = j
            j += 1


    """ Create HTML Crossword Syntax """
    # dimensions of crossword: hxw
    cw_list = obj.crossword
    html_crossword = div_crossword(cw_list, (h, w), prompt_words)

    """ Display Crossword """
    context = {
        "crossword_empty": html_crossword.empty_html,
        "crossword_solution": html_crossword.filled_html,


        "fetched_word_list": obj.word_indices,
        "size": obj.size(),
        "prompt_list": prompt_list
    }

    return render(request, 'index.html', context)
