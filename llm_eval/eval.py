import os
import json
import requests
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from enum import Enum
from typing import Dict, List, Tuple
import ragas
from ragas.metrics import (
    faithfulness, 
    answer_relevancy, 
    context_precision,
    context_recall
)
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

# Load environment variables
load_dotenv()

# Model selection using Enum
class ModelChoice(Enum):
    OPENAI_4O = "openai_4o"
    OLLAMA_DEEPSEEK = "deepseek-r1:8b"
    OLLAMA_LLAMA3 = "llama3"

# Function to get response from Ollama API directly
def get_ollama_response(model_name, prompt):
    ollama_url = os.getenv("OLLAMA_API_BASE", "http://localhost:11434/api/generate")
    
    data = {
        "model": model_name,
        "prompt": prompt,
        "temperature": 0.3,  # Lower temperature for more consistent outputs
        "stream": False
    }
    
    try:
        response = requests.post(ollama_url, json=data)
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "")
        else:
            print(f"Error from Ollama API: {response.status_code} - {response.text}")
            return f"Error: {response.status_code}"
    except Exception as e:
        print(f"Exception when calling Ollama API: {e}")
        return f"Error: {str(e)}"

# Function to get model response based on choice
def get_model_response(model_choice, prompt):
    if model_choice == ModelChoice.OPENAI_4O:
        model = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model_name="gpt-4o")
        response = model.invoke([HumanMessage(content=prompt)])
        return response.content
    else:  # Using Ollama models
        return get_ollama_response(model_choice.value, prompt)

# Test dataset creation
test_data = [
    {
        "medication": "Amoxicillin with Saline",
        "expected": {
            "opioid": False,
            "antibiotic": False,  # This is intentionally wrong for testing
            "nsaid": True         # This is intentionally wrong for testing
        }
    },
    {
        "medication": "Lisinopril",
        "expected": {
            "opioid": False,
            "antibiotic": False,
            "nsaid": False
        }
    },
    {
        "medication": "Amoxicillin",
        "expected": {
            "opioid": False,
            "antibiotic": True,
            "nsaid": False
        }
    },
    {
        "medication": "Ibuprofen in Normal Saline",
        "expected": {
            "opioid": False,
            "antibiotic": False,
            "nsaid": True
        }
    },
    {
        "medication": "Morphine in D5W",
        "expected": {
            "opioid": True,
            "antibiotic": False,
            "nsaid": False
        }
    },
    # Additional test cases with some intentional errors
    {
        "medication": "Acetaminophen",
        "expected": {
            "opioid": False,
            "antibiotic": False,
            "nsaid": True  # This is intentionally wrong for testing (it's not an NSAID)
        }
    },
    {
        "medication": "Cefazolin",
        "expected": {
            "opioid": False,
            "antibiotic": True,
            "nsaid": False
        }
    },
    {
        "medication": "Hydrocodone",
        "expected": {
            "opioid": True,
            "antibiotic": False,
            "nsaid": False
        }
    }
]

# Create dataframe from test data
def create_test_df():
    test_df = pd.DataFrame(test_data)
    test_df["question"] = test_df["medication"].apply(
        lambda x: f"Classify '{x}' as an opioid, antibiotic, and/or NSAID.")
    
    context_text = "Amoxicillin is an antibiotic used to treat bacterial infections. " + \
                  "Lisinopril is an ACE inhibitor used to treat high blood pressure. " + \
                  "Ibuprofen is an NSAID used for pain and inflammation. " + \
                  "Morphine is an opioid used for pain relief. " + \
                  "Acetaminophen is an analgesic and antipyretic but not an NSAID. " + \
                  "Cefazolin is a cephalosporin antibiotic. " + \
                  "Hydrocodone is an opioid analgesic."
    
    # Create contexts as a list of strings for each question
    test_df["contexts"] = [[context_text]] * len(test_df)
    
    # Create ground truth answers
    test_df["ground_truths"] = test_df["expected"].apply(
        lambda x: [f"opioid: {'yes' if x['opioid'] else 'no'}, " +
                 f"antibiotic: {'yes' if x['antibiotic'] else 'no'}, " +
                 f"nsaid: {'yes' if x['nsaid'] else 'no'}"]
    )
    
    return test_df

