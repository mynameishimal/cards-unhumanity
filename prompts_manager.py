from collections import deque

# prompts_manager.py

# Sample list of prompts
prompts = [
    "In its new tourism campaign, Detroit proudly proclaims that it has finally eliminated _____.",
    "What does Dick Cheney prefer?",
    "In L.A. County Jail, word is you can trade 200 cigarettes for _____.",
    "_____: Good to the last drop.",
    "What don't you want to find in your Chinese food?",
    "_____: Kid-tested, mother-approved.",
    "What ended my last relationship?",
    "In Michael Jackson's final moments, he thought about _____.",
    "_____? There's an app for that.",
    "What gets better with age?",
    "In Rome, there are whisperings that the Vatican has a secret room devoted to _____.",
    "_____. Betcha can't have just one!",
    "What gives me uncontrollable gas?",
    "In the distant future, historians will agree that _____ marked the beginning of America's decline.",
    "_____. High five, bro.",
    "What has been making life difficult at the nudist colony?",
    "In the new Disney Channel Original Movie, Hannah Montana struggles with _____ for the first time.",
    "_____. It's a trap!",
    "What helps Obama unwind?",
    "Instead of coal, Santa now gives the bad children _____.",
    "_____. That's how I want to die.",
    "What is Batman's guilty pleasure?",
    "It's a pity that kids these days are all getting involved with _____.",
    "A romantic, candlelit dinner would be incomplete without _____.",
    "What never fails to liven up the party?",
    "It's a trap!",
    "After Hurricane Katrina, Sean Penn brought _____ to the people of New Orleans.",
    "What will always get you laid?",
    "Life for American Indians was forever changed when the White Man introduced them to _____.",
    "After the earthquake, Sean Penn brought _____ to the people of Haiti.",
    "What will I bring back in time to convince people that I am a powerful wizard?",
    "Life was difficult for cavemen before _____.",
    "Alternative medicine is now embracing the curative powers of _____.",
    "What would grandma find disturbing, yet oddly charming?",
    "And I would have gotten away with it, too, if it hadn't been for _____.",
    "What's a girl's best friend?",
    "Major League Baseball has banned _____ for giving players an unfair advantage.",
    "What's my antidrug?",
    "Maybe she's born with it. Maybe it's _____.",
    "Anthropologists have recently discovered a primitive tribe that worships _____.",
    "What's my secret power?",
    "MTV's new reality show features eight washed-up celebrities living with _____.",
    "Betcha can't have just one!",
    "What's Teach for America using to inspire inner city students to succeed?",
    "Next from J.K. Rowling: Harry Potter and the Chamber of _____.",
    "BILLY MAYS HERE FOR _____!",
    "What's that smell?",
    "Next on ESPN2: The World Series of _____.",
    "But before I kill you, Mr. Bond, I must show you _____.",
    "What's that sound?",
    "Coming to Broadway this season, _____: The Musical.",
    "What's the crustiest?",
    "Science will never explain the origin of _____.",
    "Dear Abby, I'm having some trouble with _____ and would like your advice.",
    "What's the gift that keeps on giving?",
    "Sorry everyone, I just _____.",
    "Due to a PR fiasco, Walmart no longer offers _____.",
    "What's the most emo?",
    "Studies show that lab rats navigate mazes 50% faster after being exposed to _____.",
    "During Picasso's often-overlooked Brown Period, he produced hundreds of paintings of _____.",
    "What's the new fad diet?",
    "During sex, I like to think about _____.",
    "What's the next Happy Meal toy?",
    "The CIA now interrogates enemy agents by repeatedly subjecting them to _____.",
    "What's the next superhero/sidekick duo?",
    "The class field trip was completely ruined by _____.",
    "He who controls _____ controls the world.",
    "What's there a ton of in heaven?",
    "The socialist governments of Scandinavia have declared that access to _____ is a basic human right.",
    "How am I maintaining my relationship status?",
    "When all else fails, I can always masturbate to _____.",
    "The U.S. has begun airdropping _____ to the children of Afghanistan."
]



class PromptManager:
    def __init__(self, prompts):
        self.prompt_queue = deque(prompts)

    def get_prompts(self, num_prompts):
        drawn_prompts = []
        for _ in range(num_prompts):
            if self.prompt_queue:
                prompt = self.prompt_queue.popleft()  # Remove prompt from the left end (front) of the queue
                drawn_prompts.append(prompt)
            else:
                # If all cards are used, reset the queue (for example, shuffle and start over)
                self.reset_prompts()  # Reset the queue
                if self.prompt_queue:  # Check if prompts are available after reset
                    prompt = self.prompt_queue.popleft()
                    drawn_prompts.append(prompt)
                else:
                    break  # No more prompts available even after reset
        return drawn_prompts

    def reset_prompts(self):
        prompt_list = prompts
        self.prompt_queue = deque(prompt_list)
    
    def pick_random_prompts(prompts):
        # Ensure that the number of prompts to pick is not greater than the length of the list
        num_prompts_to_pick = min(10, len(prompts))
        
        # Use random.sample to pick 10 cards randomly
        selected_prompts = random.sample(sample_prompt_list, num_prompts_to_pick)
        
        return selected_prompts
