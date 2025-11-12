from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated
import pickle
import pandas as pd

#load the model file
with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)

#creating an instance of FastAPI
app = FastAPI()

#list of cities
tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]


#pydantic model for validating the user input
class UserInput(BaseModel):
   
    age: Annotated[int, Field(..., gt=0, lt=75,description="Age of the user")]
    weight: Annotated[float, Field(..., gt=0, description="weight of the person")]
    height: Annotated[float, Field(..., gt=0, lt=2.5, description="Height of the person")]
    income_lpa: Annotated[float, Field(..., gt=0, description="Salary of the user in lpa")]
    smoker: Annotated[bool, Field(...,description="Is the user smoker or not")]
    city: Annotated[str, Field(..., description="City the user lives in")]
    occupation: Annotated[str,Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'],Field(..., description="occupation of the user")]
    
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight/(self.height**2)

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
    
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "Middle-age"
        else:
            return "senior"
        
    @computed_field
    @property
    def city_tier(self) -> str:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
        
@app.get('/')
def home():
    return {'message':'Insurance Premium Prediction API'}

# machine readable
@app.get('/health')
def health_check():
    return {
        'status': 'OK'   
    }
#creating an api endpoint
@app.post('/predict')
def response(data : UserInput):
    input = pd.DataFrame([{
        'bmi': data.bmi,
        'age_group' : data.age_group,
        'lifestyle_risk' : data.lifestyle_risk,
        'city_tier' : data.city_tier,
        'income_lpa' : data.income_lpa,
        'occupation' : data.occupation
        }])
    Prediction = model.predict(input)[0]

   
    return JSONResponse(
    status_code=200,
    content={
        "response": {
            "predicted_category": Prediction,
            "confidence": 0.92,  # optional
            "class_probabilities": {"Low": 0.05, "Medium": 0.03, "High": 0.92}  # optional
        }
    }
)




