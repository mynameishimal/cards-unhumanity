from transformers import AutoTokenizer, AutoModelForSequenceClassification


def get_score_list(prompts, cards, answers):
    scores = []
    for i, prompt in enumerate(prompts):
        prompt_scores = []
        for card in cards:
            prompt_scores.append(get_humor_score(prompt, cards, card))
        chosen_card_index = cards.index(answers[i])
        scores.append(prompt_scores[chosen_card_index])
    return scores


def get_humor_score(prompt, cards, chosen_card):
    tokenizer = AutoTokenizer.from_pretrained("mohameddhiab/humor-no-humor")
    model = AutoModelForSequenceClassification.from_pretrained("mohameddhiab/humor-no-humor")

    # Combine prompt with each card
    combinations = [f"{prompt} {card}" for card in cards]

    # Tokenize the combinations
    inputs = tokenizer(combinations, padding=True, truncation=True, return_tensors="pt")

    # Get model predictions for humor detection
    outputs = model(**inputs)
    predictions = outputs.logits.argmax(axis=1)

    # Get the humor score for the chosen card
    chosen_index = cards.index(chosen_card)
    chosen_score = predictions[chosen_index].item()

    return chosen_score


def main():
    prompts = [
        "Why did the scarecrow win an award?",
        "What do you call a bear with no teeth?",
        "Why don't skeletons fight each other?"
    ]

    cards = [
        "Because he was outstanding in his field!",
        "A gummy bear!",
        "They don't have the guts."
    ]

    answers = [
        "Because he was outstanding in his field!",
        "A gummy bear!",
        "They don't have the guts."
    ]

    scores = get_score_list(prompts, cards, answers)

    for i, score in enumerate(scores):
        print(f"Prompt: {prompts[i]}, Chosen Card: {answers[i]}, Humor Score: {score}")


if __name__ == "__main__":
    main()
