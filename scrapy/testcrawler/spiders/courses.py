"""This file defines the scrapy CrawlSpider that gets the courses from U of T's Academic Calendar website.
The enclosing folder and its encolsing folder were generated with scrapy, and this was the only file made
by us (and thus is the only file that we addded our own documentation for).

To scrape and save to courses.json, run the command on the following line from the 'testcrawler' folder:
scrapy crawl coursecrawler -o courses.json
"""
import re
from typing import Union, Optional
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Response


class CourseCrawler(CrawlSpider):
    """A subclass that defines the spider we will use to scrape the courses from U of T's Academic
    Calendar website.

    Instance Attribute:
    - name: a string of the name of this CrawlSpider
    - allowed_domains: a list of strings of the allowed domains this CrawlSpider can scrape from
    - start_urls: a list of strings of the urls to start crawling on
    - rules: a tuple of the scrapy Rules this CrawlSpider has to follow to scrape
    """
    name: str = 'coursecrawler'
    allowed_domains: list[str] = ['artsci.calendar.utoronto.ca']
    start_urls: list[str] = []
    start_urls.extend(['https://artsci.calendar.utoronto.ca/search-courses?page=' + str(i) for i in range(0, 168)])
    start_urls.extend(['https://artsci.calendar.utoronto.ca/search-programs?page=' + str(i) for i in range(0, 13)])

    rules: tuple[Rule] = (
        Rule(LinkExtractor(allow=r'course\/\w{3,4}\d{3}\w\d'), callback='parse'),
    )

    def parse(self, response: Response, **kwargs) -> dict[str, Optional[Union[str, list[str]]]]:
        """Method to parse through the pages from the extracted links.
        The returned dictionary is added to the list in the output json (specified
        in the command you need to run, which can be found at the top of this file).
        """
        name = response.css('.block-page-title-block h1::text').get()
        breadth = response.css('.field--name-field-breadth-requirements div.field__item::text').get()
        exclusions = response.css('.field--name-field-exclusion div.field__item a::text').extract()

        unclean_prereqs = response.css('.field--name-field-prerequisite div.field__item *::text').extract()
        prerequisites = self._clean_prerequisites(unclean_prereqs)

        return {
            'name': name,
            'breadth': breadth,
            'prerequisites': prerequisites,
            'exclusions': exclusions
        }

    def _clean_prerequisites(self, prerequisites: list[str]) -> list[str]:
        """Helper method to clean"""
        prerequisites_so_far = []

        for prerequisite in prerequisites:
            if re.match(r'\w{3,4}\d{3}\w\d', prerequisite):
                prerequisites_so_far.append(prerequisite)
            else:
                if '/' in prerequisite and prerequisites_so_far != [] and \
                        re.match(r'\w{3,4}\d{3}\w\d', prerequisites[-1]):
                    prerequisites_so_far.append('/')
        if prerequisites_so_far != [] and prerequisites_so_far[-1] == '/':
            prerequisites_so_far.pop(-1)

        return prerequisites_so_far


if __name__ == '__main__':
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['scrapy.spiders', 'scrapy.linkextractors', 'scrapy.http', 're']
    })
