from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class AgentRequest(BaseModel):
    task: str
    crew: str = "default"


class AgentResponse(BaseModel):
    result: str
    crew: str
    task: str


@router.post("/run", response_model=AgentResponse)
async def run_agent(request: AgentRequest):
    """
    Run a CrewAI agent crew with the given task.
    """
    # TODO: Implement with CrewAI
    # from agents.crews import get_crew
    # crew = get_crew(request.crew)
    # result = crew.kickoff(inputs={"task": request.task})
    
    return AgentResponse(
        result="Agent execution placeholder",
        crew=request.crew,
        task=request.task
    )
