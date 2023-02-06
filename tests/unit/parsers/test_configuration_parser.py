from subenum.core.parsers.configuration import ConfigurationParser


class TestConfigurationParser:
    def test_parse_config(self, config_file):
        config = ConfigurationParser()
        config.parse(file_path=config_file)
        assert (
            config.parser["API_KEYS"]["virustotal"] == "Test-VirusTotal-API-Key-12345"
        )

    def test_parse_invalid_config(self):
        config = ConfigurationParser()
        config.parse(file_path=None)
        assert config.enumerators == set()

    def test_parse_invalid_provider(self, config_file):
        """This test should pass regardless of the addition of any unknown
        providers to the INI file"""
        config = ConfigurationParser()
        config.parse(file_path=config_file)
        config.parser["API_KEYS"]["unknown_provider"] = "Some-API-Key"
        assert config.enumerators
