import os
import tempfile
from pathlib import Path
from typing import Dict, Any, Generator
import pytest
import yaml


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Provide a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_yaml_content() -> Dict[str, Any]:
    """Provide sample YAML content for testing."""
    return {
        "rules": [
            {
                "name": "TestApp",
                "domains": ["example.com", "test.example.com"],
                "ips": ["192.168.1.1", "10.0.0.1"],
            }
        ]
    }


@pytest.fixture
def sample_yaml_file(temp_dir: Path, sample_yaml_content: Dict[str, Any]) -> Path:
    """Create a sample YAML file for testing."""
    yaml_file = temp_dir / "test_rules.yaml"
    with open(yaml_file, "w") as f:
        yaml.dump(sample_yaml_content, f)
    return yaml_file


@pytest.fixture
def mock_config() -> Dict[str, Any]:
    """Provide mock configuration for testing."""
    return {
        "output_dir": "generated",
        "formats": ["quantumultx", "surge", "clash"],
        "parser_header": "parser-header.yaml",
    }


@pytest.fixture
def sample_rules_data() -> Dict[str, Any]:
    """Provide sample rules data structure."""
    return {
        "TestApp": {
            "domains": ["app.example.com", "api.example.com"],
            "ips": ["1.2.3.4", "5.6.7.8"],
            "description": "Test application rules",
        }
    }


@pytest.fixture
def generated_dir(temp_dir: Path) -> Path:
    """Create a temporary generated directory."""
    gen_dir = temp_dir / "generated"
    gen_dir.mkdir(exist_ok=True)
    return gen_dir


@pytest.fixture
def parser_header_content() -> str:
    """Provide sample parser header content."""
    return """# Generated rules
# Version: 1.0.0

mixed-port: 7890
allow-lan: false
mode: rule
log-level: info
"""


@pytest.fixture
def parser_header_file(temp_dir: Path, parser_header_content: str) -> Path:
    """Create a parser header file for testing."""
    header_file = temp_dir / "parser-header.yaml"
    with open(header_file, "w") as f:
        f.write(parser_header_content)
    return header_file


@pytest.fixture(autouse=True)
def change_test_dir(request, monkeypatch):
    """Automatically change to test directory for file-based tests."""
    if "no_chdir" not in request.keywords:
        monkeypatch.chdir(request.fspath.dirname)


@pytest.fixture
def mock_git_repo(temp_dir: Path, monkeypatch):
    """Mock a git repository for testing."""
    git_dir = temp_dir / ".git"
    git_dir.mkdir()
    monkeypatch.setenv("GIT_DIR", str(git_dir))
    return temp_dir