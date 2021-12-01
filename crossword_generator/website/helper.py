import django
import random

#TODO:  - link generate button to python script (possibly views function)
#       - add 'check solutions' button
#           - save input to list
#           - compare input to solution list
#           - change color of div container depending if true or not
#       - prompt/nr reformatting (waiting on cw_generator update)

class div_crossword():
    def __init__(self, obj_list, obj_size, prompt_words):
        """
        Initialize the crossword, giving access to all necessary html elements

        :param obj_list: list representation of crossword
        :param obj_size: tuple (height, width) of dimensions of the crossword

        self.empty_html: html syntax for the empty crossword
        self.filled_html: html syntax for the solutions of the crossword
        """
        self.obj_list = obj_list
        self.obj_size = obj_size
        self.prompt_words = prompt_words

        h, w = self.obj_size
        cw_list = self.obj_list

        self.empty_html = self.empty_div(h, w, cw_list, prompt_words)
        self.filled_html = self.filled_div(h, w, cw_list)


    def input_cont(self, nr):
        """ HTML for blank input field
            nr: number that should be displayed in corner (0 if none)
            nr_div: div container displaying small number
            input_div: input field inside of squares
            """
        if nr == 0:
            str_nr = ""
        else:
            str_nr = str(int(nr))
        nr_div = "<div style='position:absolute; font-size:0.5em'>" + str_nr + "</div>"
        input_div = "<input type='text' minlength='1' maxlength='1' style='width:29px; height:29px;text-align:center; " \
                "border-style:none; border-color:black; position:relative; font-weight:bold; background:transparent; " \
               "text-transform:uppercase;'></input>"
        return nr_div + input_div


    def element_empty(self, nr):
        """ empty white div container"""
        return "<div style='width:30px; height:30px; border:thin solid; background:white; padding: 0; margin: 0;'> " \
               + self.input_cont(nr) +"</div>"


    def element_black(self):
        """ black div container """
        return "<div style='width:30px; height:30px; border:thin solid; background:black; padding: 0; margin: 0;'> </div>"


    def empty_div(self, h, w, cw_list, prompt_words):
        """ Creates the HTML syntax for the empty crossword """
        #TODO: adjust nr. depending on wheter it matches 'start position' of word
        empty_div = ""
        for row in range(h):
            empty_div = empty_div + "<div class ='row' style='padding:0; margin:0'>"
            for col in range(w):
                if cw_list[row][col] == '#':
                    empty_div = empty_div + self.element_black()
                else:
                    nr = prompt_words[row][col]
                    empty_div = empty_div + self.element_empty(nr)
            empty_div = empty_div + '</div>'
        return empty_div


    def filled_div(self, h, w, cw_list):
        """ Creates the HTML syntax for the filled crossword """
        filled_div = ""
        for row in range(h):
            filled_div = filled_div + "<div class ='row' style='padding:0; margin:0'>"
            for col in range(w):
                if cw_list[row][col] == '#':
                    filled_div = filled_div + self.element_black()
                else:
                    filled_div = filled_div + "<div class ='col-3' style='width:30px; height:30px; border:thin solid; background:white; padding: 0; margin: 0;'>" \
                                 + cw_list[row][col] + "</div>"
            filled_div = filled_div + "</div>"
        return filled_div



def random_iterator(database: django.db.models.Model, n: int):
    indices = list(range(n))
    random.shuffle(indices)
    for index in indices:
        yield database.objects.all()[index].word