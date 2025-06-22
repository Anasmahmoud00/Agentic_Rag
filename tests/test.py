import os
import sys
import unittest

# --- Path Correction ---
# This ensures that the test script can find and import modules from the parent project (e.g., 'core', 'tools').
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

# Now, import the function you want to test
from core.services.classification import classify_query_intent

class TestClassificationService(unittest.TestCase):
    """
    Test suite for the query classification service.
    """

    def test_single_intent_restaurant(self):
        """Test that a query about food correctly classifies as 'restaurant'."""
        query = "where can I find some good italian food in Rome?"
        expected_intent = "restaurant"
        actual_intent = classify_query_intent(query)
        self.assertEqual(actual_intent, expected_intent)

    def test_single_intent_activity(self):
        """Test that a query about things to do correctly classifies as 'activity'."""
        query = "what are some fun things to do in Tokyo?"
        expected_intent = "activity"
        actual_intent = classify_query_intent(query)
        self.assertEqual(actual_intent, expected_intent)
        
    def test_single_intent_accommodation(self):
        """Test that a query about hotels correctly classifies as 'accommodation'."""
        query = "I need a cheap hotel near the Eiffel Tower"
        expected_intent = "accommodation"
        actual_intent = classify_query_intent(query)
        self.assertEqual(actual_intent, expected_intent)

    def test_multiple_intents(self):
        """Test a query that should return multiple intents."""
        # Note: This depends on the classifier LLM's ability to return comma-separated values.
        query = "find me a cheap hotel and some restaurants in London"
        expected_intents = ["accommodation", "restaurant"]
        actual_intents = classify_query_intent(query)
        # The order might vary, so we check if the sets are equal
        self.assertCountEqual(actual_intents, expected_intents)

    def test_unknown_intent(self):
        """Test that a nonsensical query returns 'unknown'."""
        query = "what is the color of the sky on mars?"
        expected_intent = "unknown"
        actual_intent = classify_query_intent(query)
        self.assertEqual(actual_intent, expected_intent)

# This allows you to run the tests directly from the command line
if __name__ == '__main__':
    unittest.main()