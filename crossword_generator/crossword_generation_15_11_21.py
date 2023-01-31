from copy import deepcopy
import re

class crossword_generator():

    def __init__(self,input, size:int):
        self.input = input
        self.words = []
        self.hints = []
        self.defs = []
        self.crossword = []
        self.new_crossword = []
        self.word_by_word(size)  # note I lealize that size is not the best name here bc of the method
        self.words_that_did_not_fit = []
        self.word_indices = self.word_indices()

    def size(self):
        return len(self.crossword),len(self.crossword[0])

    def first_word(self,word):
        self.crossword.append([])
        for c in word:
            self.crossword[0].append(c)

    def __repr__(self):
        output = ""
        for row in self.crossword:
            row = " ".join(row)
            output += f'{row}\n'
        return output

    def truth_statements(self,row_index,column_index):
        output = {}
        output['is_first_row'] = row_index == 0
        if output['is_first_row'] == False:
            output['is_previous_row_free'] = self.crossword[row_index - 1][column_index] == '#'
        else:
            output['is_previous_row_free'] = False
        output['is_last_row'] = len(self.crossword) == row_index + 1
        if output['is_last_row'] == False:
            output['is_next_row_free'] = self.crossword[row_index + 1][column_index] == '#'
        else:
            output['is_next_row_free'] = False
        output['is_first_column'] = column_index == 0
        output['is_last_column'] = column_index +1 >= len(self.crossword[0])
        if output['is_first_column'] == False:
            output['is_previous_column_free'] = self.crossword[row_index][column_index - 1] == '#'
        else:
            output['is_previous_column_free'] = False
        if output['is_last_column'] == False:
            output['is_next_column_free'] = self.crossword[row_index][column_index + 1] == '#'
        else:
            output['is_next_column_free'] = False
        if (output['is_previous_row_free'] or output['is_first_row']) and (output['is_next_row_free'] or output['is_last_row']):
            output['is_previous_and_next_row_free'] = True
        else:
            output['is_previous_and_next_row_free'] = False

        if (output['is_previous_column_free'] or output['is_first_column']) and (output['is_next_column_free'] or output['is_last_column']):
            output['is_previous_and_next_column_free'] = True
        else:
            output['is_previous_and_next_column_free'] = False

        return output

    def check_left_middle_right(self,row_index,column_index,character,i):
        if self.crossword[row_index -i -1][column_index] != '#' and self.crossword[row_index -i -1][column_index] != character:
            return False
        if column_index != 0:
            if self.crossword[row_index + i][column_index -1] != '#':
                return False
        if column_index + 1 < len(self.crossword[0]):
            if self.crossword[row_index + i][column_index +1] != '#':
                return False
        return True

    def check_top_middle_bottom(self,row_index,column_index,character,i):
        if self.crossword[row_index][column_index + i] != '#' and self.crossword[row_index][column_index +i] != character:
            return False
        if row_index != 0:
            if self.crossword[row_index -1][column_index + i] != '#' and self.crossword[row_index][column_index +i] != character:
                return False
        if row_index +1 < len(self.crossword):
            if self.crossword[row_index +1][column_index + i] != '#' and self.crossword[row_index][column_index +i] != character:
                return False
        return True

    def word_fits_vertically(self,word,word_index,row_index,column_index):
        output = True
        truth_statements = self.truth_statements(row_index,column_index)
        if truth_statements['is_previous_and_next_row_free'] == False:
            return False
        word_to_prepend = word[:word_index]
        word_to_append = word[word_index+1:]
        for i,character in enumerate(word_to_prepend):
            if row_index - i - 1 < 0:
                break
            if self.check_left_middle_right(row_index,column_index,character,-i-1) == False:
                return False

        for i,character in enumerate(word_to_append):
            if row_index + i + 1 >= len(self.crossword):
                break
            if self.check_left_middle_right(row_index,column_index,character,i +1) == False:
                return False
        return output

    def word_fits_horizontally(self,word,word_index,row_index,column_index):
        output = True
        truth_statements = self.truth_statements(row_index,column_index)
        if truth_statements['is_previous_and_next_column_free'] == False:
            return False
        word_to_prepend = word[:word_index]
        word_to_append = word[word_index+1:]
        for i,character in enumerate(word_to_prepend):
            if column_index - i - 1 < 0:
                break
            if self.check_top_middle_bottom(row_index,column_index,character,-i -1) == False:
                return False
        for i,character in enumerate(word_to_append):
            if column_index + i + 1 >= len(self.crossword[0]):
                break
            if self.check_top_middle_bottom(row_index,column_index,character,+i +1) == False:
                return False
        return output

    def word_by_word(self, size):
        first_word = next(self.input)  # [word, frequency, hint, definition]
        self.words.append(first_word[0])
        self.hints.append(first_word[2])
        self.defs.append(first_word[3])
        self.first_word(self.words[0])
        self.new_crossword = deepcopy(self.crossword)
        for word in self.input:  # word = [word, frequency, hint, definition]
            if self.add_word(word[0]):  # check if fits, and execute at the same time (double purpose function)
                self.crossword = deepcopy(self.new_crossword)
                self.words.append(word[0])
                self.hints.append(word[2])
                self.defs.append(word[3])
                if len(self.words) == size:
                    break


    def add_word_vertically(self,word,word_index,row_index,column_index):
        word_to_prepend = word[:word_index][::-1]
        word_to_append = word[word_index+1:]
        for i,character in enumerate(word_to_append):
            if row_index + i + 1 >= len(self.crossword):
                row = []
                for i in range(len(self.crossword[0])):
                    if i == column_index:
                        row.append(character)
                    else:
                        row.append('#')
                self.new_crossword.append(row)
            else:
                self.new_crossword[row_index +i +1].pop(column_index)
                self.new_crossword[row_index +i +1].insert(column_index,character)
        for i,character in enumerate(word_to_prepend):
            if row_index - i - 1 < 0:
                row = []
                for i in range(len(self.crossword[0])):
                    if i == column_index:
                        row.append(character)
                    else:
                        row.append('#')
                self.new_crossword.insert(0,row)
            else:
                self.new_crossword[row_index -i -1].pop(column_index)
                self.new_crossword[row_index -i -1].insert(column_index,character)
        return 'Done'

    def add_word_horizontally(self,word,word_index,row_index,column_index):
        word_to_prepend = word[:word_index][::-1]
        word_to_append = word[word_index+1:]

        for i,character in enumerate(word_to_prepend):
            if column_index - i - 1 < 0:
                column_index += 1  # we need to do this, bc the grid changes !!!
                for ind,row in enumerate(self.crossword):
                    if ind == row_index:
                        self.new_crossword[ind].insert(0,character)
                    else:
                        self.new_crossword[ind].insert(0,'#')
            else:
                self.new_crossword[row_index].pop(column_index -i -1)
                self.new_crossword[row_index].insert(column_index -i -1,character)
        for i,character in enumerate(word_to_append):
            if column_index +i +1 >= len(self.new_crossword[0]):  # gotta use the new one, the old one is maybe too small by now
                for ind,row in enumerate(self.crossword):
                    if ind == row_index:
                        self.new_crossword[ind].append(character)
                    else:
                        self.new_crossword[ind].append('#')
            else:
                self.new_crossword[row_index].pop(column_index +i +1)
                self.new_crossword[row_index].insert(column_index + i +1, character)
        return 'Done'

    def add_word(self,word):
        word_index = 0
        for c in word:
            row_index = 0
            for row in self.crossword:
                column_index = 0
                for column in row:
                    if c == column:
                        if self.word_fits_vertically(word,word_index,row_index,column_index):
                            self.add_word_vertically(word,word_index,row_index,column_index)
                            return True  # return true to check whether word has entered the grid or not
                        if self.word_fits_horizontally(word,word_index,row_index,column_index):
                            self.add_word_horizontally(word,word_index,row_index,column_index)
                            return True  # return true to check whether word has entered the grid or not
                    column_index += 1
                row_index += 1
            word_index += 1

    def word_indices(self):
        horizontal_words = ["".join(line) for line in self.crossword]
        vertical_words = []
        for i in range(len(self.crossword[0])):
            vertical_words.append("".join([line[i] for line in self.crossword]))
        indices = {}
        for word in self.words:
            for i,row in enumerate(horizontal_words):
                if word in row:
                    find = re.search(word,row)
                    span = find.span()
                    # indeices for finding first and last letter in the grid
                    indices[word] = (i,span[0]),(i, span[1]-1)
            for i, column in enumerate(vertical_words):
                if word in column:
                    find = re.search(word,column)
                    span = find.span()
                    indices[word] = (span[0], i), (span[1]-1, i)
        return indices

def main():
    words = ['atom','ohm','molecule','electric']
    words1 = ['rate', 'act', 'process', 'director', 'example', 'house', 'hospital', 'science', 'role', 'office']
    words2 = ['john', 'board', 'area', 'name', 'wife', 'energy', 'development', 'way', 'light', 'cup','noam']
    words3 = ['season', 'list', 'president', 'response', 'side', 'term', 'association', 'person', 'charge', 'education']
    words4 = ['help', 'language', 'month', 'college', 'project', 'music', 'act', 'party', 'action', 'unit']
    words5 = ['reason', 'computer', 'project', 'thing', 'history', 'department', 'price', 'sir', 'room', 'man']
    too_close = ['call', 'concept', 'investment', 'element', 'condition', 'water',
                 'list', 'recession', 'damage', 'commitment']  # see how the grid forms water and list/recession...
    obj = crossword_generator((i for i in too_close), 10)
    print(obj.word_indices)
    print(len(obj.word_indices))
    print(obj.words)
    return obj

if __name__ == '__main__':
    print(main())

