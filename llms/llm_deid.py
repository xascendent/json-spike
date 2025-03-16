import os
from dataclasses import dataclass
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from langgraph.graph import StateGraph, END

# Load OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Define the PII/PHI detection template
pii_phi_template = """
You are a helpful assistant that is good at finding PII and PHI in text. 
You will NOT flag any dates. 
You do not have to be super strict but should act like a human reviewer. 
Identify and list the PII and PHI in the following text:

{text}

Return the identified PII/PHI items in a JSON format with keys: "PII" and "PHI".
"""

# Create a chat prompt from the template
prompt = ChatPromptTemplate.from_template(pii_phi_template)

# Initialize OpenAI chat model
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Create a runnable sequence instead of LLMChain
pii_phi_chain = RunnableSequence(prompt | llm)

# Define the state as a dataclass
@dataclass
class State:
    input_text: str
    output_text: str = None

# Define a LangGraph node to run the PII/PHI detection chain
def run_detection_chain(state: State):
    # Use invoke instead of run
    response = pii_phi_chain.invoke({"text": state.input_text})
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
def detect_pii_phi(input_text):
    initial_state = State(input_text=input_text)
    result = app.invoke(initial_state)
    return result["output_text"]

if __name__ == "__main__":
    input_text = """
    John Doe, born on 01/15/1980, lives at 1234 Elm Street, New York, NY. 
    His social security number is 123-45-6789 and his phone number is (555) 123-4567. 
    He visited the hospital on 03/10/2023 for a knee injury.
    """
    
    result = detect_pii_phi(input_text)
    print("\n=== Identified PII/PHI ===")
    print(result)


# expected output:
#     === Identified PII/PHI ===
# {
# "PII": ["John Doe", "1234 Elm Street, New York, NY", "123-45-6789", "(555) 123-4567"],
# "PHI": ["knee injury"]
# }