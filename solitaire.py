# Solitaire: Seahaven


import cards, random

random.seed(100)  # random number generator will always generate

MENU = '''     
Input options:
    MTT s d: Move card from end of Tableau column s to end of column d.
    MTC s d: Move card from end of Tableau column s to Cells d.
    MCT s d: Move card from Cells s to end of Tableau column d.
    MTF s d: Move card from end of Tableau column s to Foundation d.
    MCF s d: Move card from end of Cell s to Foundation d.
    R: Restart the game (after shuffling)
    H: Display this menu of choices
    Q: Quit the game       
'''


def initialize():
    '''
        This function calls the Deck class from cards to shuffle and deal 52
        cards, 50 cards dealt evenly into the 10 nested lists in the tableau list and the
        remaining 2 cards into the cells list and creates the foundation list.

        return: tup (tableau, foundation, cells)
    '''
    foundation = [[], [], [], []]
    tableau = [[], [], [], [], [], [], [], [], [], []]
    cells = []
    cards_list = []
    deck = cards.Deck()
    deck.shuffle()
    cards_list = [deck.deal() for i in range(52)]  # place full deck into a list
    # sort 50 cards into each list into tableau one by one
    for lst in tableau:
        list_count = 0
        index = 0
        while len(lst) <= 5:
            tableau[list_count].append(cards_list[index])
            list_count += 1
            index += 1
            if list_count == 10:
                list_count = 0
    # make sure each list in tableau has 5 cards
    new_tab = []
    for lst in tableau:
        new_lst = lst[:5]
        new_tab.append(new_lst)
    tab_lst = []  # list of 50 cards in tableau, to get the 2 remaining cards
    for lst in new_tab:
        for card in lst:
            tab_lst.append(card)
    for card in cards_list:
        if card not in tab_lst:
            cells.append(card)
    cells.append(None)
    final_cells = [None] + cells[:]
    tup = (new_tab, foundation, final_cells)
    return tup



def display(tableau, foundation, cells):
    '''Display the cell and foundation at the top.
       Display the tableau below.'''

    print("\n{:<11s}{:^16s}{:>10s}".format("foundation", "cell", "foundation"))
    print("{:>14s}{:>4s}{:>4s}{:>4s}".format("1", "2", "3", "4"))
    for i, f in enumerate(foundation):
        if f and (i == 0 or i == 1):
            print(f[-1], end=' ')  # print first card in stack(list) on foundation
        elif i == 0 or i == 1:
            print("{:4s}".format(" "),
                  end='')  # fill space where card would be so foundation gets printed in the right place
    print("{:3s}".format(' '), end='')
    for c in cells:
        if c:
            print(c, end=' ')  # print first card in stack(list) on foundation
        else:
            print("[  ]", end='')  # fill space where card would be so foundation gets printed in the right place
    print("{:3s}".format(' '), end='')
    for i, f in enumerate(foundation):
        if f and (i == 2 or i == 3):
            print(f[-1], end=' ')  # print first card in stack(list) on foundation
        elif i == 2 or i == 3:
            print("{}{}".format(" ", " "),
                  end='')  # fill space where card would be so foundation gets printed in the right place

    print()
    print("\ntableau")
    print("   ", end=' ')
    for i in range(1, 11):
        print("{:>2d} ".format(i), end=' ')
    print()
    # determine the number of rows in the longest column
    max_col = max([len(i) for i in tableau])
    for row in range(max_col):
        print("{:>2d}".format(row + 1), end=' ')
        for col in range(10):
            # check that a card exists before trying to print it
            if row < len(tableau[col]):
                print(tableau[col][row], end=' ')
            else:
                print("   ", end=' ')
        print()  # carriage return at the end of each row
    print()  # carriage return after printing the whole tableau

def convert_card(card):
    '''
        This function converts a card that does not
        have a numeric value into a numeric value.

        card: string
        return: string
    '''
    if card == "K":   # change king card to value of 13
        card = card.replace("K", "13")
    if card == "Q":   # change Queen card to value of 12
        card = card.replace("Q", "12")
    if card == "J":   # change Jack card to value of 11
        card = card.replace("J", "11")
    if card == "A":   # change Ace card to value of 1
        card = card.replace("A", "1")
    return card

