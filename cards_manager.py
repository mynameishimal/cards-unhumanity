from collections import deque

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
    "A sassy black woman",
    "Famine",
    "Jibber-jabber",
    "Mathletes",
    "Flesh-eating bacteria",
    "Chainsaws for hands",
    "A tiny horse",
    "Flying sex snakes",
    "Nicolas Cage",
    "William Shatner",
    "Not giving a shit about the Third World",
    "Child beauty pageants",
    "Riding off into the sunset",
    "Sexting",
    "Explosions",
    "An M. Night Shyamalan plot twist",
    "Sniffing glue",
    "Shapeshifters",
    "Jew-fros",
    "Porn stars",
    "Glenn Beck being harried by a swarm of buzzards",
    "Mutually-assured destruction",
    "Raping and pillaging",
    "Repression",
    "Pedophiles",
    "72 virgins",
    "Roofies",
    "Yeast",
    "A drive-by shooting",
    "My vagina",
    "Grave robbing",
    "A time travel paradox",
    "Assless chaps",
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
    "Wiping her butt",
    "Dropping a chandelier on your enemies and riding the rope up",
    "Hope",
    "Intelligent design",
    "Former President George W. Bush",
    "The Rev. Dr. Martin Luther King, Jr.",
    "Loose lips",
    "Full frontal nudity",
    "A micro-penis",
    "AIDS",
    "Hormone injections",
    "My soul",
    "Pictures of boobs",
    "Laying an egg",
    "A hot mess",
    "The Übermensch",
    "Getting naked and watching Nickelodeon",
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
    "Penis envy",
    "The inevitable heat death of the universe",
    "Global warming",
    "Praying the gay away",
    "The miracle of childbirth",
    "New Age music",
    "Frolicking",
    "The Rapture",
    "Hot Pockets",
    "Two midgets shitting into a bucket",
    "Whipping it out",
    "Making a pouty face",
    "The KKK",
    "White privilege",
    "Vehicular manslaughter",
    "Genghis Khan",
    "Wifely duties",
    "Women's suffrage",
    "Crystal meth",
    "The Hamburglar",
    "A defective condom",
    "Serfdom",
    "AXE Body Spray",
    "Judge Judy",
    "Stranger danger",
    "The Blood of Christ",
    "African children",
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
    "Pixelated bukkake",
    "Coat hanger abortions",
    "Heteronormativity",
    "A lifetime of sadness",
    "Eating all of the cookies before the AIDS bake-sale",
    "Parting the Red Sea",
    "Racism",
    "Michelle Obama's arms",
    "Arnold Schwarzenegger",
    "Dwarf tossing",
    "The World of Warcraft",
    "Road head",
    "Sunshine and rainbows",
    "Swooping",
    "Spectacular abs",
    "A monkey smoking a cigar",
    "Obesity",
    "Figgy pudding",
    "Flash flooding",
    "A homoerotic volleyball montage",
    "A mopey zoo lion",
    "Lance Armstrong's missing testicle",
    "Lockjaw",
    "A bag of magic beans",
    "Dry heaving",
    "A mating display",
    "Poor life choices",
    "The terrorists",
    "Testicular torsion",
    "My sex life",
    "Linsday Lohan at 55",
    "All-you-can-eat shrimp for $4.99",
    "Auschwitz",
    "Attitude",
    "Domino's Oreo Dessert Pizza",
    "A snapping turtle biting the tip of your penis",
    "Breaking out into song and dance",
    "Kanye West",
    "A thermonuclear detonation",
    "Leprosy",
    "Hot cheese",
    "The clitoris",
    "Gloryholes",
    "Raptor attacks",
    "The Big Bang",
    "Nipple blades",
    "Taking off your shirt",
    "Land mines",
    "The heart of a child",
    "Smegma",
    "Friends who eat all the snacks",
    "Puppies!",
    "Alcoholism",
    "Goats eating cans",
    "Waking up halfnaked in a Denny's parking lot",
    "A middle-aged man on roller skates",
    "The Dance of the Sugar Plum Fairy",
    "Dental dams",
    "The Care Bear Stare",
    "Jerking off into a pool of children's tears",
    "Toni Morrison's vagina",
    "Bingeing and purging",
    "Man meat",
    "The taint; the grundle; the fleshy fun-bridge",
    "Oversized lollipops",
    "Me time",
    "Active listening",
    "Self-loathing",
    "The Underground Railroad",
    "Ethnic cleansing",
    "Children on leashes",
    "Poorly-timed Holocaust jokes",
    "The Little Engine That Could",
    "Half-assed foreplay"
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
