from config.fake_data import fake_users

def test_fake_users_is_list():
    """Verify that fake_users is a non-empty list."""
    assert isinstance(fake_users, list)
    assert len(fake_users) > 0

def test_fake_user_fields():
    """Check that each fake user has required fields with correct types."""
    required_fields = {"name", "city", "topic", "subscription"}
    for user in fake_users:
        assert required_fields.issubset(user.keys())
        assert isinstance(user["name"], str)
        assert "subscription" in user
        assert isinstance(user["subscription"], list)
        assert len(user["subscription"]) > 0
