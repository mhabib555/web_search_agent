from dataclasses import dataclass, field
from typing import List, Optional
from pydantic import BaseModel

@dataclass
class SubscriptionConfig:
    """Configuration for subscription tiers with rate limit settings."""
    tier: str
    rate_per_min: int
    wait_period: int  # seconds

# Predefined subscription configurations
SUBSCRIPTION_CONFIGS = {
    "free": SubscriptionConfig(tier="free", rate_per_min=10, wait_period=60),
    "Pro": SubscriptionConfig(tier="Pro", rate_per_min=20, wait_period=60),
    "Ultra": SubscriptionConfig(tier="Ultra", rate_per_min=50, wait_period=60)
}

@dataclass
class UserContext:
    """User context to store personal information and preferences."""
    name: str
    city: Optional[str] = None
    topic: Optional[str] = None
    query: Optional[str] = None
    subscription: List[str] = field(default_factory=lambda: ["free"]) 


class InformationGatheringAnswer(BaseModel):
    """Represents the structured response from an information-gathering agent.

    This class defines the schema for data returned by an information-gathering process,
    including whether the information is complete and the collected data.

    Attributes:
        is_information_complete (bool): Indicates whether the information-gathering process
            has collected all required data.
        data (str): The collected data or response from the information-gathering agent.
    """
    is_information_complete: bool
    data: str
