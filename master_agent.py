from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY, DEFAULT_MODEL, DEFAULT_NUM_PERSONAS
from prompts import MASTER_AGENT_PROMPT_TEMPLATE
from persona_generator import PersonaGenerator
from persona_agent import PersonaAgent
import json
import concurrent.futures


class MasterAgent:
    def __init__(self, num_personas=DEFAULT_NUM_PERSONAS):
        """Initialize the master agent with a specified number of personas."""
        self.num_personas = num_personas
        self.persona_generator = PersonaGenerator()
        self.llm = ChatOpenAI(
            openai_api_key=OPENAI_API_KEY,
            model_name=DEFAULT_MODEL,
            temperature=0.7
        )
        self.personas = self._initialize_personas()

    def _initialize_personas(self):
        """Initialize the specified number of persona agents."""
        persona_attributes = self.persona_generator.generate_personas(
            self.num_personas
        )
        return [PersonaAgent(attrs) for attrs in persona_attributes]

    def _get_persona_response(self, persona):
        """Get response from a single persona."""
        response = persona.get_response(self.current_question)
        try:
            response_data = json.loads(response)
            return {
                'persona': str(persona),
                'data': response_data
            }
        except json.JSONDecodeError:
            return {
                'persona': str(persona),
                'data': {'error': 'Invalid JSON response', 'raw': response}
            }

    def get_crowd_response(self, question):
        """Get responses from all personas and aggregate them."""
        # Store question for parallel processing
        self.current_question = question

        # Get individual responses in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            responses = list(
                executor.map(self._get_persona_response, self.personas)
            )

        # Count Yes/No responses
        yes_count = 0
        no_count = 0
        formatted_responses = []
        invalid_responses = []

        for response in responses:
            try:
                if 'error' in response['data']:
                    error_msg = (
                        f"Persona ({response['persona']}): "
                        f"{response['data']['raw']}"
                    )
                    invalid_responses.append(error_msg)
                    formatted_responses.append(error_msg)
                    continue

                answer = response['data']['answer'].lower()
                if answer == 'yes':
                    yes_count += 1
                elif answer == 'no':
                    no_count += 1
                else:
                    invalid_msg = (
                        f"Persona ({response['persona']}): "
                        f"Invalid answer '{answer}'"
                    )
                    invalid_responses.append(invalid_msg)

                response_msg = (
                    f"Persona ({response['persona']}): "
                    f"{json.dumps(response['data'], indent=2)}"
                )
                formatted_responses.append(response_msg)
            except (KeyError, AttributeError) as e:
                error_msg = (
                    f"Persona ({response['persona']}): "
                    f"Invalid response format - {str(e)}"
                )
                invalid_responses.append(error_msg)
                formatted_responses.append(error_msg)
                continue

        # Print warnings for invalid responses
        if invalid_responses:
            print("\nWARNING: Some personas provided invalid responses:")
            for msg in invalid_responses:
                print(f"- {msg}")
            print(
                f"\nTotal invalid responses: {len(invalid_responses)} "
                f"out of {len(responses)}"
            )

        total_responses = yes_count + no_count
        if total_responses > 0:
            yes_percentage = (yes_count / total_responses) * 100
            no_percentage = (no_count / total_responses) * 100
        else:
            yes_percentage = 0
            no_percentage = 0

        # Format responses for the master prompt
        formatted_responses_str = "\n\n".join(formatted_responses)

        # Get aggregated response from master agent
        master_prompt = MASTER_AGENT_PROMPT_TEMPLATE.format(
            question=question,
            responses=formatted_responses_str,
            yes_count=yes_count,
            no_count=no_count,
            yes_percentage=yes_percentage,
            no_percentage=no_percentage
        )

        master_response = self.llm.invoke([("system", master_prompt)])

        try:
            # Clean the response by removing markdown code block markers
            content = master_response.content
            if content.startswith("```json"):
                content = content[7:]  # Remove ```json
            if content.endswith("```"):
                content = content[:-3]  # Remove ```
            content = content.strip()

            # Parse master's JSON response
            analysis_data = json.loads(content)

            # Combine Python-calculated statistics with master's analysis
            aggregated_data = {
                'yes_count': yes_count,
                'no_count': no_count,
                'yes_percentage': yes_percentage,
                'no_percentage': no_percentage,
                'valid_responses': total_responses,
                'invalid_responses': len(invalid_responses),
                **analysis_data  # Include master's analysis
            }

            return {
                'individual_responses': formatted_responses,
                'aggregated_response': aggregated_data
            }
        except json.JSONDecodeError as e:
            return {
                'individual_responses': formatted_responses,
                'aggregated_response': {
                    'error': 'Invalid JSON response from master agent',
                    'raw_response': master_response.content,
                    'error_details': str(e)
                }
            }

    def __str__(self):
        """String representation of the master agent and its personas."""
        return (
            f"Master Agent with {self.num_personas} personas:\n" +
            "\n".join(f"- {persona}" for persona in self.personas)
        )
