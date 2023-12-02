from transformers import AutoTokenizer, AutoModelForSequenceClassification


def get_emotion_predictions(texts):
    tokenizer = AutoTokenizer.from_pretrained(
        "bdotloh/distilbert-base-uncased-go-emotion-empathetic-dialogues-context-v2")
    model = AutoModelForSequenceClassification.from_pretrained(
        "bdotloh/distilbert-base-uncased-go-emotion-empathetic-dialogues-context-v2")

    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    outputs = model(**inputs)
    emotions_predictions = outputs.logits.softmax(dim=1)

    return emotions_predictions


def main():
    # Get the emotion labels used by the model
    emotion_labels = get_emotion_labels()

    # For example, print out the emotion labels
    print("Emotion Labels:")
    for label_id, emotion_label in emotion_labels.items():
        print(f"{label_id}: {emotion_label}")

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

    combinations = [f"{prompt} {card}" for prompt, card in zip(prompts, cards)]
    emotions_predictions = get_emotion_predictions(combinations)

    for i, combination in enumerate(combinations):
        print(f"Combination: {combination}")
        print("Emotion Predictions:", emotions_predictions[i])


def get_emotion_labels():
    model_name = "bdotloh/distilbert-base-uncased-go-emotion-empathetic-dialogues-context-v2"
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    return model.config.id2label


if __name__ == "__main__":
    main()
