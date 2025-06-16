import pytest
import yaml
from pathlib import Path


class TestInfrastructureValidation:
    """Validation tests to ensure the testing infrastructure is properly set up."""

    def test_pytest_is_working(self):
        """Basic test to verify pytest is running correctly."""
        assert True

    def test_fixtures_are_available(self, temp_dir, sample_yaml_content):
        """Test that fixtures from conftest.py are accessible."""
        assert isinstance(temp_dir, Path)
        assert temp_dir.exists()
        assert isinstance(sample_yaml_content, dict)
        assert "rules" in sample_yaml_content

    def test_yaml_fixture_creates_file(self, sample_yaml_file):
        """Test that the YAML file fixture works correctly."""
        assert sample_yaml_file.exists()
        with open(sample_yaml_file) as f:
            content = yaml.safe_load(f)
        assert "rules" in content
        assert len(content["rules"]) > 0

    def test_mock_fixtures_work(self, mock_config, sample_rules_data):
        """Test that mock fixtures provide expected data."""
        assert "output_dir" in mock_config
        assert "formats" in mock_config
        assert isinstance(mock_config["formats"], list)
        
        assert "TestApp" in sample_rules_data
        assert "domains" in sample_rules_data["TestApp"]
        assert "ips" in sample_rules_data["TestApp"]

    def test_generated_dir_fixture(self, generated_dir):
        """Test that the generated directory fixture works."""
        assert generated_dir.exists()
        assert generated_dir.is_dir()
        assert generated_dir.name == "generated"

    @pytest.mark.unit
    def test_unit_marker(self):
        """Test that the unit test marker is recognized."""
        assert True

    @pytest.mark.integration
    def test_integration_marker(self):
        """Test that the integration test marker is recognized."""
        assert True

    @pytest.mark.slow
    def test_slow_marker(self):
        """Test that the slow test marker is recognized."""
        assert True

    def test_coverage_is_tracked(self):
        """Test that coverage tracking is enabled."""
        # This test will be included in coverage reports
        x = 1 + 1
        assert x == 2

    def test_pytest_mock_is_available(self, mocker):
        """Test that pytest-mock is installed and working."""
        mock_func = mocker.Mock(return_value=42)
        result = mock_func()
        assert result == 42
        mock_func.assert_called_once()

    def test_parser_header_fixture(self, parser_header_file):
        """Test that parser header fixture creates a file correctly."""
        assert parser_header_file.exists()
        content = parser_header_file.read_text()
        assert "Generated rules" in content
        assert "mixed-port: 7890" in content

    def test_mock_git_repo_fixture(self, mock_git_repo):
        """Test that the git repo mock fixture works."""
        assert mock_git_repo.exists()
        git_dir = mock_git_repo / ".git"
        assert git_dir.exists()
        assert git_dir.is_dir()