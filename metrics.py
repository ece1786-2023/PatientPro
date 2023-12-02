class Metric:
    def __init__(self, name, schema, prompt):
        self.name = name
        self.schema = schema
        self.prompt = prompt

    def compute_score(self):
        raise NotImplementedError("Subclass must implement abstract method")

class Centor(Metric):
    def __init__(self):
        self.name="Centor Score"
        self.schema = (
            "{\n"
            "  \"age\": int,\n"
            "  \"tonsil_swelling\": bool,\n"
            "  \"lymph_swelling\": bool,\n"
            "  \"temp\": float,\n"
            "  \"cough_present\": bool\n"
            "}"
        )
        self.prompt = (
            "Given a medical record of a patient, extract the following pieces of information:\n\n"
            "1. Age (integer)\n"
            "2. Temperature in Celsius (float)\n"
            "3. Exudate or swollen tonsils (boolean True/False)\n"
            "4. Tender/swollen anterior cervical lymph nodes (boolean)\n"
            "5. Cough present (boolean)\n\n"
            "Use the following schema for the output:\n\n"
            f"{self.schema}"
        )
        self.gen_prompt = (
            "The new generated records should have different data but a similar chief complaint.\n\n"
            "Make sure to vary the following data:\n\n"
            "1. Age\n"
            "2. Temp\n"
            "3. Tonsils condition\n"
            "4. Lymph nodes condition\n"
            "5. Cough presence\n\n"
        )

    def compute_score(self, data):
        score = 0
        if 3 <= data['age'] <= 14:  score += 1
        elif data['age'] >= 45:     score -= 1
        if data['tonsil_swelling']: score += 1
        if data['lymph_swelling']:  score += 1
        if data['temp'] > 38.0:     score += 1
        if data['cough_present']:   score += 1
        return score
    

class qSOFA(Metric):
    def __init__(self):
        self.name = "qSOFA Score"
        self.schema = (
            "{\n"
            "  \"altered_mental\": boolean,\n"
            "  \"systolic_bp\": int,\n"
            "  \"respiratory_rate\": int\n"
            "}"
        )
        self.prompt = (
            "Given a medical record of a patient, extract the following pieces of information:\n\n"
            "1. Altered mental status, possibly based on eye, verbal and motor response: (boolean)\n"
            "2. Respiratory rate (integer)\n"
            "3. Systolic blood pressure: (integer)\n\n"
            "Use the following schema for the output, and ensure that it is strictly followed:\n\n"
            f"{self.schema}"
        )
        # TODO: Generation prompt for qSOFA metric
        self.gen_prompt=""

    def compute_score(self, data):
        score = 0
        if data['altered_mental'] == True:  score += 1
        if data['respiratory_rate'] >= 22:  score += 1
        if data['systolic_bp'] <= 100:      score += 1
        return score
