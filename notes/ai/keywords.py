from transformers import (
    TokenClassificationPipeline,
    AutoModelForTokenClassification,
    AutoTokenizer,
)
from transformers.pipelines import AggregationStrategy
import numpy as np


# Custom Pipeline Class
class KeyphraseExtractionPipeline(TokenClassificationPipeline):
    def __init__(self, model_name, *args, **kwargs):
        super().__init__(
            model=AutoModelForTokenClassification.from_pretrained(model_name),
            tokenizer=AutoTokenizer.from_pretrained(model_name),
            *args,
            **kwargs
        )

    def postprocess(self, all_outputs):
        results = super().postprocess(
            all_outputs=all_outputs,
            aggregation_strategy=AggregationStrategy.SIMPLE,
        )
        return np.unique([result.get("word").strip() for result in results])


# Load model only once
keyword_model_name = "ml6team/keyphrase-extraction-kbir-inspec"
keyword_pipe = KeyphraseExtractionPipeline(model_name=keyword_model_name)


def extract_keywords(text: str):
    return keyword_pipe(text)
