# Artificial Crowd Intelligence

A Python-based system that simulates "wisdom of the crowd" by generating diverse AI personas and aggregating their responses to questions. The system uses OpenAI's language models to create realistic personas with unique backgrounds, values, and perspectives.

For more background on the concept I try to replicate, see [Wisdom of the crowd wiki page](https://en.wikipedia.org/wiki/Wisdom_of_the_crowd). 

Based on initial testing, the personas' answers are not very diverse, likely because they rely too heavily on the internal knowledge of the LLM.

## Features

- Generate diverse personas with realistic backgrounds and characteristics
- Parallel processing of persona responses for improved performance
- JSON-formatted responses with clear Yes/No answers and concise reasoning
- Visualization of response distribution
- Detailed analysis of crowd responses including demographic insights
- Error handling and validation of responses

## Requirements

- Python 3.8+
- OpenAI API key
- Required packages (see requirements.txt):
  - langchain
  - langchain-openai
  - matplotlib
  - numpy

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Usage

1. Run the main script:
```bash
python main.py
```

2. Enter your question when prompted. The system will:
   - Generate diverse personas
   - Gather their responses
   - Display individual responses
   - Show aggregated analysis
   - Visualize the Yes/No distribution

## Project Structure

- `main.py`: Entry point and user interface
- `master_agent.py`: Handles persona management and response aggregation
- `persona_agent.py`: Individual persona response generation
- `persona_generator.py`: Creates diverse personas with unique characteristics
- `prompts.py`: Contains prompt templates for personas and master agent
- `config.py`: Configuration settings and constants

## Response Format

### Individual Persona Response
```json
{
    "answer": "Yes" or "No",
    "reason": "A simple string with 1-2 sentences explaining the decision"
}
```

### Master Agent Analysis
```json
{
    "yes_count": <number>,
    "no_count": <number>,
    "yes_percentage": <percentage>,
    "no_percentage": <percentage>,
    "key_reasons": [
        "List of main reasons given for Yes responses",
        "List of main reasons given for No responses"
    ],
    "demographic_insights": "Analysis of how different demographics influenced the responses",
    "consensus_level": "High/Medium/Low based on the distribution of responses"
}
```

## Error Handling

The system includes comprehensive error handling:
- Validates JSON responses from personas
- Tracks and reports invalid responses
- Provides detailed error messages for debugging
- Maintains system stability even with partial failures


## License

This project is licensed under the MIT License - see the LICENSE file for details. 
