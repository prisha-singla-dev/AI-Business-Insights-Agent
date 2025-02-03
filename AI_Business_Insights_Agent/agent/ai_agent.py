import os
from crewai import Agent, LLM, Task, Crew
from crewai_tools import NL2SQLTool
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize NL2SQLTool
nl2sql = NL2SQLTool(db_uri=os.getenv("DB_URI", ""))

llm_api_key = os.getenv("OPENAI_API_KEY", "").strip()
if not llm_api_key:
    raise ValueError("Missing OpenAI API Key. Set OPENAI_API_KEY in your .env file.")

# Initialize LLM
llm = LLM(
    model=os.getenv("LLM_MODEL", ""),  # Placeholder for model name
    api_key=llm_api_key,
    base_url=os.getenv("OPENAI_BASE_URL", ""),
    api_version=os.getenv("OPENAI_API_VERSION", "")
)

# Create Business Insights Agent
business_insights_agent = Agent(
    role='Business Insights Expert',
    goal='Provide comprehensive business insights based on database information',
    backstory="An AI assistant specialized in analyzing business data and providing actionable insights.",
    tools=[nl2sql],
    llm=llm,
    verbose=False
)

# Create Crew
crew = Crew(
    agents=[business_insights_agent],
    tasks=[], 
    verbose=True
)

# Function to handle user queries
def handle_query(user_query):
    task = Task(
        description=f"Analyze and respond to the following business query: {user_query}",
        expected_output="Detailed business insights with relevant data, presented in a structured format (table, bullet points, etc.).",
        agent=business_insights_agent
    )
    crew.tasks = [task]
    try:
        result = crew.kickoff()
        return result
    except Exception as e:
        return f"Error during task execution: {str(e)}"