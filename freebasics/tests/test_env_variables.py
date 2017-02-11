from django.test import TestCase, RequestFactory
from molo.core.tests.base import MoloTestCaseMixin
from freebasics.views import HomeView
from freebasics.templatetags import freebasics_tags


class EnvTestCase(TestCase, MoloTestCaseMixin):

    def setUp(self):
        self.mk_main()

    def test_block_ordering(self):
        with self.settings(BLOCK_POSITION_BANNER=4,
                           BLOCK_POSITION_LATEST=3,
                           BLOCK_POSITION_QUESTIONS=2,
                           BLOCK_POSITION_SECTIONS=1):
            factory = RequestFactory()
            request = factory.get('/')
            request.site = self.site
            home = HomeView()
            home.request = request
            context = home.get_context_data()
            self.assertEquals(context['blocks'][0], (
                'blocks/sections.html', 1))
            self.assertEquals(context['blocks'][1], (
                'blocks/questions.html', 2))
            self.assertEquals(context['blocks'][2], ('blocks/latest.html', 3))
            self.assertEquals(context['blocks'][3], ('blocks/banners.html', 4))

    def test_css_vars(self):
        with self.settings(CUSTOM_CSS_BLOCK_TEXT_TRANSFORM="lowercase",
                           CUSTOM_CSS_ACCENT_2="red"):
            styles = freebasics_tags.custom_css(context='')
            self.assertEquals(styles['accent_2'], 'red')
            self.assertEquals(styles['text_transform'], 'lowercase')

    def test_custom_css(self):
        response = self.client.get('/')
        self.assertContains(response, 'Free Basics Custom CSS')
        self.assertContains(response, '.base-bcolor')
        self.assertContains(response, '.heading')
        self.assertContains(response, '.article-list__item')
