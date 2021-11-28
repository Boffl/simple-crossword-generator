


class div_crossword():

    def __init__(self, obj_list, obj_size):
        self.obj_list = obj_list
        self.obj_size = obj_size

        # dimensions of crossword: hxw
        h, w = self.obj_size
        cw_list = self.obj_list

        self.empty_html = self.empty_div(h, w, cw_list)
        self.filled_html = self.filled_div(h, w, cw_list)


    def element_empty(self):
        """ blank white div container"""
        input_cont = "<input type='text' minlength='1' maxlength='1' style='width:29px; height:29px;text-align:center; " \
                     "border-style:none; border-color:black; position:relative; font-weight:bold; background:transparent; text-transform:uppercase;'>" \
                     "</input>"

        return "<div style='width:30px; height:30px; border:thin solid; background:white; padding: 0; margin: 0;'> " \
               + "<div style='position:absolute; font-size:0.5em'> 1 </div>" \
               + input_cont +"</div>"

    def element_black(self):
        return "<div style='width:30px; height:30px; border:thin solid; background:black; padding: 0; margin: 0;'> </div>"


    def empty_div(self, h, w, cw_list):
        """ Creates the HTML syntax for the empty crossword """
        empty_div = ""
        for row in range(h):
            empty_div = empty_div + "<div class ='row' style='padding:0; margin:0'>"
            for col in range(w):
                if cw_list[row][col] == '#':
                    empty_div = empty_div + self.element_black()
                else:
                    empty_div = empty_div + self.element_empty()
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


    def add(self, a, b):
        return a + b

    def sub(self, a, b):
        return a - b

    # explicit function
    def method():
        print("GFG")