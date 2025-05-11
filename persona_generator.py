import random
from config import (
    AGE_DISTRIBUTION,
    EDUCATION_LEVELS,
    REGIONS,
    GENDER_DISTRIBUTION,
    EMPLOYMENT_DISTRIBUTION,
    PERSONAL_VALUES,
    LIFE_EXPERIENCES,
    PERSONALITY_TRAITS
)


class PersonaGenerator:
    def __init__(self):
        self.employment = EMPLOYMENT_DISTRIBUTION
        self.total_employment = sum(EMPLOYMENT_DISTRIBUTION.values())
        self.employment_probabilities = {
            k: v/self.total_employment
            for k, v in EMPLOYMENT_DISTRIBUTION.items()
        }

    def _sample_age(self):
        """Sample age based on US age distribution."""
        age_range = random.choices(
            list(AGE_DISTRIBUTION.keys()),
            weights=list(AGE_DISTRIBUTION.values())
        )[0]
        if age_range == "65+":
            return random.randint(65, 85)  # reasonable upper bound for 65+
        min_age, max_age = map(int, age_range.split('-'))
        return random.randint(min_age, max_age)

    def _sample_gender(self):
        """Sample gender based on US gender distribution."""
        return random.choices(
            list(GENDER_DISTRIBUTION.keys()),
            weights=list(GENDER_DISTRIBUTION.values())
        )[0]

    def _sample_education(self):
        """Sample education level."""
        return random.choice(EDUCATION_LEVELS)

    def _sample_region(self):
        """Sample US region."""
        return random.choice(REGIONS)

    def _sample_occupation(self):
        """Sample occupation based on employment statistics."""
        industry = random.choices(
            list(self.employment_probabilities.keys()),
            weights=list(self.employment_probabilities.values())
        )[0]
        return industry

    def _sample_personal_values(self):
        """Sample 2-3 personal values that influence decision making."""
        num_values = random.randint(2, 3)
        return random.sample(PERSONAL_VALUES, num_values)

    def _sample_life_experiences(self):
        """Sample 1-2 significant life experiences."""
        num_experiences = random.randint(1, 2)
        return random.sample(LIFE_EXPERIENCES, num_experiences)

    def _sample_personality_traits(self):
        """Sample personality traits for each dimension."""
        return {
            trait: random.choice(levels)
            for trait, levels in PERSONALITY_TRAITS.items()
        }

    def generate_persona(self):
        """Generate a single persona with realistic demographic and
        psychological attributes."""
        return {
            'age': self._sample_age(),
            'gender': self._sample_gender(),
            'education': self._sample_education(),
            'region': self._sample_region(),
            'occupation': self._sample_occupation(),
            'personal_values': self._sample_personal_values(),
            'life_experiences': self._sample_life_experiences(),
            'personality_traits': self._sample_personality_traits()
        }

    def generate_personas(self, num_personas):
        """Generate multiple unique personas."""
        return [self.generate_persona() for _ in range(num_personas)]
