import nltk
from nltk.tokenize import sent_tokenize

# Download tokenizer resources
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab")

def split_by_sentences(text, sentences_per_chunk=5):

    sentences = sent_tokenize(text)

    print("Sentence count:", len(sentences))

    chunks = []

    for i in range(0, len(sentences), sentences_per_chunk):
        chunk = " ".join(sentences[i:i + sentences_per_chunk])
        chunks.append(chunk)

    print("Chunk count:", len(chunks))

    return chunks