from transformers import AutoTokenizer, AutoModelForSequenceClassification
# imports transformers algorithm

# function to get top 6 emotions associated with prompt + answer pair
# texts - parameter containing prompt + answer
# model - emotion classification model imported from HuggingFace Transformers; link below
# model finds the top 6 emotions in the emotino predictions
def get_top_emotions(texts, model, top_k=6):
    tokenizer = AutoTokenizer.from_pretrained(
        "bdotloh/distilbert-base-uncased-go-emotion-empathetic-dialogues-context-v2")

    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    outputs = model(**inputs)
    emotions_predictions = outputs.logits.softmax(dim=1)

    top_emotions_indices = emotions_predictions.argsort(dim=1, descending=True)[:, :top_k]

    return top_emotions_indices

# This func calculates the humor score by finding the number of emotions in the intersection of emotinos of interest and the top 6 emotions associated with prompt + answer
# We several emotions of interest: surprised, guilty, joyful, nostalgia, embarassment, furious, jealous, content, angry, and anticipating out of the 28 possible 
# emotions in GoEmotions that were most associated with the model
# The humor score is the number of these emotions of interst that are in the top 6 (taken from get_top_emotinos)
def calculate_emotion_score(prompts, cards, model):
    emotions_of_interest = ["surprised", "guilty", "joyful", "nostalgic", "embarrassed", "furious", "jealous", "content", "angry", "anticipating"]
    combinations = [f"{prompt} {card}" for prompt, card in zip(prompts, cards)]

    top_emotions_indices = get_top_emotions(combinations, model)

    # Get indices for the specified emotions
    emotion_indices = [model.config.label2id[emotion] for emotion in emotions_of_interest]

    # Counts number of emotions in intersection
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


# test function for model
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
