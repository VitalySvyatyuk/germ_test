import requests
from lxml import html
from bs4 import BeautifulSoup

import logging
from django.core.management.base import BaseCommand
from recruiting.models import Vacancy, Company, City

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    BASE_URL = 'https://www.trainee.de'
    HEADERS = {'User-Agent': 'Mozilla/5.0'}
    JOBS_QUANTITY = 20
    active_vacancies = []

    def handle(self, *args, **options):
        for job_ctx in self.parse_job_page():
            active_vacancy = self.get_or_write_to_db(job_ctx)
            print(active_vacancy)
            self.active_vacancies.append(active_vacancy)

        for vacancy in Vacancy.objects.filter(is_active=True):
            if vacancy not in self.active_vacancies:
                vacancy.is_active = False
                vacancy.save()
        logger.debug("Outdated vacancies are inactive now")

    def parse_job_page(self):
        for path in self.get_first_job_links():
            html_tree = self.get_html_tree(path)
            ctx = dict()
            ctx['title'] = html_tree.xpath('//h2[@class="tr-mrgv+ tr-md-mrgv++++"]/text()')[0]
            ctx['location'] = html_tree.xpath('//ul[@class="tr-list"]/li[1]/text()')[6][1:]\
                .replace('\n                        ', '')
            ctx['starts_at'] = html_tree.xpath('//ul[@class="tr-list"]/li[2]/text()')[6][1:]\
                .replace('\n                        ', '')
            ctx['ends_at'] = html_tree.xpath('//ul[@class="tr-list"]/li[3]/text()')[6][1:]\
                .replace('\n                        ', '')
            description = html_tree.xpath('//div[contains (@class, "tr-text+")]')
            ctx['description'] = self.parse_description(description)
            try:
                ctx['image_list'] = [html_tree.xpath('//img[@class="tr-stage__logo"]/@src')[0]]
            except IndexError:
                ctx['image_list'] = ""
            ctx['company'] = html_tree.xpath('//h1/text()')[0]
            yield ctx

    @staticmethod
    def get_or_write_to_db(job_ctx):
        location, created = City.objects.get_or_create(
            location=job_ctx['location'])
        company, created = Company.objects.get_or_create(
            name=job_ctx['company'],
            location=location)
        active_vacancy, created = Vacancy.objects.get_or_create(
            title=job_ctx['title'],
            starts_at=job_ctx['starts_at'],
            ends_at=job_ctx['ends_at'],
            description=job_ctx['description'],
            image_list=job_ctx['image_list'],
            company=company,
            location=location)
        return active_vacancy

    def get_html_tree(self, path):
        response = requests.get(self.BASE_URL + path, headers=self.HEADERS)
        return html.fromstring(response.content)

    def get_first_job_links(self):
        html_tree = self.get_html_tree('/traineestellen')
        return html_tree.xpath('//a[@class="tr-card tr-card--link"]/@href')[:self.JOBS_QUANTITY]

    @staticmethod
    def parse_description(html_description):
        html_string = html.tostring(html_description[0])
        soup = BeautifulSoup(html_string, "lxml")
        text_data = soup.findAll(text=True)
        filtered_text_data = list(filter(lambda x: x != '\n', text_data))
        return ' '.join(filtered_text_data)
