from typing import List
from typing import Union

class Card:
    """
    Card class for holding question and answer information.
    """

    def __init__(self, Q: str = "", A: str = "") -> None:
        """
        Initializes an instance of the Card class, and assigns values for the
        question (Q) and answer (A). Both default to an empty string.
        """
        self.Q = Q
        self.A = A


    def copy(self) -> "Card":
        """
        Returns a new instance of the Card class with the same values as the
        current instance.
        """
        return Card(self.Q, self.A)


class Deck:
    """
    Deck class for holding a collection of cards.
    """

    def __init__(self) -> None:
        """
        Initializes an instance of the Deck class, and creates an empty list of
        Card objects.
        """
        self.card_collection = []


    def __len__(self) -> int:
        """
        Returns the number of Card objects in this instance of the Deck class.
        """
        return len(self.card_collection)


    def add(self, card: Union[Card, list]) -> None:
        """
        Adds a copy of the given Card object to the card_collection in this
        instance of the Deck class.
        """
        if isinstance(card, Card):
            self.card_collection.append(card.copy())
        elif isinstance(card, list):
            for item in card:
                if not isinstance(item, Card):
                    msg = "The given argument was not of the Card type."
                    raise TypeError(msg)
                
                self.card_collection.append(item.copy())
        else:
            msg = "The given argument was not of the Card or the list type."
            raise TypeError(msg)
        
        

    def copy(self) -> "Deck":
        """
        Returns a new instance of the Deck class with the copies of the Card
        objects that are in the current instance.
        """
        copy_deck = Deck()
        

class Quiz:
    """
    Quiz class for holding one instance of questions and answers.
    """

    def __init__(self, deck: Union[Deck,List[Deck]] = Deck()) -> None:
        """
        Initializes an instance of the Quiz class, and creates a new Deck object
        that is specific to this instance of the Quiz class. Pass a Deck object
        or list of Deck objects to add decks to this instance of the Quiz class.
        """
        if isinstance(deck, Deck):
            self.deck_collection = [deck]
        elif isinstance(deck, list):
            if len(deck) == 0:
                raise ValueError("The given argument was an empty list.")
            
            self.deck_collection = []
            
            for item in deck:
                if not isinstance(item, Deck):
                    msg = "The given argument was a list that contained at " \
                        "least one item that was not of the Deck type."
                    raise TypeError(msg)
                
                self.deck_collection += item
        else:
            msg = "The given argument was not of the Deck or the list type"
            raise TypeError(msg)
        

    def __len__(self) -> int:
        """
        Returns the sum of all Card objects contained in all of the Deck objects
        contained in this instance of the Quiz class.
        """
        return sum([len(deck_item) for deck_item in self.deck_collection])


def take_quiz(quiz: Quiz) -> None:
    """
    Shows a random order of questions contained in the given Quiz object to the
    user, and compares the user's inputs to the answers.
    """
    pass