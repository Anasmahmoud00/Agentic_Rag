# /content/Basir_RAG_Agents/core/models/schemas.py
from typing import List, Optional
from pydantic import BaseModel, Field

# --- Activity Schemas ---
class SingleActivitySchema(BaseModel):
    Country: str = Field(..., description="Country where the activity is available")
    City: str = Field(..., description="City where the activity is located")
    ActivityName: str = Field(..., description="Name of the activity")
    Description: str = Field(..., description="Detailed description of the activity")
    Category: str = Field(..., description="Type/category of activity")
    PriceRange: Optional[str] = Field(..., description="Approximate cost range")
    BestTimeToVisit: Optional[str] = Field(..., description="Recommended time for this activity")
    Duration: Optional[str] = Field(..., description="How long the activity typically takes")
    Location: Optional[str] = Field(..., description="Specific location or address")

class ActivityOutputSchema(BaseModel):
    activities: List[SingleActivitySchema]

# --- Accommodation Schemas ---
class SingleAccommodationSchema(BaseModel):
    Country: str = Field(..., description="Country where accommodation is located")
    City: str = Field(..., description="City where accommodation is located")
    Name: str = Field(..., description="Name of the accommodation")
    Type: str = Field(..., description="Type of accommodation (hotel, hostel, etc.)")
    PriceRange: str = Field(..., description="Price range in USD")
    Location: str = Field(..., description="Location details")
    Rating: Optional[str] = Field(..., description="Rating if available")
    Amenities: Optional[List[str]] = Field(..., description="List of amenities")

class AccommodationOutputSchema(BaseModel):
    accommodations: List[SingleAccommodationSchema]

# --- Dish Schemas ---
class SingleDishSchema(BaseModel):
    Country: str = Field(..., description="Country where dish originates")
    Region: Optional[str] = Field(..., description="Specific region if applicable")
    DishName: str = Field(..., description="Name of the dish")
    Description: str = Field(..., description="Description of the dish")
    Ingredients: List[str] = Field(..., description="Main ingredients")
    TypicalMealTime: Optional[str] = Field(..., description="When it's typically eaten")
    Vegetarian: Optional[bool] = Field(..., description="Whether it's vegetarian")

class DishOutputSchema(BaseModel):
    dishes: List[SingleDishSchema]

# --- Restaurant Schemas ---
class SingleRestaurantSchema(BaseModel):
    Country: str = Field(..., description="Country where restaurant is located")
    City: str = Field(..., description="City where restaurant is located")
    Name: str = Field(..., description="Name of the restaurant")
    CuisineType: str = Field(..., description="Type of cuisine served")
    PriceRange: str = Field(..., description="Price range indicator")
    Address: str = Field(..., description="Physical address")
    Rating: Optional[str] = Field(..., description="Rating if available")
    SpecialDiets: Optional[List[str]] = Field(..., description="Dietary options available")

class RestaurantOutputSchema(BaseModel):
    restaurants: List[SingleRestaurantSchema]

# --- Scam Schemas ---
class SingleScamSchema(BaseModel):
    Country: str = Field(..., description="Country where the scam is common.")
    City: Optional[str] = Field(..., description="City where the scam is common.")
    ScamType: str = Field(..., description="The type or name of the scam.")
    Description: str = Field(..., description="A detailed description of how the scam works.")
    Location: str = Field(..., description="Specific locations where the scam often occurs (e.g., tourist areas, train stations).")
    PreventionTips: str = Field(..., description="Actionable tips on how to avoid this scam.")

class ScamOutputSchema(BaseModel):
    scams: List[SingleScamSchema]

# --- Seasonal Schemas ---
class SingleSeasonalSchema(BaseModel):
    Country: str = Field(..., description="The country the seasonal information pertains to.")
    Question: str = Field(..., description="The user's question about seasonal travel (e.g., 'best time to visit').")
    Answer: str = Field(..., description="A detailed answer regarding seasons, weather, and best travel times.")

class SeasonalOutputSchema(BaseModel):
    seasonals: List[SingleSeasonalSchema]

# --- Transportation Schemas ---
class SingleTransportationSchema(BaseModel):
    Country: str = Field(..., description="Country of the transport option.")
    From: str = Field(..., description="Starting point of the journey.")
    To: str = Field(..., description="Destination of the journey.")
    TransportMode: str = Field(..., description="Mode of transport (e.g., Train, Bus, Ferry).")
    Provider: Optional[str] = Field(..., description="The company providing the service.")
    Schedule: Optional[str] = Field(..., description="Information on schedules or frequency.")
    DurationInHours: Optional[str] = Field(..., description="Estimated duration of the trip in hours.")
    PriceRangeInUSD: Optional[str] = Field(..., description="Typical price range in USD.")
    CostDetailsAndOptions: Optional[str] = Field(..., description="More details on costs and options.")
    AdditionalInfo: Optional[str] = Field(..., description="Any other relevant information.")

class TransportationOutputSchema(BaseModel):
    transportations: List[SingleTransportationSchema]

# --- Visa Schemas ---
class SingleVisaSchema(BaseModel):
    Country: str = Field(..., description="The country the visa information pertains to.")
    Question: str = Field(..., description="The user's question about visa requirements.")
    Answer: str = Field(..., description="A clear and concise answer to the visa question.")

class VisaOutputSchema(BaseModel):
    visas: List[SingleVisaSchema]