def validate_move_within_tableau(tableau, src_col, dst_col):
    '''
        This function checks to see if a card can be moved
        from the end of a specified column into the end of another
        specified column within the tableau.

        tableau: nested list
        src_col: int
        dst_col: int
        return: bool
    '''
    if tableau[src_col] == []:  # check if card exists
        return False
    source_str = ""   # source card as str
    destination_str = ""  # destination card as str
    source = str(tableau[src_col][-1])  # convert source card into str
    source_str += source
    source_str = source_str.replace(" ", "")

    # if destination column is empty, only king is allowed
    if tableau[dst_col] == []:
        if source_str[0] == "K":
            return True
        else:
            return False

    destination = str(tableau[dst_col][-1])  # convert destination card into str
    destination_str += destination
    destination_str = destination_str.replace(" ", "")

    # check to see if symbols match up
    if source_str[-1] == destination_str[-1]:
        # if card is king, queen, ace, or jack, convert to numeric value
        if source_str[0] in "KQJA":
            c = convert_card(source_str[0])
            source_str = source_str.replace(source_str[0], str(c))
        if destination_str[0] in "KQJA":
            c = convert_card(destination_str[0])
            destination_str = destination_str.replace(destination_str[0], str(c))
        # get numeric values of both cards, so they can be compared
        source_lst = [source_str[0:-1], source_str[-1]]  # convert str to list, in case of double digits
        destination_lst = [destination_str[0:-1], destination_str[-1]]
        source_num = int(source_lst[0])
        destination_num = int(destination_lst[0])

        if source_num + 1 == destination_num:  # check numeric values
            return True
        else:
            return False
    else:
        return False



def validate_move_cell_to_tableau(tableau, cells, cell_no, dst_col):
    '''
        This function check to see if a specified card from the cell
        can be moved to the end of a specified column in the tableau.

        tableau: nested list
        cells: list
        cell_no: int
        dst_col: int
        return: bool
    '''
    if cells[cell_no] == None:  # check if card exists
        return False
    cells_str = str(cells[cell_no])  # card from cell as str
    cells_str = cells_str.replace(" ", "")
    # if destination column is empty, only king is allowed
    if tableau[dst_col] == []:
        if cells_str[0] == "K":
            return True
        else:
            return False
    destination_str = str(tableau[dst_col][-1])  # destination card as str
    destination_str = destination_str.replace(" ", "")

    # check if symbols match
    if cells_str[-1] == destination_str[-1]:
        # if card is king, queen, ace, or jack, convert to numeric value
        if cells_str[0] in "KQJA":
            c = convert_card(cells_str[0])
            cells_str = cells_str.replace(cells_str[0], str(c))
        if destination_str[0] in "KQJA":
            c = convert_card(destination_str[0])
            destination_str = destination_str.replace(destination_str[0], str(c))

        # get card from cell and destination values, so they can be compared
        cells_lst = [cells_str[0:-1], cells_str[-1]]  # convert str to list, in case of double digits
        cells_num = int(cells_lst[0])
        destination_lst = [destination_str[0:-1], destination_str[-1]]
        destination_num = int(destination_lst[0])

        if cells_num + 1 == destination_num:  # check values of cards
            return True
        else:
            return False
    else:
        return False




def validate_move_tableau_to_cell(tableau, cells, src_col, cell_no):
    '''
        This function checks to see if a card from the end of a
        specified column in the tableau can be moved into the cell.

        tableau: nested list
        cells: list
        src_col: int
        cell_no: int
        return: bool
    '''
    if tableau[src_col] == []:  # check if card exists
        return False

    if cells[cell_no] == None:  # check if cell is empty
        return True
    else:
        return False



def validate_move_tableau_to_foundation(tableau, foundation, src_col, found_no):
    '''
        This function checks to see if a card from the end of a
        specified column in the tableau can be moved into a specified
        list within the foundation.

        tableau: nested list
        foundation: nested list
        src_col: int
        found_no: int
        return: bool
    '''

    if tableau[src_col] == []: # check of card exists
        return False

    source_str = str(tableau[src_col][-1])  # source card as str
    source_str = source_str.replace(" ", "")
    # check if foundation is empty and if card is ace
    if foundation[found_no] == []:
        if source_str[0] == "A":
            return True
        else:
            return False

    foundation_str = str(foundation[found_no][-1])  # last foundation card as str
    foundation_str = foundation_str.replace(" ", "")
    # check symbols of the two cards
    if foundation_str[-1] == source_str[-1]:
        # if card is king, queen, ace, or jack, convert to numeric value
        if source_str[0] in "KQJA":
            c = convert_card(source_str[0])
            source_str = source_str.replace(source_str[0], str(c))
        if foundation_str[0] in "KQJA":
            c = convert_card(foundation_str[0])
            foundation_str = foundation_str.replace(foundation_str[0], str(c))
        # get the numeric value of source and foundation card, so they can be compared
        source_lst = [source_str[0:-1], source_str[-1]]  # convert str to list, in case of double digits
        source_num = int(source_lst[0])
        foundation_lst = [foundation_str[0:-1], foundation_str[-1]]
        foundation_num = int(foundation_lst[0])
        if source_num - 1 == foundation_num:  # check values of cards
            return True
        else:
            return False
    else:
        return False



