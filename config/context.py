from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class SubscriptionConfig:
    """Configuration for subscription tiers with rate limit settings."""
    tier: str
    rate_per_min: int
    wait_period: int  # seconds

# Predefined subscription configurations
SUBSCRIPTION_CONFIGS = {
    "free": SubscriptionConfig(tier="free", rate_per_min=10, wait_period=60),
    "Pro": SubscriptionConfig(tier="Pro", rate_per_min=20, wait_period=60),  # Example: Higher rate for Pro
    "Ultra": SubscriptionConfig(tier="Ultra", rate_per_min=50, wait_period=60)  # Example: Higher rate for Ultra
}

@dataclass
class UserContext:
    """User context to store personal information and preferences."""
    name: str
    city: Optional[str] = None
    topic: Optional[str] = None
    query: Optional[str] = None
    subscription: List[str] = field(default_factory=lambda: ["free"])  # Default to free tier