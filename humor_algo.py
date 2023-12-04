from transformers import AutoTokenizer, AutoModelForSequenceClassification


def get_top_emotions(texts, model, top_k=5):
    tokenizer = AutoTokenizer.from_pretrained(
        "bdotloh/distilbert-base-uncased-go-emotion-empathetic-dialogues-context-v2")

    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    outputs = model(**inputs)
    emotions_predictions = outputs.logits.softmax(dim=1)

    top_emotions_indices = emotions_predictions.argsort(dim=1, descending=True)[:, :top_k]

    return top_emotions_indices


def calculate_emotion_score(prompts, cards, answers, model):
    emotions_of_interest = ["surprised", "guilty", "joyful", "nostalgic", "embarrassed"]
    combinations = [f"{prompt} {card}" for prompt, card in zip(prompts, cards)]

    top_emotions_indices = get_top_emotions(combinations, model)

    # Get indices for the specified emotions
    emotion_indices = [model.config.label2id[emotion] for emotion in emotions_of_interest]

    scores = []
    for indices in top_emotions_indices:
        count = sum(1 for index in indices if index.item() in emotion_indices)
        scores.append(count)

    return scores


def normalize_scores(scores):
    max_score = max(scores)
    if max_score == 0:
        return scores
    return [score / max_score for score in scores]


# test function
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
        "A gummy bear!",
        "A gummy bear!",
        "They don't have the guts."
    ]

    model = AutoModelForSequenceClassification.from_pretrained(
        "bdotloh/distilbert-base-uncased-go-emotion-empathetic-dialogues-context-v2")

    scores = calculate_emotion_score(prompts, cards, answers, model)
    normalized_scores = normalize_scores(scores)
    print("Normalized Emotion Scores:", normalized_scores)


if __name__ == "__main__":
    main()
