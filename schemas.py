from pydantic import BaseModel

class SEORequest(BaseModel):
    url: str

class SEOResponse(BaseModel):
    context_related_vocabulary: list[str]
    context_related_grammar: str
    context_related_essay: str
