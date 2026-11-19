from django.test import TestCase
from django.urls import reverse

from .models import Category, Tag

class ProductsViewTests(TestCase):
    fixtures = ['sample_data.json']
    products_url = reverse("products")

    def get_products(self, query="", category="", tags=()):
        params = {"query": query}
        if category:
            params["category"] = Category.objects.get(name=category).pk
        if tags:
            params["tags"] = [Tag.objects.get(name=t).pk for t in tags]

        response = self.client.get(self.products_url, params)
        return response.context["products"]

    def test_no_search_or_filters_returns_all_products(self):
        products = self.get_products()
        self.assertEqual(len(products), 20)

    def test_search_with_no_matches_returns_no_products(self):
        products = self.get_products(query="xyz")
        self.assertEqual(len(products), 0)

    def test_search_and_filter_with_matches_returns_matching_products(self):
        cases = [
            # search only: matches on description, case-insensitively
            (
                "breaker",
                "",
                [],
                {
                    "15A Single-Pole Breaker",
                    "20A GFCI Breaker",
                    "20A Single-Pole Breaker",
                    "30A Double-Pole Breaker",
                }
            ),
            # search only: matches across two categories (breakers and receptacles)
            (
                "20A",
                "",
                [],
                {
                    "20A Commercial-Grade Duplex Outlet",
                    "20A GFCI Breaker",
                    "20A GFCI Outlet, Weather-Resistant",
                    "20A Single-Pole Breaker",
                }
            ),
            # search + category: category narrows search results
            (
                "20A",
                "Breakers",
                [],
                {
                    "20A GFCI Breaker",
                    "20A Single-Pole Breaker",
                }
            ),
            # the following three cases show:
            # search + multiple tags: product must have ALL selected tags
            (
                "LED",
                "",
                ["Outdoor Rated"],
                {"LED Wall Pack, Dusk-to-Dawn"}
            ),
            (
                "LED",
                "",
                ["Commercial"],
                {
                    "4ft LED Strip Fixture",
                    "LED Wall Pack, Dusk-to-Dawn",
                }
            ),
            (
                "LED",
                "",
                ["Outdoor Rated", "Commercial"],
                {"LED Wall Pack, Dusk-to-Dawn"}
            ),
        ]
        for query, category, tags, expected in cases:
            with self.subTest(query=query, category=category, tags=tags):
                products = self.get_products(query, category, tags)
                actual = {p.description for p in products}
                self.assertEqual(actual, expected)

    def test_invalid_category_id_returns_all_products(self):
        # No search or filter is applied in this case
        response = self.client.get(self.products_url, {"category": 9999})
        products = response.context["products"]
        self.assertEqual(len(products), 20)

    def test_invalid_tag_id_returns_all_products(self):
        # No search or filter is applied in this case
        response = self.client.get(self.products_url, {"tags": [9999]})
        products = response.context["products"]
        self.assertEqual(len(products), 20)

    def test_products_view_avoids_n_plus_one_queries(self):
        # 1 for category choices in form
        # 1 for tag choices in form
        # 1 for products and categories (joined via select_related)
        # 1 for tags (prefetch)
        with self.assertNumQueries(4):
            self.get_products()
