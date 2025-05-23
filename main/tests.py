from django.test import TestCase
from django.urls import reverse
from .models import ModelCV

class CVViewsTestCase(TestCase):
    def setUp(self):
        self.cv = ModelCV.objects.create(
            firstname="Brad",
            lastname="Pitt",
            bio="Award-winning actor and producer known for his versatile roles.",
            skills=["Acting", "Production", "Public Speaking"],
            projects=[
                {
                    "name": "Fight Club",
                    "description": "Cult classic.",
                    "link": "https://example.com/fight-club"
                }
            ],
            contacts={
                "email": "brad@example.com",
                "twitter": "@brad"
            }
        )

    def test_cv_list_view(self):
        response = self.client.get(reverse("template_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Brad Pitt")

    def test_cv_detail_view(self):
        response = self.client.get(reverse("template_detail", kwargs={"pk": self.cv.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fight Club")
