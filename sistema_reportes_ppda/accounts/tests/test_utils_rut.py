from django.test import TestCase
from accounts.utils import format_rut, validate_rut


class ValidateRUTTestCase(TestCase):
    def test_valid_ruts(self):
        """Test valid Chilean RUTs."""
        valid_ruts = [
            "11.603.215-5",  # With dots and dash
            "11603215-5",    # Without dots
            "116032155",     # Without dash
            "17.164.237-K",   # With uppercase K
            "17164237-K",     # Without dots, uppercase K
            "17164237k",      # Lowercase k
            "1234567-4"  # 7 digit RUT
        ]

        for rut in valid_ruts:
            with self.subTest(rut=rut):
                self.assertTrue(validate_rut(rut), f"Expected {rut} to be valid")

    def test_invalid_ruts(self):
        """Test invalid Chilean RUTs."""
        invalid_ruts = [
            "12.345.678-0",  # Incorrect DV
            "12345678-K",    # Incorrect DV
            "12345678",      # Missing DV
            "1234567",       # Too short
            "1234567890",    # Too long
            "abcdefghi",     # Letters instead of numbers
            "!@#$.567-K",    # Special characters
            "",              # Empty string
            None,            # NoneType
        ]

        for rut in invalid_ruts:
            with self.subTest(rut=rut):
                self.assertFalse(validate_rut(rut), f"Expected {rut} to be invalid")


class FormatRUTTestCase(TestCase):
    def test_format_rut(self):
        """Test RUT formatting to 'XXXXXXXX-X' format."""
        test_cases = [
            ("12.345.678-9", "12345678-9"),
            ("12345678-9", "12345678-9"),
            ("12.345.6789", "12345678-9"),
            ("123456789", "12345678-9"),
            ("1.234.567-k", "1234567-K"),
            (".1.234..567-k.", "1234567-K"),
            ("", ""),  # Edge case: empty string
            ("k", "K"),  # Edge case: single letter
        ]

        for raw_rut, expected_rut in test_cases:
            with self.subTest(raw_rut=raw_rut):
                self.assertEqual(format_rut(raw_rut), expected_rut)