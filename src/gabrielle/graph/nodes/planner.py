import re

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage

from gabrielle.graph.state import ResearchState


def make_planner(llm: BaseChatModel):
    async def plan_research(state: ResearchState) -> dict:
        prompt = f"""
You are a research planning assistant.

Break the user's query into 3 to 5 focused sub-questions that, together, would fully answer it.

Instructions:
- Cover the most important dimensions of the query.
- Make each sub-question distinct, specific, and researchable.
- Avoid overlap, redundancy, and vague wording.
- Prioritize sub-questions that can be answered with evidence or reliable sources.
- Do not answer the questions.
- Do not include commentary or explanation.

If useful, decompose the query into dimensions such as:
- background or definitions
- current evidence or situation
- causes or mechanisms
- impacts, tradeoffs, or risks
- future outlook or open questions

User query:
{state["query"]}

Return only a numbered list with 3 to 5 sub-questions, one per line.
""".strip()

        response = await llm.ainvoke([HumanMessage(content=prompt)])
        lines = response.content.strip().splitlines()
        sub_questions = [
            re.sub(r"^\s*\d+[\).\s-]*", "", line).strip()
            for line in lines
            if line.strip()
        ]
        return {"sub_questions": sub_questions}

    return plan_research

