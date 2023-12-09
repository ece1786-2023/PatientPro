import re

class Metric:
    name = ""
    id = ""
    schema = ""
    gen_prompt = ""

    def compute_score(self):
        raise NotImplementedError("Subclass must implement abstract method")
    
    def extract_keys(self):
        keys = re.findall(r'\"(.*?)\":', self.schema)
        return keys

class Centor(Metric):
    name = "Centor Score"
    id = "centor"
    schema = (
        "{\n"
        "  \"age\": int,\n"
        "  \"tonsil_swelling\": bool,\n"
        "  \"lymph_swelling\": bool,\n"
        "  \"temp\": float,\n"
        "  \"cough_present\": bool\n"
        "}"
    )
    prompt = (
        "Given a medical record of a patient, extract the following pieces of information:\n\n"
        "1. Age (integer)\n"
        "2. Temperature in Celsius (float)\n"
        "3. Exudate or swollen tonsils (boolean True/False)\n"
        "4. Tender/swollen anterior cervical lymph nodes (boolean)\n"
        "5. Cough present (boolean)\n\n"
        "Use the following schema for the output:\n\n"
        f"{schema}"
    )
    gen_prompt = (
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
    name = "qSOFA Score"
    id = "qsofa"
    schema = (
        "{\n"
        "  \"altered_mental\": boolean,\n"
        "  \"systolic_bp\": int,\n"
        "  \"respiratory_rate\": int\n"
        "}"
    )
    prompt = (
        "Given a medical record of a patient, extract the following pieces of information:\n\n"
        "1. Altered mental state including confusion, non-responsiveness, or reduction in Glasgow coma scale (boolean).\n"
        "2. Respiratory rate RR (integer).\n"
        "3. Systolic blood pressure: (integer).\n\n"
        "Additional notes:\n"
        "For Altered mental status, look for neurologic assessment.\n"
        "Do not report values from the HPI (History of Present Illness) section, only current readings.\n\n"
        "Use the following schema for the output, and ensure that it is strictly followed:\n"
        "for Respiratory rate, igonore RR (spontaneous) unless it's the only one present\n\n"
        f"{schema}"
    )
    # TODO: Generation prompt for qSOFA metric

    def compute_score(self, data):
        score = 0
        if data['altered_mental'] == True:  score += 1
        if data['respiratory_rate'] >= 22:  score += 1
        if data['systolic_bp'] <= 100:      score += 1
        return score

class NEWS2(Metric):
    name = "NEWS2 Score"
    id = "news2"
    schema = (
        "{\n"
        "  \"respiratory_rate\": int,\n"
        "  \"o2_saturation\": int,\n"
        "  \"supplemental_o2\": boolean,\n"
        "  \"temperature\": float,\n"
        "  \"systolic_bp\": int,\n"
        "  \"heart_rate\": int,\n"
        "  \"AVPU\": string,\n"
        "}"
    )
    prompt = (
        "Given a medical record of a patient, extract the following pieces of information:\n\n"
        "1. Respiratory rate RR (integer).\n"
        "2. Oxygen saturation percentage SpO2 (integer).\n"
        "3. If the patient is receiving supplemental oxygen (boolean).\n"
        "4. Temperature in Celsius (float).\n"
        "5. Systolic blood pressure (integer).\n"
        "6. Heart Rate bpm (integer)\n"
        "6. AVPU Score: (single character). One of {A, V, P, U} based on if the patient is fully Awake," 
                        "responds to Verbal stimulation, responds to Painful stimulation, or is Unresponsive, respectively.\n\n"
        "Additional notes:\n"
        "Do not report values from the HPI (History of Present Illness) section, only current readings.\n"
        "For Respiratory rate, ignore RR (spontaneous) unless it's the only one present.\n"
        "Use the following schema for the output, and ensure that it is strictly followed:\n\n"
        f"{schema}"
    )
    def compute_score(self, data):
        score = 0
        
        RR = data['respiratory_rate']
        if      RR <= 8:            score += 3
        elif    9  <= RR <= 11:     score += 1
        elif    12 <= RR <= 20:     score += 0
        elif    21 <= RR <= 24:     score += 2
        elif    RR >= 25:           score += 3

        O2 = data['o2_saturation']
        if      O2 <= 91:           score += 3
        elif    92 <= O2 <= 93:     score += 2 
        elif    94 <= O2 <= 95:     score += 1 
        elif    O2 >= 96:           score += 0

        SO2 = data['supplemental_o2']
        if SO2 == True:             score += 2

        T = data['temperature']
        if      T <= 35.0:          score += 3
        elif    35.1 <= T <= 36.0:  score += 1
        elif    36.1 <= T <= 38.0:  score += 0
        elif    38.1 <= T <= 39.0:  score += 1
        elif    T >= 39.1:          score += 2

        SBP = data['systolic_bp']
        if      SBP <= 90:          score += 3
        elif    91  <= SBP <= 100:  score += 2
        elif    101 <= SBP <= 110:  score += 1
        elif    111 <= SBP <= 219:  score += 0
        elif    SBP >= 220:         score += 3

        HR = data['heart_rate']
        if      HR  <= 40:          score += 3
        elif    41  <= HR <= 50:    score += 1
        elif    51  <= HR <= 90:    score += 0
        elif    91  <= HR <= 110:   score += 1
        elif    111 <= HR <= 130:   score += 2
        elif    HR  >= 131:         score += 3

        AVPU = data['AVPU']
        if AVPU == 'A':             score += 0
        elif AVPU in {'V','P','U'}: score += 3

        return score

def get_metric(metric_str):
    metric_classes = {cls.id: cls for cls in Metric.__subclasses__()}
    metric_class = metric_classes.get(metric_str)
    if metric_class:
        return metric_class()
    else:
        print("[ERROR] invalid metric")
        return None