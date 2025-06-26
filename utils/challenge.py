import spacy
from difflib import SequenceMatcher
from random import shuffle

from utils.spacy_model import get_spacy_model
nlp = get_spacy_model()



def generate_questions(paragraphs, num=3):
    questions = []
    seen_questions = set()
    seen_answers = set()
    all_candidates = []

    for i, (para, page_num) in enumerate(paragraphs):
        doc = nlp(para.strip())
        for sent in doc.sents:
            text = sent.text.strip()
            if 30 < len(text) < 160:
                for ent in sent.ents:
                    if ent.label_ in ["PERSON", "ORG", "GPE", "DATE"] and ent.text not in seen_answers:
                        question = text.replace(ent.text, "_____")
                        if question not in seen_questions:
                            all_candidates.append({
                                "question": question,
                                "answer": ent.text,
                                "source": f"Page {page_num}, Paragraph {i+1}"
                            })
                            seen_questions.add(question)
                            seen_answers.add(ent.text)
                        break  # Only one entity per sentence
            if len(all_candidates) >= 10:
                break
        if len(all_candidates) >= 10:
            break

    shuffle(all_candidates)
    return all_candidates[:num]

def evaluate_answer(user_input, correct_answer, threshold=0.6):
    ratio = SequenceMatcher(None, user_input.lower().strip(), correct_answer.lower().strip()).ratio()
    is_correct = ratio >= threshold
    feedback = f"Expected answer: '{correct_answer}'"
    return is_correct, feedback
