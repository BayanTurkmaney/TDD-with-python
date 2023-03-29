"""
Test Cases for Mocking Lab
"""
import json
from unittest import TestCase
from unittest.mock import patch, Mock
from requests import Response
from models import IMDb

IMDB_DATA = {}

class TestIMDbDatabase(TestCase):
    """Tests Cases for IMDb Database"""

    @classmethod
    def setUpClass(cls):
        """ Load imdb responses needed by tests """
        global IMDB_DATA
        with open('tests/fixtures/imdb_responses.json') as json_data:
            IMDB_DATA = json.load(json_data)
    
    #Notice this code instantiates an IMDb object initializing it with an API key. Then the code calls imdb.search_titles() for the movie “Bambi” and asserts that the results are not None. It also checks that the error message is empty and that the id returned is tt1375666.
    #You want to patch the search_titles() method of the IMDb class (i.e., IBDb.search_titles()) so that it is not called at all. For this, you will use the @patch() decorator and patch the return_value to return the GOOD_SEARCH test fixture data.
    #Notice that this is patching test_imdb.IMDb.search_titles. The name of your test module is test_imdb and so you should patch the IMDb class that you imported, not the one in the models package. This concept is important to understand. You always want to patch the function that is within the namespace that you are testing. This is why you need to fully qualify IMDb.search_titles as test_imdb.IMDb.search_titles.
    @patch('test_imdb.IMDb.search_titles')
    def test_search_by_title(self, imdb_mock):
        """Test searching by title"""
        imdb_mock.return_value = IMDB_DATA["GOOD_SEARCH"]
        imdb = IMDb("k_12345678")
        results = imdb.search_titles("Bambi")
        self.assertIsNotNone(results)
        self.assertIsNone(results["errorMessage"])
        self.assertIsNotNone(results["results"])
        self.assertEqual(results["results"][0]["id"], "tt1375666")

    
    @patch('models.imdb.requests.get')
    def test_search_with_no_results(self, imdb_mock):
        """Test searching with no results"""
        imdb_mock.return_value = Mock(status_code=404)
        imdb = IMDb("k_12345678")
        results = imdb.search_titles("Bambi")
        self.assertEqual(results, {})


    @patch('models.imdb.requests.get')
    def test_search_by_title_failed(self, imdb_mock):
        """Test searching by title failed"""
        imdb_mock.return_value = Mock(
            spec=Response,
            status_code=200,
            json=Mock(return_value=IMDB_DATA["INVALID_API"])
        )
        imdb = IMDb("bad-key")
        results = imdb.search_titles("Bambi")
        self.assertIsNotNone(results)
        self.assertEqual(results["errorMessage"], "Invalid API Key")

    
    @patch('models.imdb.requests.get')
    def test_movie_ratings(self, imdb_mock):
        """Test movie Ratings"""
        imdb_mock.return_value = Mock(
            spec=Response,
            status_code=200,
            json=Mock(return_value=IMDB_DATA["GOOD_RATING"])
        )
        imdb = IMDb("k_12345678")
        results = imdb.movie_ratings("tt1375666")
        self.assertIsNotNone(results)
        self.assertEqual(results["title"], "Bambi")
        self.assertEqual(results["filmAffinity"], 3)
        self.assertEqual(results["rottenTomatoes"], 5)


    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

