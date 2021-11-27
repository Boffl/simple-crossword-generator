from django.shortcuts import render
import sys
sys.path.append("..")
from Database.crossword_generation_15_11_21 import crossword_generator
from .models import Words3
from .helper import div_crossword


# Create your views here.

def index(request):
    """ Main Page """
    word_list = []
    definition_list = []

    """ Import Data """
    for i in range(1, 15):
        # get a random word
        temp_obj = Words3.objects.order_by('?').first()
        temp_name = temp_obj.word
        temp_def = temp_obj.definition

        # save data to lists
        word_list.append(temp_name)
        definition_list.append([i, temp_def])

    """ Create Crosword """
    # obj: crossword object
    obj = crossword_generator(word_list)
    obj.word_by_word()

    """ Render html List """
    fetched_words = "<h3>Prompts:</h3> "
    for i in range(len(word_list)):
        fetched_words = fetched_words + str(definition_list[i][0]) + "  " + definition_list[i][1] + "<br>"


    """ Create Crossword """
    # dimensions of crossword: hxw
    h, w = obj.size()
    cw_list = obj.crossword
    html_crossword = div_crossword(cw_list, (h,w))


    """ Display Crossword """
    context = {
        "crossword_empty": html_crossword.empty_html,
        "crossword_solution": html_crossword.filled_html,

        "cw_list": cw_list,
        "size": obj.size(),
        "fetched_word_list": word_list,
        "fetched_words": fetched_words
    }

    return render(request, 'index.html', context)
