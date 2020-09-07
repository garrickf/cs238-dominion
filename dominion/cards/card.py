""" Card class TODO: docstring
"""

from abc import ABC, abstractmethod
from dominion.common import CardType


class Card(ABC):
    def __init__(self, *, name, kind, cost, desc=""):
        """ Constructs a card.

        @param name (str): The card's name
        @param kind (dominion.common.CardType) Card type
        @param cost (int): Treasure cost of the card
        @param desc (str): Description on the card, if written
        """
        self.name = name
        self.kind = kind
        self.cost = cost
        self.description = desc

    def __str__(self):
        """ Returns a string representation of the card; useful during gameplay.
        """
        return '[{}]'.format(self.name)

    @property
    def desc(self):
        if self.description:
            return self.description
        elif self.kind == CardType.VICTORY:
            return f'Victory card worth %s VP.' % (self.vp)
        elif self.kind == CardType.TREASURE:
            return f'Treasure card worth %s.' % (self.value)
        elif self.kind == CardType.CURSE:
            return f'%s VP for each held.' % (self.vp)


class TreasureCard(Card):
    def __init__(self, *, name, cost, desc="", value):
        super().__init__(name=name,
                         kind=CardType.TREASURE,
                         cost=cost,
                         desc=desc)
        self.value = value


class VictoryCard(Card):
    def __init__(self, *, name, cost, desc="", vp):
        super().__init__(name=name,
                         kind=CardType.VICTORY,
                         cost=cost,
                         desc=desc)
        self.vp = vp


class ActionCard(Card):
    def __init__(self, *, name, cost, desc=""):
        super().__init__(name=name, kind=CardType.ACTION, cost=cost, desc=desc)

    @abstractmethod
    def play(self, by, game_ctx):
        pass