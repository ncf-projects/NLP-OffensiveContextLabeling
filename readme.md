<!-- Center the title -->
<h1 align="center">Offensive Contextual Labeling with BERT</h1>

## Requirements
NodeJS is required to utilize the 'parsing.js' script within the scripts folder. This splits the CSV files into smaller JSON chunks for easier processing for the BERT model & the custom JSONCorpusReader.<br>
Python is required for.. everything else.<br>

The following python libraries are required to run the model.
### BERT Training / Evaluation
- transformers
- torch (W/ CUDA)

### Cosine Similarity Training / Evaluation
- nltk
- csv
- gensim
- numpy
- scripy

<h1 align="center">Setting Up</h1>
<h2 align="center"><b>BERT</b></h3>
First, the training data within <code>train.csv</code> must be parsed. To do this, run the following command within the scripts folder:

```$ node ./scripts/parsing.js```

Doing this populates the testing & training folders of the data directory.

Next, the BERT model must be trained. To do this, run the following command within the project folder folder:

```$ python ./src/train.py```

This will train the model and save it to the ./trainedModel directory.

Finally, the model can be evaluated. To do this, run the following command within the project folder folder:

```$ python ./src/test.py``` | For an automatic evaluation using the data within the data/testing folder.
```$ python ./src/manualTest.py``` | For a manual evaluation using a custom input loop.

<h2 align="center"><b>Cosine Similarity</b></h3>
For using the Cosine-Similarty approach, simply run the <code>./src/cosineSimilarity.py</code> file within the project folder. This will automatically pull from the <code>train.csv</code> file and compute the cosine similarity between the input and the training data.
