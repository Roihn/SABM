import openai
import time

class PersonalizedAgent:
    def __init__(self, id, gender, ethnicity, education, occupation, location, temperature=0.8, model='gpt-3.5-turbo', max_tokens=64, persona = "", api_key = ""):
        self.id = id
        self.gender = gender
        self.ethnicity = ethnicity
        self.education = education
        self.occupation = occupation
        self.location = location
        self.personality_score = 0
        self.temperature = temperature
        self.persona = persona
        self.tcu_scale = None

        self.group = 1
        self.decision = {}
        self.decision_reason = {}

        self.model = model
        self.max_tokens = max_tokens

        self.api_key = api_key
        openai.api_key = self.api_key
    
    def communicate(self, context):
        prompt = context + "\n\n"
        message = ""

        retries = 3
        backoff_factor = 2
        current_retry = 0

        while current_retry < retries:
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "user", "content": prompt},
                        {"role": "user", "content": ""}
                    ],
                    max_tokens=self.max_tokens,
                    n=1,
                    temperature=self.temperature,
                    top_p=1
                )
                message = response['choices'][0]['message']['content'].strip()
                #print(message)
                return message
            except openai.error.RateLimitError as e:
                if current_retry < retries - 1:
                    wait_time = backoff_factor ** current_retry
                    print(f"RateLimitError: Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    current_retry += 1
                else:
                    print(f"Error {e}")
                    raise e
            except Exception as e:
                if current_retry < retries - 1:
                    wait_time = backoff_factor ** current_retry
                    print(f"RateLimitError: Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    current_retry += 1
                else:
                    print(f"Error {e}")
                    raise e

    def generate_persona(self):
        persona = f"{self.gender}, {self.ethnicity}, {self.education}, {self.occupation}, living in a {self.location} area"
        return persona
