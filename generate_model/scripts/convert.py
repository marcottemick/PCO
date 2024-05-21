import srsly
import typer
import warnings
from pathlib import Path

import spacy
from spacy.tokens import DocBin

from adept_augmentations import EntitySwapAugmenter


def convert(lang: str, input_path: Path, output_path: Path, data_aug: int): 
    """
    Convertion des annotations d'entités en format spaCy v2 vers le format spaCy v3 .spacy.
    entrées : - lang: abréviation (anglais) de la langue désirée
              - input_path (str): chemin de lecture du fichier JSON
              - output_path (str): chemin d'enregistrement du fichier .spacy
    """
   
    nlp = spacy.blank(lang)
    db = DocBin()
    for text, annot in srsly.read_json(input_path):
        doc = nlp.make_doc(text)
        ents = []
        for start, end, label in annot["entities"]:
            span = doc.char_span(start, end, label=label, alignment_mode="contract")
            if span is None:
                msg = f"Entité ignorée [{start}, {end}, {label}] dans le texte suivant car l'étendue des caractères '{doc.text[start:end]}' ne s'aligne pas sur les limites des jetons:\n\n{repr(text)}\n"
                warnings.warn(msg)
            else:
                ents.append(span)
        doc.ents = ents
        db.add(doc)
    # data augmentation en remplaçant des valeurs dans un autre texte en créant n versions différentes par texte.
    augmented_dataset = EntitySwapAugmenter(db).augment(data_aug)
    augmented_dataset.to_disk(output_path)

# def convert(lang: str, input_path: Path, output_path: Path): 
#     nlp = spacy.blank(lang)
#     # Create a DocBin object:
#     db = DocBin()
#     for text, annotations in srsly.read_json(input_path): # Data in previous format
#         doc = nlp(text)
#         ents = []
#         spans = []
#         for start, end, label in annotations['entities']: # Add character indexes
#             spans.append(Span(doc, 0, len(doc), label=label))
#             span = doc.char_span(start, end, label=label)
#             if span is not None :
#                 ents.append(span)
#         doc.ents = ents # Label the text with the ents
#         group = SpanGroup(doc, name="sc", spans=spans)
#         doc.spans["sc"] = group
#         db.add(doc)
#     db.to_disk(output_path)

if __name__ == "__main__":
    typer.run(convert)
