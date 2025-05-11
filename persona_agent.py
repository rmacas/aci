from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY, DEFAULT_MODEL
from prompts import PERSONA_PROMPT_TEMPLATE
import json


class PersonaAgent:
    def __init__(self, persona_attributes):
        """Initialize a persona agent with specific demographic and
        psychological attributes."""
        self.attributes = persona_attributes
        self.llm = ChatOpenAI(
            openai_api_key=OPENAI_API_KEY,
            model_name=DEFAULT_MODEL,
            temperature=0.7
        )

    def get_response(self, question):
        """Get a response from this persona for a given question."""
        # Determine employment status and retirement info
        age = self.attributes['age']
        if age >= 65:
            employment_status = "retired"
            retirement_info = (
                f"You previously worked in {self.attributes['occupation']} "
                "before retiring."
            )
        else:
            employment_status = f"working as a {self.attributes['occupation']}"
            retirement_info = ""

        # Format personal values and experiences
        values_str = ", ".join(self.attributes['personal_values'])
        experiences_str = ", ".join(self.attributes['life_experiences'])
        personality_str = ", ".join(
            f"{trait}: {level}"
            for trait, level in self.attributes['personality_traits'].items()
        )

        # Format the prompt with persona attributes and question
        prompt = PERSONA_PROMPT_TEMPLATE.format(
            age=self.attributes['age'],
            gender=self.attributes['gender'],
            employment_status=employment_status,
            region=self.attributes['region'],
            education=self.attributes['education'],
            retirement_info=retirement_info,
            personal_values=values_str,
            life_experiences=experiences_str,
            personality_traits=personality_str,
            question=question
        )

        try:
            # Get response from LLM
            response = self.llm.invoke([("system", prompt)])
            if hasattr(response, 'content'):
                return response.content
            elif isinstance(response, dict) and 'choices' in response:
                return response['choices'][0]['message']['content']
            else:
                return str(response)
        except Exception as e:
            return json.dumps({
                'answer': 'No',
                'reason': f'Error getting response: {str(e)}'
            })

    def __str__(self):
        """String representation of the persona."""
        age = self.attributes['age']
        if age >= 65:
            occupation = f"retired (formerly {self.attributes['occupation']})"
        else:
            occupation = self.attributes['occupation']

        values = ", ".join(self.attributes['personal_values'])
        experiences = ", ".join(self.attributes['life_experiences'])

        return (
            f"{self.attributes['age']}-year-old {self.attributes['gender']} "
            f"{occupation} from {self.attributes['region']} "
            f"with {self.attributes['education']}\n"
            f"Values: {values}\n"
            f"Experiences: {experiences}"
        )
