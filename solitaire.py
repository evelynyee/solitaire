"""
Klondike Solitaire Game
Evelyn Yee
Fall 2021
"""
import random

#global variables
version = 1.1
notes = "\
- The gameplay is very manual. You will have to enter all of your moves as \
prompted, and there is no auto-complete.\
\r- To play, press enter after you are happy with your response.\
\r- Not every board is playable, due to the rules of solitaire. The dealing is random.\
"
note_lines = notes.count('\r')
heart = '\u2665'
diamond = '\u2666'
spade = '\u2660'
club = '\u2663'
values = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']

# card class
class Card():
    suite = ''
    value = ''
    hidden = False

    def __init__(self, val_in, suite_in):
        self.suite = suite_in
        self.value = val_in
        self.hidden = True
        return

    def __repr__(self):
        if self.hidden == True:
            return '***'
        else:
            if self.value == '10':
                return str(self.value+self.suite)
            else:
                return str(self.value+' '+self.suite)

    def get_suite(self):
        return self.suite

    def get_value(self):
        return self.value

    def get_hidden(self):
        return self.hidden

    def hide(self):
        self.hidden = True
        return

    def show(self):
        self.hidden = False
        return


#game board class
class Board():
    tableau = [] #the card stacks for playing
    foundation = {} #the place to store finished cards (by suite)
    draw = [] #the draw pile
    discard = [] #the dicard pile

    def __init__(self):
        self.tableau = []
        self.foundation = {heart:[], diamond: [], spade:[], club:[]}
        self.draw = []
        self.discard = []
        return

    def get_draw(self):
        return self.draw

    def get_tableau(self):
        return self.tableau

    def get_foundation(self):
        return self.foundation

    def get_discard(self):
        return self.discard

    def set_draw(self, cards):
        """
        sets up the draw pile
        """
        assert isinstance(cards[0], Card), 'not a cards.'
        self.draw = cards.copy()
        return

    def set_tableau(self, cards):
        """
        sets up the tableau
        """
        assert isinstance(cards[0], Card), 'not a cards.'
        counter = 0
        for slot in range(7):
            self.tableau.append([])
            for i in range(slot+1):
                self.tableau[slot].append(cards[counter])
                if i == slot:
                    self.tableau[slot][-1].show()
                counter += 1
        return


    def can_move(self,cards, to_pos):
        """
        checks if a list of cards are in an appropriate order to be moved and if the place on the tableau can receive them.
        """
        assert isinstance(cards[0], Card), 'not a cards.'
        assert isinstance(to_pos, int) and to_pos>=-1, 'invalid column position'
        #check if visible
        for card in cards:
            if card.get_hidden():
                print('All card values must be visible in order to move.')
                return False
        else:
        #check if in order
            if to_pos == -1: #moving to foundation
                if len(cards) != 1:
                    print("Only 1 card may be moved to foundation at a time.")
                    return False
                if len(self.foundation[cards[0].get_suite()]) == 0:
                    if cards[0].get_value() == 'A':
                        return True
                    else:
                        print('First card on foundation must be an Ace.')
                        return False
                else:
                    cards_and_base = [self.foundation[cards[0].get_suite()][-1], cards[0]]
                    if values.index(cards_and_base[0].get_value()) != \
values.index(cards_and_base[1].get_value())-1:
                        return False
            else: #moving to tableau

                #check if to_pos is empty (cards[0] needs to be King)
                if len(self.tableau[to_pos])==0:
                    if cards[0].get_value() != 'K':
                        print ("Only Kings may be moved to empty spaces.")
                        return False
                cards_and_base = []
                cards_and_base.append(self.tableau[to_pos][-1])
                cards_and_base.extend(cards)
                prev_i = 13
                for card in cards_and_base:
                    if len(cards_and_base) != 1:
                        i = values.index(card.get_value())
                        if prev_i == 13:
                            prev_i = i
                            continue
                        else:
                            if prev_i == i+1:
                                prev_i = i
                            else:
                                print('Cards and base must be in order to move.')
                                return False
                #check if cards[0] suite opposite color as last card on to_pos
                if (cards_and_base[0].get_suite() in [heart, diamond]) \
