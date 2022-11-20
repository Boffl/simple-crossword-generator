import django
import random

#TODO:  - link generate button to python script (possibly views function)
#       - add 'check solutions' button
#           - save input to list
#           - compare input to solution list
#           - change color of div container depending if true or not

class div_crossword():
    def __init__(self, obj_list, obj_size, prompt_words, entered_solutions):
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
        self.entered_solutions = entered_solutions

        h, w = self.obj_size
        cw_list = self.obj_list
        self.size = "2.2vw"
        self.empty_html = self.empty_div(h, w, cw_list, prompt_words)
        self.filled_html = self.filled_div(h, w, cw_list)
        self.corrected_html_syntax = self.corrected_html_syntax(h, w, cw_list, prompt_words, entered_solutions)


    def input_cont(self, nr, coord, content):
        """ HTML for blank input field
            nr: number that should be displayed in corner (0 if none)
            nr_div: div container displaying small number
            input_div: input field inside of squares
            """
        if nr == 0:
            str_nr = ""
        else:
            str_nr = str(nr)
        div_id = "letters" #coordinates of div container
        nr_div = "<div class='index_number' style='position:absolute; font-size:0.5em'>" + str_nr + "</div>"
        # input_div = "<input name='letters' id='" + str(div_id) + "' " +\
        #             "type='text' minlength='1' maxlength='1' style='width:29px; height:29px;text-align:center; " \
        #             "border-style:none; border-color:black; position:relative; font-weight:bold; background:transparent; " \
        #            "text-transform:uppercase;' value=" + content + "></input>"
        input_div = "<input autocomplete='off' name='letters' id='" + str(div_id) + "' " +\
                    "type='text' minlength='1' maxlength='1' style='width:100%; height:100%;text-align:center; " \
                    "border-style:none; border-color:black; position:relative; font-weight:bold; background:transparent; " \
                   "text-transform:uppercase;' value=" + content + "></input>"
        return nr_div + input_div


    def element_empty(self, nr, coord):
        """ empty white div container
        nr: str that is displayed small in corner
        coord: coordinates of div container
        """
        return f"<span style='width:{self.size}; height:{self.size}; border:thin solid; background:#e7e7e7; padding: 0; margin: 0;'> " \
               + self.input_cont(nr, coord, "") +"</span>"


    def element_black(self):
        """ black div container """
        return f"<span style='width:{self.size}; height:{self.size}; border:thin solid; border-color:#f7f7f7; background:#f7f7f7; padding: 0; margin: 0;'> </span>"


    def empty_div(self, h, w, cw_list, prompt_words):
        """ Creates the HTML syntax for the empty crossword """
        empty_div = "<label for='letters'></label>"
        for row in range(h):
            empty_div = empty_div + "<div class ='row' style='padding:0; margin:0'>"
            for col in range(w):
                if cw_list[row][col] == '#':
                    empty_div = empty_div + self.element_black()
                else:
                    nr = prompt_words[row][col]
                    empty_div = empty_div + self.element_empty(nr, (row,col))
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
                    filled_div = filled_div + f"<div class='solution_field' class ='col-3' style='width:{self.size}; height:{self.size}; border:thin solid; background:#e7e7e7; padding: 0; margin: 0;'>" \
                                 + cw_list[row][col] + "</div>"
            filled_div = filled_div + "</div>"
        return filled_div

    def element_corrected(self, nr, coord, solution, given):
        """ empty white div container
        nr: str that is displayed small in corner
        coord: coordinates of div container
        """
        color = "#ff96a3"

        if given == "" or given == " ":
            color = "#e7e7e7"
        if given.upper() == solution.upper():
            color = "#b7edc6"



        return f"<div style='width:{self.size}; height:{self.size}; border:thin solid; background:" + color +"; padding: 0; margin: 0;'> " \
               + self.input_cont(nr, coord, str(given)) + "</div>"


    def corrected_html_syntax(self, h, w, cw_list, prompt_words, entered_solutions):
        """ Creates the HTML syntax for the empty crossword """
        # counts through the empty divs
        empty_counter = 0
        empty_div = "<label for='letters'></label>"
        for row in range(h):
            empty_div = empty_div + "<div class ='row' style='padding:0; margin:0'>"
            for col in range(w):
                if cw_list[row][col] == '#':
                    empty_div = empty_div + self.element_black()
                else:
                    nr = prompt_words[row][col]
                    empty_div = empty_div + self.element_corrected(nr, (row, col), cw_list[row][col], entered_solutions[empty_counter])
                    empty_counter += 1
            empty_div = empty_div + '</div>'
        return empty_div



def random_iterator(database: django.db.models.Model, n: int):
    indices = list(range(n))
    random.shuffle(indices)
    for index in indices:
        yield database.objects.all()[index].word



def html_corrected(entered_solutions):
    """
    :param entered_solutions:
    :param correct_solutions:
    :return: html for the corrected crossword
    """
    # open file with all previous parameters and read it out
    word_list = []
    with open('word_list.txt', 'r') as f:
        for line in f:
            word_list.append(list(line))
    h, w = len(word_list), len(word_list[0])

    with open('prompt_words.txt', 'r') as f:
        prompt_words1 = f.read().split(',')

    prompt_words = []
    for row in range(h):
        templist = []
        for element in range(w):
            templist.append(prompt_words1[int(row)*w + int(element)])
        prompt_words.append(templist)

    cw_html = str(entered_solutions) + str(word_list)

    html_crossword = div_crossword(word_list, (h, w-1), prompt_words, entered_solutions)
    return html_crossword.corrected_html_syntax
