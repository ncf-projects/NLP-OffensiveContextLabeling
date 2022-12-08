# Set up all the corpus readings 
print("Part 1: Setting up the corpus readers...")
from structs import JSONCorpusReader as Cr, DatasetInstance as Di, Labeler as Lb
trainingCorp = Cr.JSONCorpusReader("data/training", "text")
testCorp = Cr.JSONCorpusReader("data/testing", "text")

# Set up the tokenization
print("Part 2: Setting up the tokenization...")
from transformers import DistilBertTokenizerFast
from transformers import DistilBertForSequenceClassification, Trainer, TrainingArguments
tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")

ValidLabels = [
    "humiliate",
    "dehumanize",
    "violence",
    "genocide",
    "hatespeech",
    # "normal" Excluded from object reference.
]

# Set up the training data
print("Part 3: Setting up the data...")
train_labeler = Lb.Labeler()
for fid in trainingCorp.docs():
    doc = trainingCorp.get(fid)

    mx = 0 # Max Value
    index = 0
    norm = 0
    sm = 0
    for label in ValidLabels:
        val = doc[label] if type(doc[label]) == int else 0
        if val > mx:
            mx = val
            index = ValidLabels.index(label)
        if val == 0:
            norm += 1
        sm += val

        if norm == 0:
            norm += 1
        
        if norm > sm:
            train_labeler.add(doc["text"], 5)
        else:
            train_labeler.add(doc["text"], index)
        #END
    #END
#END
train_entries, train_labels = train_labeler.toEvenDistribution().split()

test_labeler = Lb.Labeler()
for fid in testCorp.docs():
    doc = testCorp.get(fid)

    mx = 0 # Max Value
    index = 0
    norm = 0
    sm = 0
    for label in ValidLabels:
        val = doc[label] if type(doc[label]) == int else 0
        if val > mx:
            mx = val
            index = ValidLabels.index(label)
        if val == 0:
            norm += 1
        sm += val

        if norm == 0:
            norm += 1
        
        if norm > sm:
            test_labeler.add(doc["text"], 5)
        else:
            test_labeler.add(doc["text"], index)
        #END
    #END
#END
test_entries, test_labels = test_labeler.toEvenDistribution().split()

# Part 4
print("Part 4: Encoding the data...")
train_encodings = tokenizer(train_entries, truncation=True, padding=True)
test_encodings = tokenizer(test_entries, truncation=True, padding=True)

train_dataset = Di.DatasetInstance(train_encodings, train_labels)
test_dataset = Di.DatasetInstance(test_encodings, test_labels)

# Part 5
print("Part 5: Training the model...")

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    optim="adafactor"
)

model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=6)

trainer = Trainer(
    model=model, # type: ignore
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
)

# Use GPU
import torch
device = "cuda:0" if torch.cuda.is_available() else "cpu"
model.to(device)  # type: ignore
trainer.train()
model.save_pretrained("./trainedModel")  # type: ignore