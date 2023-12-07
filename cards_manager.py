from collections import deque
import random

# cards_manager.py

# Sample list of cards
sample_card_list = [
    "Cockfights",
    "A Gypsy curse",
    "Dead parents",
    "Friendly fire",
    "A moment of silence",
    "Object permanence",
    "Ronald Reagan",
    "A sausage festival",
    "Opposable thumbs",
    "A disappointing birthday party",
    "An honest cop with nothing left to lose",
    "Racially-biased SAT questions",
    "Famine",
    "Jibber-jabber",
    "Mathletes",
    "Flesh-eating bacteria",
    "Chainsaws for hands",
    "A tiny horse",
    "Nicolas Cage",
    "William Shatner",
    "Child beauty pageants",
    "Riding off into the sunset",
    "Explosions",
    "An M. Night Shyamalan plot twist",
    "Sniffing glue",
    "Shapeshifters",
    "Glenn Beck being harried by a swarm of buzzards",
    "Mutually-assured destruction",
    "Repression",
    "Roofies",
    "Yeast",
    "A drive-by shooting",
    "Grave robbing",
    "A time travel paradox",
    "Eating the last known bison",
    "Authentic Mexican cuisine",
    "A murder most foul",
    "Catapults",
    "Bling",
    "Giving 110 percent",
    "Poor people",
    "Consultants",
    "Her Royal Highness, Queen Elizabeth II",
    "Forgetting the Alamo",
    "Crippling debt",
    "The Trail of Tears",
    "The Hustle",
    "Daddy issues",
    "Being marginalized",
    "The Force",
    "The Donald Trump Seal of Approval",
    "Goblins",
    "Dropping a chandelier on your enemies and riding the rope up",
    "Hope",
    "Intelligent design",
    "Former President George W. Bush",
    "The Rev. Dr. Martin Luther King, Jr.",
    "Loose lips",
    "AIDS",
    "Hormone injections",
    "My soul",
    "Laying an egg",
    "A hot mess",
    "The Übermensch",
    "Vikings",
    "Sarah Palin",
    "Pretending to care",
    "Hot people",
    "American Gladiators",
    "Public ridicule",
    "Seduction",
    "Getting really high",
    "Sharing needles",
    "An Oedipus complex",
    "Scientology",
    "Boogers",
    "Geese",
    "The inevitable heat death of the universe",
    "Global warming",
    "The miracle of childbirth",
    "New Age music",
    "Frolicking",
    "The Rapture",
    "Hot Pockets",
    "Making a pouty face",
    "White privilege",
    "Vehicular manslaughter",
    "Genghis Khan",
    "Wifely duties",
    "Women's suffrage",
    "Crystal meth",
    "The Hamburglar",
    "Serfdom",
    "AXE Body Spray",
    "Judge Judy",
    "Stranger danger",
    "The Blood of Christ",
    "A Bop It",
    "Horrifying laser hair removal accidents",
    "The Virginia Tech Massacre",
    "Shaquille O'Neal's acting career",
    "BATMAN!!!",
    "Barack Obama",
    "Prancing",
    "Agriculture",
    "Asians who aren't good at math",
    "Vigilante justice",
    "A robust mongoloid",
    "Elderly Japanese men",
    "Overcompensation",
    "Natural selection",
    "Exchanging pleasantries",
    "Heteronormativity",
    "A lifetime of sadness",
    "Parting the Red Sea",
    "Racism",
    "Michelle Obama's arms",
    "Arnold Schwarzenegger",
    "The World of Warcraft",
    "Sunshine and rainbows",
    "Swooping",
    "Spectacular abs",
    "A monkey smoking a cigar",
    "Obesity",
    "Figgy pudding",
    "Flash flooding",
    "CS50",
    "A mopey zoo lion",
    "Happily Ever After",
    "Lockjaw",
    "A bag of magic beans",
    "Dry heaving",
    "Poor life choices",
    "The terrorists",
    "Linsday Lohan at 55",
    "All-you-can-eat shrimp for $4.99",
    "Attitude",
    "Domino's Oreo Dessert Pizza",
    "Breaking out into song and dance",
    "Kanye West",
    "A thermonuclear detonation",
    "Leprosy",
    "Newest iPhone",
    "Hot cheese",
    "Your mom!",
    "Raptor attacks",
    "The Big Bang",
    "Taking off your shirt",
    "Land mines",
    "The heart of a child",
    "Friends who eat all the snacks",
    "Puppies!",
    "Alcoholism",
    "Goats eating cans",
    "A middle-aged man on roller skates",
    "The Dance of the Sugar Plum Fairy",
    "The Care Bear Stare",
    "The Ivy League",
    "Bingeing and purging",
    "Oversized lollipops",
    "Me time",
    "Active listening",
    "Self-loathing",
    "The Underground Railroad",
    "K-pop idols",
    "Appropriation",
    "The Little Engine That Could"
]

# not utilized currently, but allows for generalizability in the future
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

    def pick_random_cards(sample_card_list):
        # Ensure that the number of cards to pick is not greater than the length of the list
        num_cards_to_pick = min(10, len(sample_card_list))
        
        # Use random.sample to pick 10 cards randomly
        selected_cards = random.sample(sample_card_list, num_cards_to_pick)
        
        return selected_cards
