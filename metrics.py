class Metric:
    def __init__(self, name, schema, prompt):
        self.name = name
        self.schema = schema
        self.prompt = prompt

    def compute_score(self):
        raise NotImplementedError("Subclass must implement abstract method")



class CENTOR(Metric):
    def __init__(self):
        self.name="CENTOR Score"
        self.schema = "{\n  \"age\": int,\n  \"tonsil_swelling\": boolean,\n  \"lymph_swelling\": boolean,\n  \"temp\": float,\n  \"cough_present\": boolean\n}"
        self.prompt = f"given a medical record of a patient, extract the following pieces of information:\n\n1. age (integer)\n2. temperature in Celsius (float)\n3. exudate or swollen tonsils (boolean True/False)\n4. tender/swollen anterior cervical lymph nodes (boolean)\n5. cough present (boolean)\n\nuse the following schema for the output:\n\n{self.schema}"

    def compute_score(self, data):
        
        score = 0

        if 3 <= data['age'] <= 14:
            score += 1
        elif data['age'] >= 45:
            score -= 1
        
        if data['tonsil_swelling']:
            score += 1
        
        if data['lymph_swelling']:
            score += 1
        
        if data['temp'] > 38.0:
            score += 1
        
        if data['cough_present']:
            score += 1
        
        return score