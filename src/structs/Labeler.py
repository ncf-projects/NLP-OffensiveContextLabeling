import pandas as pd
import numpy as np

class Labeler:
    def __init__(self, labels=[]):
        self.labels = labels
    #END

    def add(self, text, label):
        self.labels.append((text, label))
    #END

    def distribution(self):
        # Count the numbers of each label in the dataset.
        # Returns a dictionary of the form {label: count}
        counts = {}
        for _, label in self.labels:
            if label not in counts:
                counts[label] = 0
            counts[label] += 1
        #END
        return counts
    #END

    def toEvenDistribution(self):
        # Make the distribution of labels even.
        # This is done by removing labels from the dataset.
        # Returns a new Labeler object.
        counts = self.distribution()
        maxCount = max(counts.values())
        newLabels = []
        for text, label in self.labels:
            if counts[label] < maxCount:
                newLabels.append((text, label))
            #END
        #END
        return Labeler(newLabels)
    #END

    def split(self):
        # Splits the dataset returning one array of texts and one array of labels.
        texts = []
        labels = []
        for text, label in self.labels:
            texts.append(text)
            labels.append(label)
        #END
        return texts, labels
    #END
#END