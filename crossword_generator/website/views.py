from django.shortcuts import render
from django.http import HttpResponse
import sys
sys.path.append("..")
import numpy as np
from Database.crossword_generation_15_11_21 import crossword_generator
from .models import Words3
from .helper import div_crossword
from .helper import random_iterator
from .forms import solutions
from django.http import HttpResponseRedirect

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
    input = random_iterator(Words3, 852) # atm there are exactly 852 words in the db
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
    prompt_list = "<h3>Prompts:</h3> <ol id='prompts'>"
    j = 1
    faulty_crossword = False
    for i, word in enumerate(word_list):
        direction = ''

        if word in obj.word_indices:  # need to check this bc of faulty crosswords produce bad indices, leads to errors
            position = obj.word_indices[word]  # index of last and first character of the word in the grid
            if position[0][0] == position[1][0]:
                direction = '(horizontal) '
            if position[0][1] == position[1][1]:
                direction = '(vertical) '
            in1, in2 = position[0]
            # stupidlist.append([in1, in2])
            if prompt_words[in1][in2] == 0:
                prompt_words[in1][in2] = j
            else:
                prompt_words[in1][in2] = f"{prompt_words[in1][in2]}/{j}"  # two words starting in the same place

        else:
            faulty_crossword = True

        # basically creating a long html string, with the definition and the hint.
        # The hint is set to be hidden and there is a button to get the hints displayed
        # The button calls a function in the generate-button.js file
        prompt_list += f"""
        <li>
            <i> {direction} </i>{definition_list[i]}
            <input hidden type="text" value={word} id="hint_for_{word}"</input> 
            <button id='hint_button_for_{word}' class='hint_button' onclick="getHints(document.getElementById('hint_for_{word}').value)"
            style="border:none; color:white; background-color:black; border-radius:12px; font-size:60%; text-align:center;">
                HINT</button>
            <div hidden id='hint_display_for_{word}'> Hint: {hint_list[i]}</div>
        </li> """

        j += 1
    # don't forget
    prompt_list += '</ol>'

    if faulty_crossword:
        prompt_list = prompt_list + "There was a mistake in making the crossword grid." + "<br>"
        prompt_list = prompt_list + "List to debug the Crossword Generator:" + "<br>"
        prompt_list = prompt_list + f"{word_list}" + "<br>"

    """ Create HTML Crossword Syntax """
    # dimensions of crossword: hxw
    cw_list = obj.crossword
    html_crossword = div_crossword(cw_list, (h, w), prompt_words)

    """ Display Crossword """
    context = {
        "crossword_empty": html_crossword.empty_html,
        "crossword_solution": html_crossword.filled_html,


        "fetched_word_list": obj.words,
        "size": obj.size(),
        "prompt_list": prompt_list
    }

    return render(request, 'index.html', context)

# refresh to make new crossword, very simple, but it works...
def refresh(request):
    print('refreshed the page')
    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")


def check_solutions(request):
    """ checks entered solutions of crossword """
    print("checked!")
    if request.method == 'POST':
        form = solutions(request.POST)
        return render(request, 'index.html', {'crossword_empty': form})  # methods must return HttpResponse
    else:
        form = solutions()
        return render(request, 'index.html', {'crossword_empty': form})