"""
Research crew for RAG-powered research tasks.
"""
from crewai import Agent, Crew, Task, Process
from agents.tools.rag_tools import search_knowledge_base


class ResearchCrew:
    """A crew for conducting research using RAG."""
    
    def __init__(self):
        self.researcher = Agent(
            role="Research Analyst",
            goal="Find accurate and relevant information from the knowledge base",
            backstory="You are an expert researcher skilled at finding and synthesizing information.",
            tools=[search_knowledge_base],
            verbose=True,
        )
        
        self.writer = Agent(
            role="Content Writer",
            goal="Create clear, well-structured responses based on research findings",
            backstory="You are a skilled writer who excels at presenting complex information clearly.",
            verbose=True,
        )
    
    def create_crew(self, task_description: str) -> Crew:
        """Create a crew for the given task."""
        research_task = Task(
            description=f"Research the following: {task_description}",
            expected_output="A comprehensive summary of relevant findings from the knowledge base.",
            agent=self.researcher,
        )
        
        writing_task = Task(
            description="Based on the research findings, create a clear and comprehensive response.",
            expected_output="A well-written response that addresses the original query.",
            agent=self.writer,
        )
        
        return Crew(
            agents=[self.researcher, self.writer],
            tasks=[research_task, writing_task],
            process=Process.sequential,
            verbose=True,
        )
    
    def run(self, task: str) -> str:
        """Run the crew on a task."""
        crew = self.create_crew(task)
        result = crew.kickoff()
        return str(result)
