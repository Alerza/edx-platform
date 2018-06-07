""" Tests for journals marketing views. """

import mock

from django.conf import settings
from django.core.urlresolvers import reverse

from openedx.core.djangolib.testing.utils import CacheIsolationTestCase
from openedx.core.djangoapps.site_configuration.tests.mixins import SiteMixin


def get_mocked_journal_data():
    return {
        "uuid": "1918b738-979f-42cb-bde0-13335366fa86",
        "title": "dummy-title",
        "partner": "edx",
        "journals": [
            {
                "title": "dummy-title",
                "sku": "ASZ1GZ",
                "card_image_url": "dummy-url",
                "slug": "dummy-title",
                "access_length": "8 weeks",
                "short_description": "dummy short description"
            }
        ],
        "courses": [
            {
                "short_description": "dummy short description",
                "course_runs": [
                    {
                        "key": "course-v1:ABC+ABC101+2015_T1",
                        "title": "Matt edX test course",
                        "start": "2015-01-08T00:00:00Z",
                        "end": "2016-12-30T00:00:00Z",
                        "image": {
                            "src": "dummy/url"
                        },
                        "seats": [
                            {
                                "type": "verified",
                                "sku": "unit03",
                                "bulk_sku": "2DF467D"
                            }
                        ]
                    }
                ]
            }
        ],
        "applicable_seat_types": ["credit", "honor", "verified"]
    }


def get_mocked_pricing_data():
    return {
        "currency": "USD",
        "discount_value": 0.3,
        "is_discounted": False,
        "total_incl_tax": 23.01,
        "purchase_url": "dummy-url",
        "total_incl_tax_excl_discounts": 40
    }


class JournalMarketingViewTest(CacheIsolationTestCase, SiteMixin):
    """ Tests for the student account views that update the user's account information. """

    def setUp(self):
        super(JournalMarketingViewTest, self).setUp()
        self.path = reverse(
            "openedx.journals.bundle_about",
            kwargs={'bundle_uuid': "4837728d-6dab-458b-9e3f-3e799cfdc31c"}
        )


    # @mock.patch.dict(settings.FEATURES, {"ENABLE_JOURNAL_INTEGRATION": True})
    # @mock.patch('openedx.features.journals.api.get_journal_bundles')
    # def test_with_empty_data(self, mock_journal_bundles):
    #     mock_journal_bundles.return_value = []
    #     response = self.client.get(path=reverse(
    #         "openedx.journals.bundle_about",
    #         kwargs={'bundle_uuid': "4837728d-6dab-458b-9e3f-3e799cfdc31c"}
    #     ))
    #     self.assertEqual(response.status_code, 404)

    @mock.patch.dict(settings.FEATURES, {"ENABLE_JOURNAL_INTEGRATION": True})
    @mock.patch('openedx.features.journals.api.DiscoveryApiClient.get_journal_bundles')
    def test_with_empthy_data(self, mock_bundles):
        mock_bundles.return_value = []
        response = self.client.get(path=self.path)
        self.assertEqual(response.status_code, 404)

    @mock.patch.dict(settings.FEATURES, {"ENABLE_JOURNAL_INTEGRATION": True})
    @mock.patch('openedx.features.journals.views.marketing.get_pricing_data')
    @mock.patch('openedx.features.journals.api.DiscoveryApiClient.get_journal_bundles')
    def test_with_empthy_data(self, mock_bundles, mock_pricing_data):
        mock_pricing_data.return_value = get_mocked_pricing_data()
        mock_bundles.return_value = get_mocked_journal_data()
        response = self.client.get(path=self.path)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Purchase the Bundle")


