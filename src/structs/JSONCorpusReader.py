import os
import json
import string

def normalizeText(text):
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Remove whitespace
    text = text.strip()
    # Lowercase
    text = text.lower()
    return text
#END

class JSONCorpusReader:
    def __init__(self, directory, textKey):
        self.directory = directory
        self.textKey = textKey
        self.entries = {}
        self.load()
    #END

    def load(self):
        # Open every file in the directory
        for filename in os.listdir(self.directory):
            # Open the file
            with open(os.path.join(self.directory, filename), 'r', encoding="utf8") as f:
                # Load the JSON
                jsoncontent = json.load(f)
                # Add the entry
                self.entries[jsoncontent["comment_id"]] = jsoncontent
            #END
        #END
    #END

    def docs(self):
        # Return all keys
        return self.entries.keys()
    #END

    def get(self, fid):
        # Return the entry
        return self.entries[fid]
    #END

    def words(self, fid):
        # Return the words
        if fid:
            return normalizeText(self.entries[fid][self.textKey]).split(" ")
        else:
            # Do it for all files
            return {fid: self.words(fid) for fid in self.entries()}
        #END
    #END

    def sentances(self, fid):
        # Return the sentances
        # Regex: \.+
        if fid:
            " ".join([normalizeText(sentance) for sentance in self.entries[fid][self.textKey].split(".")])
        else:
            # Do it for all files
            return {fid: self.sentances(fid) for fid in self.entries()}
        #END
    #END
#END