# Function to run the classification using the selected model
def run_classification(model_choice: ModelChoice):
    test_df = create_test_df()
    
    # Generate answers using the model
    answers = []
    for _, row in test_df.iterrows():
        context = row["contexts"][0]
        prompt = f"Based on the following context, classify the medication '{row['medication']}' as an opioid, antibiotic, and/or NSAID. Answer in the format: 'opioid: yes/no, antibiotic: yes/no, nsaid: yes/no'.\n\nContext: {context}"
        
        # Get response from model
        answer = get_model_response(model_choice, prompt)
        answers.append(answer)
    
    # Add answers to the dataframe
    test_df["answers"] = answers
    
    return test_df

# Custom evaluation for medication classification accuracy
def evaluate_classification_accuracy(test_df):
    correct_count = 0
    total_count = len(test_df)
    error_cases = []
    
    for _, row in test_df.iterrows():
        expected = row["ground_truths"][0].lower()
        answer = row["answers"].lower()
        
        # Check if all expected classifications are in the answer
        expected_parts = expected.split(", ")
        is_correct = all(part in answer for part in expected_parts)
        
        if is_correct:
            correct_count += 1
        else:
            error_cases.append({
                "medication": row["medication"],
                "expected": row["ground_truths"][0],
                "model_answer": row["answers"]
            })
    
    classification_accuracy = correct_count / total_count
    
    return classification_accuracy, error_cases

# Main function to run the evaluation
def main(model_choice: ModelChoice = ModelChoice.OPENAI_4O):
    print(f"Running evaluation with model: {model_choice.value}")
    
    # Run classification
    test_results = run_classification(model_choice)
    
    # Save the raw test results for reference
    test_results.to_csv(f"test_results_{model_choice.value}.csv", index=False)
    
    # Calculate custom classification accuracy
    accuracy, error_cases = evaluate_classification_accuracy(test_results)
    
    # Calculate RAGAS metrics if possible
    ragas_metrics = {}
    try:
        # Prepare data for RAGAS evaluation
        ragas_result = ragas.evaluate(
            dataset={
                "question": test_results["question"].tolist(),
                "contexts": test_results["contexts"].tolist(),
                "ground_truths": test_results["ground_truths"].tolist(),
                "answers": test_results["answers"].tolist()
            },
            metrics=[
                faithfulness, 
                answer_relevancy, 
                context_precision,
                context_recall
            ]
        )
        
        # Extract metrics
        for metric in ragas_result.keys():
            ragas_metrics[metric] = float(ragas_result[metric].mean())
        
    except Exception as e:
        print(f"Warning: Could not run RAGAS evaluation: {e}")
        print("Continuing with custom evaluation only.")
    
    # Combine metrics
    metrics = {
        "classification_accuracy": accuracy,
        **ragas_metrics
    }
    
    # Print results
    print("\nModel Evaluation Results:")
    print(f"Model: {model_choice.value}")
    print(f"Metrics:")
    for metric, value in metrics.items():
        print(f"  {metric}: {value:.4f}")
    
    print(f"\nClassification Errors ({len(error_cases)} out of {len(test_results)}):")
    for case in error_cases:
        print(f"  Medication: {case['medication']}")
        print(f"  Expected: {case['expected']}")
        print(f"  Model Answer: {case['model_answer']}")
        print("")
    
    # Save results to file
    results = {
        "model": model_choice.value,
        "metrics": metrics,
        "error_cases": error_cases
    }
    
    with open(f"ragas_results_{model_choice.value}.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to ragas_results_{model_choice.value}.json")
    
    return test_results, metrics, error_cases

if __name__ == "__main__":
    # You can change the model here
    model_choice = ModelChoice.OLLAMA_DEEPSEEK
    main(model_choice)