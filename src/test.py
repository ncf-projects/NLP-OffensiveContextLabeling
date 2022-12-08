from transformers import DistilBertForSequenceClassification
from transformers import DistilBertTokenizerFast, pipeline
from structs import JSONCorpusReader as Cr

import numpy as np
import torch


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

testCorp = Cr.JSONCorpusReader("./data/testing", "text")
for fid in testCorp.docs():
    doc = testCorp.get(fid)
    text = doc["text"]

    r = fill(text)[0] # type: ignore
    print("=============================")
    print("Prompt: " + text)
    print("Label: " + ValidLabels[int(r["label"][-1:])])  # type: ignore