and (cards_and_base[1].get_suite() in [heart, diamond]):
                    print('Cards cannot be moved onto a card of the same color.')
                    return False
                elif (cards_and_base[0].get_suite() in [spade, club]) \
and (cards_and_base[1].get_suite() in [spade, club]):
                    print('Cards cannot be moved onto a card of the same color.')
                    return False
        return True


    def move_cards(self, from_loc, num_cards, to_loc,\
from_pos = -1, to_pos= -1):
        """
        adjusts the game board when a card (or stack of cards) is moveed into the tableau or foundation, from the foundation, tableau, or discard
        """
        assert num_cards >= 0, "negative cards selected"
        if num_cards > 1: #moving multiple cards
            assert to_loc == 't' and from_loc == 't', \
"invalid card movement"
            assert from_pos > -1, "from column not specified"
            assert to_pos > -1, "to column not specified"
            if len(self.tableau[from_pos]) < num_cards:
                print ("There are not enough cards in that column.")
                return
            cards = self.tableau[from_pos][-num_cards:]
            if self.can_move(cards, to_pos):
                self.tableau[to_pos].extend(cards)
                del self.tableau[from_pos][-num_cards:]
                if len(self.tableau[from_pos]) > 0:
                    self.tableau[from_pos][-1].show()
            else: #invalid move
                return

        else: #moving one card
            if from_loc == "f":
                assert from_pos in [heart, diamond, spade, club], \
"foundation suite not specified"
                if len(self.foundation[from_pos]) < num_cards:
                    print('That space on the foundation is empty.')
                    return
                card = self.foundation[from_pos][-1]
                if not self.can_move([card], to_pos):
                    return
                del self.foundation[from_pos][-1]
            elif from_loc == "t":
                assert from_pos > -1, "from column not specified"
                if len(self.tableau[from_pos]) < num_cards:
                    print ("There are not enough cards in that column.")
                    return
                card = self.tableau[from_pos][-1]
                if not self.can_move([card], to_pos):
                    return
                del self.tableau[from_pos][-1]
                if len(self.tableau[from_pos]) > 0:
                    self.tableau[from_pos][-1].show()
            elif from_loc == 'd':
                if len(self.tableau[from_pos]) < num_cards:
                    print ("The discard is empty. Flip another card to fill it.")
                    return
                card = self.discard[-1]
                if not self.can_move([card], to_pos):
                    return
                del self.discard[-1]
            else:
                print("error: invalid card removal")

            if to_loc == 'f':
                self.foundation[card.get_suite()].append(card)
            elif to_loc == 't':
                assert to_pos > -1, "to column not specified"
                self.tableau[to_pos].append(card)
            else:
                print("error: invalid card placement")
        return


    def flip_up(self):
        """
        Flips up the top (first index) card from the draw pile.
        Makes it show and moves it to the discard (last index).
        If all cards are in discard, cycles discard back into draw
        """
        if len(self.draw) == 0:
            for card in self.discard:
                card.hide()
                self.draw.append(card)
            self.discard.clear()
        else:
            self.discard.append(self.draw[0])
            self.discard[-1].show()
            self.draw = self.draw[1:]
        return


    def game_won(self):
        """
        checks to see if game has been won
        """
        for suite in self.foundation:
            if len(self.foundation[suite]) != 13:
                return False
        return True


    def display(self):
        """
        prints a visual representation of the current board
        """
        print("Foundation:", end=" ")
        for suite in self.foundation:
            if len(self.foundation[suite]) == 0:
                print ('[ '+suite+' ]', end = " ")
            else:
                print ('['+str(self.foundation[suite][-1])+']', end = " ")
        print()

        if len(self.discard) == 0:
            print("Discard: [   ]", end = ' ')
        else:
            print("Discard: ["+str(self.discard[-1])+']', end = ' ')

        if len(self.draw) == 0:
            print("Draw: [   ]")
        else:
            print("Draw: ["+str(self.draw[0])+']')

        print()
        print(' |__'+'__|__'.join([str(i) for i in range(7)])+'__| ')
        longest_col = 0
        for col in self.tableau:
            if len(col) > longest_col:
                longest_col = len(col)

        for row in range(longest_col):
            print('', end = ' | ')
            for col in self.tableau:
                if row < len(col):
                    print(col[row], end = ' | ')
                else:
                    print('   ', end = ' | ')
            print()
        return


