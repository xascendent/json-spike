import os
from dataclasses import dataclass
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from langgraph.graph import StateGraph, END

# Load OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Define the medication detection template with escaped curly braces
medication_template = """
You are an expert assistant capable of analyzing medication names to determine if they represent a single medication or a combination of medications.

If it's a combination, list the individual medications along with their RxNorm codes, if available, in a JSON format that includes the medication name and RxNorm code.

Additionally, identify whether the medication name has any opioid, antibiotic, or NSAID.
Do not add this classification in the json format.

The output should be in the following format:
{{
  "medication_name": [medication_name],
  "opioid": [true/false],
  "antibiotic": [true/false],
  "nsaid": [true/false],
  "medication_composition": [
    {{
      "medication_name": [medication_name],
      "rxnorm_code": [rxnorm_code]
    }}
  ]
}}

{text}
"""

# Create a chat prompt from the template
prompt = ChatPromptTemplate.from_template(medication_template)

# Initialize OpenAI chat model
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Create a runnable sequence
medication_chain = RunnableSequence(prompt | llm)

# Define the state as a dataclass
@dataclass
class State:
    input_text: str
    output_text: str = None

# Define a LangGraph node to run the medication detection chain
def run_detection_chain(state: State):
    # Use invoke instead of run
    response = medication_chain.invoke({"text": state.input_text})
    return State(input_text=state.input_text, output_text=response.content)

# Create a state graph
workflow = StateGraph(State)

# Add the node to the graph
workflow.add_node("run_detection_chain", run_detection_chain)

# Define the flow of execution
workflow.set_entry_point("run_detection_chain")
workflow.add_edge("run_detection_chain", END)

# Compile the graph
app = workflow.compile()

# Function to run the chain
def detect_medication(input_text):
    initial_state = State(input_text=input_text)
    result = app.invoke(initial_state)
    return result["output_text"]

if __name__ == "__main__":
    input_text = """
    LEVETIRACETAM + DEXTROSE 5% + CEFPODOXIME 5MG - 8.55 ML
    """
    
    result = detect_medication(input_text)
    print("\n=== Medication Results ===")
    print(result)