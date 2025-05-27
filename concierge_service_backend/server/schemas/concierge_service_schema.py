from pydantic import BaseModel, Field, model_validator
from typing import List,Optional
from datetime import date as dt_date, time as dt_time
from datetime import datetime 
from server.enums import concierge_service_enum

    
class IntentCategorySchema(BaseModel):
    """Represents the intent category and confidence score of a user's query."""
    intent_category: concierge_service_enum.IntentCategoryEnum = Field(description="The predicted intent category of the user's query.")
    confidence_score: float = Field(ge=0, le=1, description="Confidence score (0 to 1) indicating how certain the model is about the predicted category.")

class DiningEntitieSchema(BaseModel):
    """Schema for dining-related intent entities, such as date, time, location, cuisine, party size, and budget."""

    dining_date: Optional[dt_date] = Field(None,description="Date of the dining reservation")
    dining_time: Optional[dt_time] = Field(None,description="Time of the dining reservation")
    location: Optional[str] = Field(None,description="Location or city for dining")
    cuisine: Optional[concierge_service_enum.CuisineTypeEnum] = Field(None,description="Preferred cuisine type")
    party_size: Optional[int] = Field(None,description="Number of people in the dining party")
    budget: Optional[float] = Field(None,gt=0, description="Estimated budget for dining (must be > 0)")
    @model_validator(mode="after")
    @classmethod
    def validate_date_and_time(cls, model):
        today = dt_date.today()
        now = datetime.now().time()

        if model.dining_date and model.dining_date < today:
            raise ValueError("Dining date must be today or in the future")

        if model.dining_date == today and model.dining_time and model.dining_time < now:
            raise ValueError("Dining time must be current or later")

        return model



class TravelEntitiesSchema(BaseModel):
    """Schema for travel-related intent entities including locations, dates, transport mode, and budget."""

    source_location: Optional[str] = Field(None,description="Starting point of travel")
    destination_location: Optional[str] = Field(None,description="Destination of the trip")
    travel_date: Optional[dt_date] = Field(None,description="Date of travel")
    return_date: Optional[dt_date] = Field(None,description="Date of return (if any)")
    mode_of_transport: Optional[concierge_service_enum.ModeOfTransportEnum] = Field(None,description="Preferred mode of transport")
    number_of_travelers: Optional[int] = Field(None,gt=0,description="Number of travelers")
    budget: Optional[float] = Field(None,gt=0, description="Estimated travel budget (must be > 0)")
    @model_validator(mode="after")
    @classmethod
    def validate_date_and_time(cls, model):
        today = dt_date.today()
        now = datetime.now().time()

        if model.travel_date and model.travel_date < today:
            raise ValueError("Travel date must be today or in the future")

        if model.return_date and model.travel_date < today:
            raise ValueError("Travel date must be today or in the future")

        if model.travel_date and model.return_date and model.travel_date <= model.return_date :
            raise ValueError("Travel date must be today or in the future")

        return model


class GiftingEntitiesSchema(BaseModel):
    """Schema for gifting-related intent entities including recipient, occasion, and delivery details."""

    recipient: Optional[str] = Field(None,description="Name or relation of the gift recipient")
    occasion: Optional[str] = Field(None,description="Occasion for the gift (e.g. birthday, anniversary)")
    budget: Optional[float] = Field(None,gt=0, description="Budget for the gift (must be > 0)")
    delivery_date: Optional[dt_date] = Field(None,description="Preferred delivery date for the gift")
    delivery_location: Optional[str] = Field(None,description="Delivery address or location")
    gift_type: Optional[concierge_service_enum.GiftTypeEnum] = Field(None,description="Preferred type of gift (e.g. flowers, gadgets)")
    @model_validator(mode="after")
    @classmethod
    def validate_date_and_time(cls, model):
        today = dt_date.today()
        now = datetime.now().time()

        if model.delivery_date and model.delivery_date < today:
            raise ValueError("Delivery date must be today or in the future")

        return model

class CabBookingEntitiesSchema(BaseModel):
    """Schema for cab booking-related intent entities such as pickup/drop locations and cab preferences."""

    pickup_location: Optional[str] = Field(None,description="Location where the cab should pick up")
    dropoff_location: Optional[str] = Field(None,description="Location where the cab should drop off")
    pickup_date: Optional[dt_date] = Field(None,description="Desired date of pickup")
    pickup_time: Optional[dt_time] = Field(None,description="Desired time of pickup")
    number_of_passengers: Optional[int] = Field(None,gt=0, description="Number of passengers for the ride")
    cab_type: Optional[concierge_service_enum.CabTypeEnum] = Field(None,description="Type of cab preferred (e.g. sedan, SUV)")
    price_range: Optional[float] = Field(None,gt=0, description="Estimated price range for the ride (must be > 0)")
    @model_validator(mode="after")
    @classmethod
    def validate_date_and_time(cls, model):
        today = dt_date.today()
        now = datetime.now().time()

        if model.pickup_date and model.pickup_date < today:
            raise ValueError("Pickup date must be today or in the future")

        if model.pickup_date == today and model.pickup_time and model.pickup_time < now:
            raise ValueError("Travel date must be today or in the future")

        return model

class FollowUpQuestionSchema(BaseModel):
    """Represents a single follow-up question for missing or ambiguous entity."""
    question: str = Field(description="The follow-up question to ask the user")
    field: str = Field(description="The missing field that this question addresses")
    options: Optional[List[str]] = Field(None, description="Suggested options for the user to choose from")
    required: bool = Field(True, description="Whether this entity is required to proceed")


class FollowUpQuestionsSchema(BaseModel):
    """Represents a collection of follow-up questions with their options."""
    question_config: List[FollowUpQuestionSchema] = Field(description="A list of questions, each with its type and potential answer options.")
  
  
INTENT_ENTITIES_SCHEMA_MAPPER = {
    "dining": DiningEntitieSchema,
    "travel": TravelEntitiesSchema,
    "gifting": GiftingEntitiesSchema,
    "cab booking": CabBookingEntitiesSchema,
}

