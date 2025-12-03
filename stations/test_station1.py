"""Tests for station1.py weather station simulator."""
import os
from unittest.mock import patch

import pytest

from station1 import (
    create_data_payload,
    generate_humidity,
    generate_temperature,
    get_config,
)


class TestGenerateTemperature:
    """Tests for temperature generation."""

    def test_temperature_in_normal_range(self):
        """Test that normal temperatures fall within expected range."""
        # Run multiple times to test randomness
        temperatures = [generate_temperature() for _ in range(100)]

        # Filter out error sentinel values
        normal_temps = [t for t in temperatures if t != -999]

        # All normal temperatures should be between 15 and 30
        assert all(15 <= t <= 30 for t in normal_temps)
        # Should have mostly normal values
        assert len(normal_temps) > 90

    def test_temperature_error_values_present(self):
        """Test that error sentinel values (-999) occasionally appear."""
        # Run many times to catch the 2% error rate
        temperatures = [generate_temperature() for _ in range(200)]

        # Should have some error values (roughly 2%)
        error_count = temperatures.count(-999)
        # Allow range from 0 to 15 (roughly 2% of 200 = 4, with margin)
        assert 0 <= error_count <= 15

    def test_temperature_rounded_to_one_decimal(self):
        """Test that temperatures are rounded to 1 decimal place."""
        temperatures = [generate_temperature() for _ in range(50)]
        normal_temps = [t for t in temperatures if t != -999]

        # Check that all have at most 1 decimal place
        for temp in normal_temps:
            assert temp == round(temp, 1)


class TestGenerateHumidity:
    """Tests for humidity generation."""

    def test_humidity_in_normal_range(self):
        """Test that normal humidity falls within expected range."""
        humidities = [generate_humidity() for _ in range(100)]

        # Filter values that are in normal range (30-60)
        normal_humidity = [h for h in humidities if 30 <= h <= 60]

        # Most values should be in normal range
        assert len(normal_humidity) > 90
        assert all(30 <= h <= 60 for h in normal_humidity)

    def test_humidity_error_values_present(self):
        """Test that error values (out of range) occasionally appear."""
        humidities = [generate_humidity() for _ in range(200)]

        # Find out-of-range values (should be roughly 2%)
        out_of_range = [h for h in humidities if h < 0 or h > 100]

        # Allow range from 0 to 15 (roughly 2% of 200 = 4, with margin)
        assert 0 <= len(out_of_range) <= 15

    def test_humidity_error_range(self):
        """Test that error values fall in the error range (-100 to 200)."""
        # Generate many values to catch error cases
        humidities = [generate_humidity() for _ in range(500)]

        # All values should be either in normal range or error range
        for h in humidities:
            assert (-100 <= h <= 200)

    def test_humidity_rounded_to_one_decimal(self):
        """Test that humidity values are rounded to 1 decimal place."""
        humidities = [generate_humidity() for _ in range(50)]

        # Check that all have at most 1 decimal place
        for humidity in humidities:
            assert humidity == round(humidity, 1)


class TestCreateDataPayload:
    """Tests for data payload creation."""

    def test_payload_structure(self):
        """Test that payload contains all required fields."""
        data = create_data_payload("WS-01", 25.5, 45.0)

        assert "stationId" in data
        assert "temperature" in data
        assert "humidity" in data
        assert "timestamp" in data

    def test_payload_values(self):
        """Test that payload values match input parameters."""
        station_id = "WS-TEST"
        temperature = 22.3
        humidity = 55.7

        data = create_data_payload(station_id, temperature, humidity)

        assert data["stationId"] == station_id
        assert data["temperature"] == temperature
        assert data["humidity"] == humidity

    def test_payload_timestamp_format(self):
        """Test that timestamp is in ISO 8601 format."""
        data = create_data_payload("WS-01", 20.0, 50.0)

        timestamp = data["timestamp"]

        # Check ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ
        assert "T" in timestamp
        assert timestamp.endswith("Z")
        assert len(timestamp) == 20  # Format: 2024-01-15T12:34:56Z

    def test_payload_with_error_values(self):
        """Test that payload works with error sentinel values."""
        data = create_data_payload("WS-02", -999, 150.0)

        assert data["temperature"] == -999
        assert data["humidity"] == 150.0


class TestGetConfig:
    """Tests for configuration retrieval."""

    def test_config_defaults(self):
        """Test default configuration values."""
        # Clear environment variables
        with patch.dict(os.environ, {}, clear=True):
            config = get_config()

            assert config["station_id"] == "WS-XX"
            assert config["interval"] == 5
            assert config["broker"] == "mosquitto"
            assert config["port"] == 1883
            assert config["topic"] == "weather"

    def test_config_from_environment(self):
        """Test configuration from environment variables."""
        with patch.dict(
            os.environ, {"STATION_ID": "WS-TEST", "INTERVAL": "10"}, clear=True
        ):
            config = get_config()

            assert config["station_id"] == "WS-TEST"
            assert config["interval"] == 10

    def test_config_station_id_override(self):
        """Test that STATION_ID environment variable overrides default."""
        with patch.dict(os.environ, {"STATION_ID": "WS-99"}, clear=True):
            config = get_config()
            assert config["station_id"] == "WS-99"

    def test_config_interval_override(self):
        """Test that INTERVAL environment variable overrides default."""
        with patch.dict(os.environ, {"INTERVAL": "15"}, clear=True):
            config = get_config()
            assert config["interval"] == 15

    def test_config_interval_type(self):
        """Test that interval is returned as integer."""
        config = get_config()
        assert isinstance(config["interval"], int)