def validate_move_cell_to_foundation(cells, foundation, cell_no, found_no):
    '''
        This function checks to see if a card from the cell can
        be moved into a specified list within the foundation.

        cells: list
        foundation: nested list
        cell_no: int
        found_no: int
        return: bool
    '''
    try:
        if cells[cell_no] == None:  # check if card exists
            return False
    except:
        return False

    cell_str = str(cells[cell_no])  # cell card as str
    cell_str = cell_str.replace(" ", "")
    # check if foundation is empty and if card is ace
    if foundation[found_no] == []:
        if cell_str[0] == "A":
            return True
        else:
            return False

    foundation_str = str(foundation[found_no][-1])  # last foundation card as string
    foundation_str = foundation_str.replace(" ", "")
    # check symbols of foundation and cell cards
    if foundation_str[-1] == cell_str[-1]:
        # if card is king, queen, ace, or jack, convert to numeric value
        if cell_str[0] in "KQJA":
            c = convert_card(cell_str[0])
            cell_str = cell_str.replace(cell_str[0], str(c))
        if foundation_str[0] in "KQJA":
            c = convert_card(foundation_str[0])
            foundation_str = foundation_str.replace(foundation_str[0], str(c))
        # get numeric values of cell and foundation cards, so they can be compared
        cell_lst = [cell_str[0:-1], cell_str[-1]]  # convert str to list, in case of double digits
        cell_num = int(cell_lst[0])
        foundation_lst = [foundation_str[0:-1], foundation_str[-1]]
        foundation_num = int(foundation_lst[0])

        if cell_num - 1 == foundation_num:  # check values
            return True
        else:
            return False
    else:
        return False





def move_within_tableau(tableau, src_col, dst_col):
    '''
        This function calls a function to verify that
        the card can be moved and updates the tableau display.

        tableau: nested list
        src_col: int
        dst_col: int
        return: bool
    '''
    condition = validate_move_within_tableau(tableau, src_col, dst_col)
    if condition:
        # update tableau
        tableau[dst_col].append(tableau[src_col][-1])
        tableau[src_col].pop()
        return True
    else:
        return False


def move_tableau_to_cell(tableau, cells, src_col, cell_no):
    '''
        This function calls function to verify that the card can be
        moved and updates the cells and tableau displays.

        tableau: nested list
        cells: list
        src_col: int
        cell_no: int
        return: bool
    '''

    condition = validate_move_tableau_to_cell(tableau, cells, src_col, cell_no)
    if condition:
        # update tableau and cells
        cells[cell_no] = tableau[src_col][-1]
        tableau[src_col].pop()
        return True
    else:
        return False


def move_cell_to_tableau(tableau, cells, cell_no, dst_col):
    '''
        This function calls function to verify that the card can
        be moved and updates the tableau and cells displays.

        tableau: nested list
        cells: list
        cell_no: int
        dst_col: int
        return: bool
    '''
    condition = validate_move_cell_to_tableau(tableau, cells, cell_no, dst_col)
    if condition:
        # update tableau and cells
        tableau[dst_col].append(cells[cell_no])
        cells[cell_no] = None
        return True
    else:
        return False

def move_cell_to_foundation(cells, foundation, cell_no, found_no):
    '''
        This function calls function to verify that the card
        can be moved and updates the cells and foundation displays.

        cells: list
        foundation: nested list
        cell_no: int
        param found_no: int
        return: bool
    '''
    condition = validate_move_cell_to_foundation(cells, foundation, cell_no, found_no)
    if condition:
        # update cells and foundation
        foundation[found_no].append(cells[cell_no])
        cells[cell_no] = None
        return True
    else:
        return False


def move_tableau_to_foundation(tableau, foundation, src_col, found_no):
    '''
        This function calls function to verify that card
        can be moved and updates the tableau and foundation
        displays.

        tableau: nested list
        foundation: nested list
        src_col: int
        found_no: int
        return: bool
    '''
    condition = validate_move_tableau_to_foundation(tableau, foundation, src_col, found_no)
    if condition:
        # update tableau and foundation
        foundation[found_no].append(tableau[src_col][-1])
        tableau[src_col].pop()
        return True
    else:
        return False


def check_for_win(foundation):
    '''
        This function checks to see if all 52 cards are
        in the foundation to see if user has won.

        foundation: nested list
        return: bool
    '''
    count = 0  # count of cards in foundation list
    for lst in foundation:
        for card in lst:
            count += 1
    if count == 52:  # check if all cards in deck are in foundation
        return True
    else:
        return False



