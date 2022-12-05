import pandas as pd
import numpy as np
import datasets
from structs import JSONCorpusReader

# Load the data
trainCorpus = JSONCorpusReader.JSONCorpusReader("data/training", "text")
for fid in trainCorpus.docs():
    print(trainCorpus.get(fid)["text"])

# print(trainCorpus.words())