def main():
    def build_deck():
        """
        Generates the deck (list) of 52 cards, no jokers.
        >>> print(build_deck())
        [A ♥, 2 ♥, 3 ♥, 4 ♥, 5 ♥, 6 ♥, 7 ♥, 8 ♥, 9 ♥, 10♥, J ♥, Q ♥, K ♥, \
    A ♦, 2 ♦, 3 ♦, 4 ♦, 5 ♦, 6 ♦, 7 ♦, 8 ♦, 9 ♦, 10♦, J ♦, Q ♦, K ♦, \
    A ♠, 2 ♠, 3 ♠, 4 ♠, 5 ♠, 6 ♠, 7 ♠, 8 ♠, 9 ♠, 10♠, J ♠, Q ♠, K ♠, \
    A ♣, 2 ♣, 3 ♣, 4 ♣, 5 ♣, 6 ♣, 7 ♣, 8 ♣, 9 ♣, 10♣, J ♣, Q ♣, K ♣]
        """
        deck = []
        for suite in [heart,diamond,spade,club]:
            for value in values:
                deck.append(Card(value,suite))
        return deck


    def count_showing(cards):
        """
        Counts how many cards in a list are showing. (hidden==False)
        """
        return sum([not card.get_hidden() for card in cards])


    def rules():
        """
        Prints rules in an interactive way.
        Major credits to bicyclecards.com/how-to-play/klondike/ for the rules.
        """
        print("This solitaire game uses a standard 52-card deck (no jokers).\
\n\rIn the set-up, 28 cards are dealt out into the 'tableau' in 7 columns, \
and the rest of the cards are placed in the draw pile.\
\n\rThe top card of each column is flipped up (looks like [A \u2660]),\
but all other cards are face down (looks like [***])\
\n\rAt the top of the board is the 'foundation', with one stack for each suit.\
\n\rThe game board looks like this:", 0, 0)
        demo_deck = build_deck()
        demo_board = Board()
        demo_board.set_tableau(demo_deck)
        demo_deck = demo_deck[28:]
        demo_board.set_draw(demo_deck)
        demo_board.display()

        input("Press enter to continue.")

        print("The goal of the game is to get all cards of all four suits built up onto the foundation, from Ace to King.\
\n\rAs cards of each suit are flipped up, they may be moved onto the foundation in order by their value.\
\n\rAny face-up card (including those on the foundation) may be placed on a card that has a value 1-higher and a suit of the opposite color. (Hearts and diamonds are red, and spades and clubs are black.)\
\n\rFor example, [5 \u2665] can be moved onto [6 \u2663] but not [7 \u2660], [5 \u2663], or [6 \u2666]. \
\n\rMultiple face-up cards may be moved together, following the same rules. \
\n\rThe bottom card of each column of the tableau is always flipped to be face-up. \
\n\rIf there is an empty column in the tableau, only a King may be moved onto it.", 0, 8)

        input("Press enter to continue.")

        print("Cards may be flipped up from the draw pile into the discard, where they may be played onto the tableau or foundation. \
\n\rIf the draw pile runs out, the discard is flipped directly back over into the draw, without being shuffled.\
\n\rTo take a turn, follow the prompts given to you.", 0, 17)
        repeat = ''
        while repeat not in ['y','n']:
            input("Would you like that repeated? [y/n]")
        if repeat == 'n':
            return
        else:
            rules()


    deck = build_deck()
    random.shuffle(deck)
    game_board = Board()
    game_board.set_tableau(deck)
    deck = deck[28:]
    game_board.set_draw(deck)

    input(f"Welcome to Evi's Klondike solitaire game, version {version}! \
Before you play, here are some notes:\n\r{notes}")

    read_rules = ''
    while read_rules not in ['y','n']:
        read_rules = input("Are you familiar with the rules to solitaire and this system? [y/n]")

    if read_rules == 'n':
        rules()

    input("Press enter to continue.")

    playing = True

    while playing:
        if game_board.game_won():
            print ('Congratulations! You won!')
            playing = False
            continue
        print()
        game_board.display()
        task = input("Press 'f' to flip the next card from the draw pile. \
Press 'm' to move a card. Press 'e' to end the game.")
        if task == 'e':
            playing = False
            break
        elif task == 'f':
            game_board.flip_up()
        elif task == 'm':
            from_loc = ''
            while from_loc not in ('d','t','f','b','e'): #get from_loc
                from_loc = input("Where would you like to move a card from?\
\nPress 'd' for discard, 't' for tableau, 'f' for foundation, 'b' to go back, or 'e' to end the game.")
            if from_loc == 'b': # go back
                continue
            elif from_loc == 'e': # exit
                playing = False
                continue
            else: # move a card
                if from_loc == 'f': # move from foundation
                    from_pos = ''
                    while from_pos not in ['h','d','s','c','b','e']:
                        from_pos = input("Which suit would you like to move from?\n\rType the name of the suit (h/d/s/c) or 'b' to go back or 'e' to end the game.")
                    if from_pos == 'b':
                        continue
                    elif from_pos == 'e':
                        playing = False
                        continue
                    elif from_pos == 'h':
                        from_pos = heart
                    elif from_pos == 'd':
                        from_pos = diamond
                    elif from_pos == 's':
                        from_pos = spade
                    else:
                        from_pos = club
                if from_loc == 't': # move from tableau
                    from_pos = ''
                    while from_pos not in ['0','1','2','3','4','5','6','b','e']:
                        from_pos = input("Which column would you like to move from? (0 is the far left, and 6 is the far right.)\n\rEnter a number (0-6), press 'b' to go back, or press 'e' to end the game.")
                    if from_pos == 'b':
                        continue
                    elif from_pos == 'e':
                        playing = False
                        continue
                    else:
                        from_pos = int(from_pos)
                    good_val = False
                    while not good_val: #get num_cards
                        available = count_showing(game_board.get_tableau()[from_pos])
                        num_cards = input("How many cards would you like to move? There are "+str(available)+" cards showing in that column.\n\rEnter a number, press 'b' to go back, or press 'e' to end the game.")
                        if num_cards == 'b':
                            break
                        elif num_cards == 'e':
                            playing = False
                            break
                        else:
                            try:
                                num_cards = int(num_cards)
                                if num_cards >= 0 and num_cards <= available:
                                    good_val = True
                            except ValueError:
                                continue
                    if num_cards == 'b':
                        continue
                    elif num_cards == 'e':
                        playing = False
                        continue
                else:
                    num_cards = 1 # this is a dumb place to put this, but it's what I've got.
                to_loc = ''
                while to_loc not in ('t','f','b','e'): #get to_loc
                    to_loc = input("Where would you like to move the card(s) to?\
\nPress 't' for tableau, 'f' for foundation, 'b' to go back, or 'e' to end the game.")
                if to_loc == 'b':
                    continue
                elif to_loc == 'e':
                    playing = False
                    continue
                else:
                    if to_loc == 't':
                        to_pos = ''
                        while to_pos not in ['0','1','2','3','4','5','6','b','e']:
                            to_pos = input("Which column would you like to move the card(s) to? \
(0 is the far left, and 6 is the far right.)\
\nEnter a number (0-6) or press 'e' to end the game.")
                        if to_pos == 'b':
                            continue
                        elif to_pos == 'e':
                            playing = False
                            continue
                        else:
                            to_pos = int(to_pos)

            if from_loc in ['t','f'] and to_loc == 't':
                game_board.move_cards(from_loc, num_cards, to_loc, from_pos = from_pos, to_pos = to_pos)
            elif from_loc in ['t','f']:
                game_board.move_cards(from_loc, num_cards, to_loc, from_pos = from_pos)
            elif to_loc == 't':
                game_board.move_cards(from_loc, num_cards, to_loc, to_pos = to_pos)
            else:
                game_board.move_cards(from_loc, num_cards, to_loc)
        else:
            input("invalid input. Try again?")


    #game end
    replay = input("Thank you for playing! Would you like to play again? [y/n]")
    if replay == 'y':
        main()
    else:
        return None

if __name__ == "__main__":
    main()
