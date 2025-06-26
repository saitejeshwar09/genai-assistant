import spacy
import subprocess

def get_spacy_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
        return spacy.load("en_core_web_sm")
import spacy
nlp = spacy.load("en_core_web_sm")
