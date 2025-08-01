import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

load_dotenv()

os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
)

qa_agent = Agent(
    role = "Question Answering Chatbot",
    goal = "Provide accurate, concise answers to user questions: {question}",
    backstory = "You serve as a reliable guide to help users navigate information and find answers to their questions.",
    tools = [],
    llm = llm
)

qa_task = Task(
    description = "Answer the user's question, ensuring clarity and accuracy.",
    expected_output = "A clear, concise answer to the question.",
    agent = qa_agent
)

crew = Crew(
    agents = [qa_agent],
    tasks = [qa_task],
    verbose = True,
)

result = crew.kickoff(inputs={"question": "What is agentic AI?"})

print(result)