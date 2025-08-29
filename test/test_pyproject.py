import toml

def test_pyproject_toml_fields():
    data = toml.load("pyproject.toml")
    assert "project" in data
    project = data["project"]
    assert project["requires-python"] == ">=3.10"
    assert "dependencies" in project
    deps = project["dependencies"]
    assert any("openai-agents" in dep for dep in deps)
    assert any("tavily-python" in dep for dep in deps)

def test_pyproject_dev_dependencies():
    data = toml.load("pyproject.toml")
    assert "dependency-groups" in data
    dev = data["dependency-groups"]["dev"]
    assert any("pytest" in dep for dep in dev)
    assert any("pytest-asyncio" in dep for dep in dev)