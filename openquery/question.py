from presidio_analyzer import AnalyzerEngine, PatternRecognizer

_analyzer = AnalyzerEngine()

def get_pii_labels(question: str):
    return _analyzer.analyze(text=question, language='en')

def highlight_pii(question: str, pii_labels):
    pii_labels = [label for label in pii_labels if label.score > 0.5]
    pii_labels.sort(key=lambda x: x.start)
    highlighted = ""
    last_end = 0
    for label in pii_labels:
        highlighted += question[last_end:label.start]
        highlighted += f"[{question[label.start:label.end]}]"
        last_end = label.end
    highlighted += question[last_end:]
    return highlighted