def get_option():
    '''Prompt the user for an option and check that the input has the
       form requested in the menu, printing an error message, if not.
       Return:
    MTT s d: Move card from end of Tableau column s to end of column d.
    MTC s d: Move card from end of Tableau column s to Cells d.
    MCT s d: Move card from Cells s to end of Tableau column d.
    MTF s d: Move card from end of Tableau column s to Foundation d.
    MCF s d: Move card from Cells s to Foundation d.
    R: Restart the game (after shuffling)
    H: Display this menu of choices
    Q: Quit the game
    '''
    option = input("\nInput an option (MTT,MTC,MCT,MTF,MCF,R,H,Q): ")
    option_list = option.strip().split()

    opt_char = option_list[0][0].upper()

    if opt_char in 'RHQ' and len(option_list) == 1:  # correct format
        return [opt_char]

    if opt_char == 'M' and len(option_list) == 3 and option_list[1].isdigit() \
            and option_list[2].isdigit():
        opt_str = option_list[0]
        if opt_str in ['MTT', 'MTC', 'MCT', 'MTF', 'MCF']:
            return [opt_str, int(option_list[1]), int(option_list[2])]

    print("Error in option:", option)
    return None  # none of the above


def main():
    ''' main '''
    print("\nWelcome to Seahaven Solitaire.\n")
    tableau, foundation, cells = initialize()
    display(tableau, foundation, cells)
    print(MENU)
    option = get_option()
    if option == None:
        option = get_option()  # ask user for another option if get_option returns None
    # loop function for user input
    while option != None:
        if option[0] == "MTC":
            # verify move and update display
            move = move_tableau_to_cell(tableau, cells, option[1] - 1, option[2] - 1)
            if move:
                win = check_for_win(foundation) # check if user won after every move
                if win:
                    print("You won!")
                    display(tableau, foundation, cells)
                    print("\n- - - - New Game. - - - -")
                    tableau, foundation, cells = initialize()  # start new game if user won
                    display(tableau, foundation, cells)
                    print(MENU)
                    pass  # don't display again if user won
                display(tableau, foundation, cells)  # only display if move is valid

            else:  # display error if move can't be done
                print("Error in move: " + option[0] + " , " + str(option[1]) + " , " + str(option[2]))

        # all options follow the same structure

        if option[0] == "MTT":
            move = move_within_tableau(tableau, option[1] - 1, option[2] - 1)
            if move:
                win = check_for_win(foundation)
                if win:
                    print("You won!")
                    display(tableau, foundation, cells)
                    print("\n- - - - New Game. - - - -")
                    tableau, foundation, cells = initialize()
                    display(tableau, foundation, cells)
                    print(MENU)
                    pass
                display(tableau, foundation, cells)
            else:
                print("Error in move: " + option[0] + " , " + str(option[1]) + " , " + str(option[2]))

        if option[0] == "MCF":
            move = move_cell_to_foundation(cells, foundation, option[1] - 1, option[2] - 1)
            if move:
                win = check_for_win(foundation)
                if win:
                    print("You won!")
                    display(tableau, foundation, cells)
                    print("\n- - - - New Game. - - - -")
                    tableau, foundation, cells = initialize()
                    display(tableau, foundation, cells)
                    print(MENU)
                    pass
                display(tableau, foundation, cells)
            else:
                print("Error in move: " + option[0] + " , " + str(option[1]) + " , " + str(option[2]))

        if option[0] == "MTF":
            move = move_tableau_to_foundation(tableau, foundation, option[1] - 1, option[2] - 1)
            if move:
                win = check_for_win(foundation)
                if win:
                    print("You won!")
                    display(tableau, foundation, cells)
                    print("\n- - - - New Game. - - - -")
                    tableau, foundation, cells = initialize()
                    display(tableau, foundation, cells)
                    print(MENU)
                    pass
                display(tableau, foundation, cells)
            else:
                print("Error in move: " + option[0] + " , " + str(option[1]) + " , " + str(option[2]))

        if option[0] == "MCT":
            move = move_cell_to_tableau(tableau, cells, option[1] - 1, option[2] - 1)
            if move:
                win = check_for_win(foundation)
                if win:
                    print("You won!")
                    display(tableau, foundation, cells)
                    print("\n- - - - New Game. - - - -")
                    tableau, foundation, cells = initialize()
                    display(tableau, foundation, cells)
                    print(MENU)
                    pass
                display(tableau, foundation, cells)
            else:
                print("Error in move: " + option[0] + " , " + str(option[1]) + " , " + str(option[2]))

        if option[0] == "H":  # print Menu
            print(MENU)
        if option[0] == "Q":  # exit game
            break
        if option[0] == "R":  # restart game
            tableau, foundation, cells = initialize()
            display(tableau, foundation, cells)
            print(MENU)

        option = get_option()  # display option after every move

    print("Thank you for playing.")



if __name__ == '__main__':
    main()

