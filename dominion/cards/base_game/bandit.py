"""Bandit: Gain a Gold. Each other player reveals the top 2 cards of their deck,
trashes a revealed treasure other than Copper, and discards the rest.
"""

# From dominion module
from dominion.cards import ActionCard
from dominion.common import DeckPile, QueuePosition
from dominion.events import Event
from dominion.prettyprint import card_to_str, cards_to_str, options_to_str

from .gold import GOLD
from .silver import SILVER


def get_treasures_as_options(cards):
    """Takes a list of cards and returns a dict from index to string option"""
    options = {}
    for idx, card in enumerate(cards):
        if card in [GOLD, SILVER]:
            options[idx] = card.name
    return options


class BanditEventSelf(Event):
    def forward(self, game_ctx, player):
        if game_ctx.table[GOLD] > 0:
            game_ctx.table.buy(GOLD, player, free=True, to_pile=DeckPile.DISCARD)
            print(f"Player acquired a {card_to_str(GOLD)}")
        else:
            player.show("There are no more Golds in the Supply.")


class BanditEventOther(Event):
    def forward(self, game_ctx, player):
        top_cards = player.deck.draw_cards(n=2, to_caller=True)
        print(f"Player reveals top two cards: {cards_to_str(top_cards)}")

        if any(treasure in top_cards for treasure in [GOLD, SILVER]):
            options = get_treasures_as_options(top_cards)
            player.show(options_to_str(options))
            prompt_str = "You must trash a treasure other than Copper"
            c = player.get_input(prompt_str, options, allow_skip=False)

            # By not adding the card to discard, it's implicitly trashed.
            # Add will update counts
            del top_cards[c]
            print(f"Player trashes {options[c]}")

        player.deck.add(top_cards, to_pile=DeckPile.DISCARD)


# TODO: subclass as ActionAttackCard
class Bandit(ActionCard):
    def __init__(self):
        super().__init__(
            name="Bandit",
            cost=5,
            desc=(
                "Gain a Gold. Each other player reveals the top 2 cards of their"
                " deck, trashes a revealed treasure other than Copper, and"
                " discards the rest."
            ),
        )

    def play(self, game_ctx, player):
        events = [BanditEventSelf(target=player.name)]

        # TODO: clarify between player names and objects
        for other_player_name in game_ctx.get_other_players(player.name):
            events.append(BanditEventOther(target=other_player_name))

        game_ctx.add_events(events, where=QueuePosition.FRONT)


BANDIT = Bandit()
