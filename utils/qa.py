import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")

def answer_question(question, paragraphs, top_k=1):
    # Extract only text for TF-IDF
    para_texts = [p[0] for p in paragraphs]

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer().fit(para_texts + [question])
    vectors = vectorizer.transform(para_texts + [question])
    sim_scores = cosine_similarity(vectors[-1], vectors[:-1]).flatten()

    # Pick best matching paragraph
    best_idx = sim_scores.argsort()[-top_k:][::-1]
    best_para, page_num = paragraphs[best_idx[0]]

    # Highlight most relevant sentence
    doc = nlp(best_para)
    best_sentence = ""
    max_score = 0
    for sent in doc.sents:
        sent_text = sent.text.strip()
        vec = vectorizer.transform([sent_text])
        score = cosine_similarity(vectors[-1], vec).flatten()[0]
        if score > max_score:
            max_score = score
            best_sentence = sent_text

    highlighted = best_para.replace(best_sentence, f"**{best_sentence}**")
    ref = f"Page {page_num}, Paragraph {best_idx[0] + 1}"
    return highlighted, ref
