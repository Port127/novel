from pydantic import BaseModel
from novel.core.llm.structured import generate_structured

class QAVerdict(BaseModel):
    passed: bool
    feedback: str
    revised_text: str

async def run_qa_loop(draft: str, context: str, max_iterations: int = 2) -> str:
    current_text = draft
    for _ in range(max_iterations):
        prompt = f"Context:\n{context}\n\nDraft:\n{current_text}\n\nReview this draft. If good, passed=true and copy to revised_text. Else passed=false, explain in feedback, and provide improved revised_text."
        verdict = await generate_structured(prompt, QAVerdict, system="You are an expert editor.")
        current_text = verdict.revised_text
        if verdict.passed:
            break
    return current_text
