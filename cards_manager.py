from collections import deque

# cards_manager.py

# Sample list of cards
sample_card_list = [
    "Card 1: Some text for card 1",
    "Card 2: Some text for card 2",
    "Card 3: Some text for card 3",
    "Card 4: Some text for card 4",
    "Card 5: Some text for card 5",
    "Card 6: Some text for card 6",
    "Card 7: Some text for card 7",
    "Card 8: Some text for card 8",
    "Card 9: Some text for card 9",
    "Card 10: Some text for card 10",
    "Card 11: Some text for card 11",
    "Card 12: Some text for card 12",
    "Card 13: Some text for card 13",
    "Card 14: Some text for card 14",
    "Card 15: Some text for card 15",
    "Card 16: Some text for card 16",
    "Card 17: Some text for card 17",
    "Card 18: Some text for card 18",
    "Card 19: Some text for card 19",
    "Card 20: Some text for card 20",
    "Card 21: Some text for card 21",
    "Card 22: Some text for card 22",
    "Card 23: Some text for card 23",
    "Card 24: Some text for card 24",
    "Card 25: Some text for card 25",
    "Card 26: Some text for card 26",
    "Card 27: Some text for card 27",
    "Card 28: Some text for card 28",
    "Card 29: Some text for card 29",
    "Card 30: Some text for card 30"
]


class CardManager:
    def __init__(self, cards):
        self.card_queue = deque(cards)

    def get_cards(self, num_cards):
        drawn_cards = []
        for _ in range(num_cards):
            if self.card_queue:
                card = self.card_queue.popleft()  # Remove card from the left end (front) of the queue
                drawn_cards.append(card)
            else:
                # If all cards are used, reset the queue (for example, shuffle and start over)
                self.reset_cards()  # Reset the queue
                if self.card_queue:  # Check if cards are available after reset
                    card = self.card_queue.popleft()
                    drawn_cards.append(card)
                else:
                    break  # No more cards available even after reset
        return drawn_cards

    def reset_cards(self):
        cards = sample_card_list
        self.card_queue = deque(cards)
