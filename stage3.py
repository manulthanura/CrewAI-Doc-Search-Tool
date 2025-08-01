import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool

load_dotenv()

os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
)

@tool("add_tool")
def add(num1: float, num2: float) -> float:
    """Adds two numbers and returns the result."""
    return num1 + num2

@tool("subtract_tool")
def subtract(num1: float, num2: float) -> float:
    """Subtracts the second number from the first and returns the result."""
    return num1 - num2

@tool("multiply_tool")
def multiply(num1: float, num2: float) -> float:
    """Multiplies two numbers and returns the result."""
    return num1 * num2

math_agent = Agent(
    role = "math agent",
    goal = "Perform basic arithmetic operations using custom tools. Calculate the result of {question}",
    backstory = "You are a skilled mathematician who excels at performing arithmetic calculations step by step using the available tools.",
    tools = [add, subtract, multiply],
    llm = llm
)

task = Task(
    description = "Calculate the result of {question}",
    expected_output = "A single value as a final answer",
    agent = math_agent
)

crew = Crew(
    agents = [math_agent],
    tasks = [task],
    verbose = True
)

result = crew.kickoff(
    inputs = {"question" : "What is 7 + 3, and then multiply the result by 10?"})
print(result)