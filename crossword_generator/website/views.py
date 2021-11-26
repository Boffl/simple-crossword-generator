from django.shortcuts import render
import sys
sys.path.append("..")
from Database.crossword_generation_15_11_21 import crossword_generator
from .models import Words3


# Create your views here.

def index(request):
    """ Main Page """
    word_list = []
    definition_list = []

    """ Import Data """
    for i in range(1, 11):
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


    """ Create Empty Crossword """
    # dimensions of crossword: hxw
    h, w = obj.size()
    cw_list = obj.crossword

    empty_div = ""
    for row in range(h):
        empty_div = empty_div + "<div class ='row' style='padding:0; margin:0'>"
        for col in range(w):
            if cw_list[row][col] == '#':
                empty_div = empty_div + "<div class ='col-3' style='display: flex; width:30px; height:30px; border:thin solid; background:black; padding: 0; margin: 0;'> </div>"
            else:
                empty_div = empty_div + "<div class ='col-3' style='width:30px; height:30px; border:thin solid; background:white; padding: 0; margin: 0;'> </div>"
        empty_div = empty_div + '</div>'

    """ Create Filled Crossword"""
    filled_div = ""
    for row in range(h):
        filled_div = filled_div + "<div class ='row' style='padding:0; margin:0'>"
        for col in range(w):
            if cw_list[row][col] == '#':
                filled_div = filled_div + "<div class ='col-3' style='width:30px; height:30px; border:thin solid; background:black; padding: 0; margin: 0;'> </div>"
            else:
                filled_div = filled_div + "<div class ='col-3' style='width:30px; height:30px; border:thin solid; background:white; padding: 0; margin: 0;'>"\
                             + cw_list[row][col] + "</div>"
        filled_div = filled_div + "</div>"


    """ Display Crossword """
    context = {
        "cw": obj,
        "crossword_empty": empty_div,
        "crossword_solution": filled_div,
        "cw_list": cw_list,
        "size": obj.size(),
        "fetched_word_list": word_list,
        "fetched_words": fetched_words,

    }


    return render(request, 'index.html', context)
