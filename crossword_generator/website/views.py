from django.shortcuts import render
import sys
sys.path.append("..")
import numpy as np
from Database.crossword_generation_15_11_21 import crossword_generator
from .models import Words3
from .helper import div_crossword
from .helper import random_iterator


# Create your views here.

def index(request):
    """ Main Page """

    """ Import Data """
    #word_list, definition_list = [], []
    #for i in range(1, 15):
        # get a random word from the Database
        #temp_obj = Words3.objects.order_by('?').first()
        #temp_name = temp_obj.word
        #temp_def = temp_obj.definition
        # save the data to lists
        #word_list.append(temp_name)
        #definition_list.append([i, temp_def])

    """ Create Crosword Object """
    # iterator object (see helper.py)
    input = random_iterator(Words3, 900) # don't know how much in total, but less than 1000
    obj = crossword_generator(input, 10) # create crossword with 10 words
    h, w = obj.size()  # dimensions of the crossword grid
    word_list = obj.words
    definition_list = [Words3.objects.filter(word = w)[0].definition for w in word_list]
    hint_list = [Words3.objects.filter(word = w)[0].hint for w in word_list]
    # note in the above we are getting definitions by assuming that every word only occurs once.
    # once we include homonyms and holonyms the .filter() method will return a longer list, and we have to choose
    # which definition/hint to use.
    # stupidlist = []

    """ Render HTML Prompt List """
    prompt_words = np.zeros((int(h+1), int(w+1))).tolist()
    prompt_list = "<h3>Prompts:</h3> "
    j = 1
    for i, word in enumerate(word_list):
        prompt_list = prompt_list + str(j) + "   " + definition_list[i] + "<br>"
        if word in obj.word_indices:  # faulty crosswords produce bad indices, leads to errors
            in1, in2 = obj.word_indices[word][0]
            # stupidlist.append([in1, in2])
            if prompt_words[in1][in2] == 0:
                prompt_words[in1][in2] = j
            else:
                prompt_words[in1][in2] = f"{prompt_words[in1][in2]}/{j}"
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

