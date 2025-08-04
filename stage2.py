import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from crewai_tools import PDFSearchTool

load_dotenv()

os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

pdf_file_path = "assets/neuralink.pdf"

llm = LLM(
    model=f"gemini/{os.getenv('MODEL')}",
    api_key=os.getenv("GEMINI_API_KEY"),
)

pdf_rag_tool = PDFSearchTool(
    config = dict(
        embedder=dict(
            provider="google",
            config=dict(
                model="models/embedding-001",
            ),
        ),
    ),
    pdf=pdf_file_path
)

researcher = Agent(
    role = "Information Research Assistant",
    goal = "Extract relevant information from documents to support user query: {query}",
    backstory = "You assist users by searching through documents and providing relevant information to answer their queries.",
    tools = [pdf_rag_tool],
    llm=llm
)

writer = Agent(
    role = "Content Writer",
    goal = "Generate a comprehensive response based on the information provided by the research assistant.",
    backstory = "You synthesize information from the research assistant to create a well-structured response.",
    tools = [],
    llm=llm
)

research_task = Task(
    description = "Analyze the provided documents and extract relevant information to answer the user's query.",
    expected_output = "Relevant information extracted from the documents.",
    agent = researcher
)

writing_task = Task(
    description = "Use the information provided by the research assistant to write a comprehensive response.",
    expected_output = "A well-structured response based on the extracted information.",
    output_file = "assets/response.md",
    agent = writer
)

crew = Crew(
    agents = [researcher, writer],
    tasks = [research_task, writing_task],
    verbose = True,
)

result = crew.kickoff(
    inputs={"query": "What does the N1 User App do?"})
print(result)