from django.shortcuts import render
import sys
sys.path.append("..")
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
    obj.word_by_word()

    """ Render HTML Prompt List """
    fetched_words = "<h3>Prompts:</h3> "
    for i in range(len(word_list)):
        fetched_words = fetched_words + str(definition_list[i][0]) + "  " + definition_list[i][1] + "<br>"

    """ Create HTML Crossword Syntax """
    # dimensions of crossword: hxw
    h, w = obj.size()
    cw_list = obj.crossword
    html_crossword = div_crossword(cw_list, (h, w))

    """ Display Crossword """
    context = {
        "crossword_empty": html_crossword.empty_html,
        "crossword_solution": html_crossword.filled_html,

        "fetched_word_list": word_list,
        "fetched_words": fetched_words
    }

    return render(request, 'index.html', context)
