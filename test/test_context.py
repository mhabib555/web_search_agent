from config.context import SubscriptionConfig, SUBSCRIPTION_CONFIGS, UserContext

def test_subscription_config_fields():
    """Verify SubscriptionConfig fields are correctly set."""
    config = SubscriptionConfig(tier="test", rate_per_min=5, wait_period=30)
    assert config.tier == "test"
    assert config.rate_per_min == 5
    assert config.wait_period == 30

def test_subscription_configs_dict():
    """Test SUBSCRIPTION_CONFIGS dictionary contains expected tiers and settings."""
    assert "free" in SUBSCRIPTION_CONFIGS
    assert "Pro" in SUBSCRIPTION_CONFIGS
    assert "Ultra" in SUBSCRIPTION_CONFIGS
    assert SUBSCRIPTION_CONFIGS["free"].tier == "free"
    assert SUBSCRIPTION_CONFIGS["Pro"].rate_per_min > SUBSCRIPTION_CONFIGS["free"].rate_per_min

def test_user_context_defaults():
    """Check default values of UserContext are correctly initialized."""
    user = UserContext(name="Alice")
    assert user.name == "Alice"
    assert user.city is None
    assert user.topic is None
    assert user.query is None
    assert user.subscription == ["free"]

def test_user_context_custom():
    """Verify UserContext initializes correctly with custom values."""
    user = UserContext(
        name="Bob",
        city="Paris",
        topic="AI",
        query="What is AI?",
        subscription=["Pro"]
    )
    assert user.name == "Bob"
    assert user.city == "Paris"
    assert user.topic == "AI"
    assert user.query == "What is AI?"
    assert user.subscription == ["Pro"]
