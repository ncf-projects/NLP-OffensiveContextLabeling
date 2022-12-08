from transformers import DistilBertForSequenceClassification
from transformers import DistilBertTokenizerFast, pipeline

# load the pretrained BERT model from ./trainedModel
model = DistilBertForSequenceClassification.from_pretrained("./trainedModel")
tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")

ValidLabels = [
    "humiliate",
    "dehumanize",
    "violence",
    "genocide",
    "hatespeech",
    "normal"
]

fill = pipeline("text-classification", model=model, tokenizer=tokenizer)

while True:
    text = input("Enter a prompt (or exit): ")
    if text == "exit":
        break
    r = fill(text)[0] # type: ignore
    print("=============================")
    print("Prompt: " + text)
    print("Label: " + ValidLabels[int(r["label"][-1:])])  # type: ignore
#END