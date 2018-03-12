import lxml
import pytest

from recruiting.management.commands.parse_trainee import Command
from recruiting.models import Vacancy

command = Command()
command.JOBS_QUANTITY = 1


def test_get_html_tree():
    html_tree = command.get_html_tree('/traineestellen')
    print(type(html_tree))
    assert isinstance(html_tree, lxml.html.HtmlElement)


def test_get_first_job_links():
    global first_job_links
    first_job_links = command.get_first_job_links()
    assert len(first_job_links) == command.JOBS_QUANTITY
    assert isinstance(first_job_links[0], lxml.etree._ElementUnicodeResult)


def test_parse_job_page():
    global page_context
    page_context = next(command.parse_job_page())
    assert isinstance(page_context['title'], str)
    assert '\n' not in page_context['title']
    assert isinstance(page_context['location'], str)
    assert '___' not in page_context['location']
    assert '\n' not in page_context['location']
    assert isinstance(page_context['starts_at'], str)
    assert '___' not in page_context['starts_at']
    assert '\n' not in page_context['starts_at']
    assert isinstance(page_context['ends_at'], str)
    assert '___' not in page_context['ends_at']
    assert '\n' not in page_context['ends_at']
    assert isinstance(page_context['description'], str)
    assert isinstance(page_context['image_list'], list)
    assert isinstance(page_context['company'], str)
    assert '\n' not in page_context['company']


def test_parse_description():
    html_tree = command.get_html_tree(first_job_links[0])
    description = html_tree.xpath('//div[contains (@class, "tr-text+")]')
    str_description = command.parse_description(description)
    assert '\n' not in str_description
    assert '<p>' not in str_description


@pytest.mark.django_db(transaction=False)
def test_get_or_write_to_db():
    active_vacancy = command.get_or_write_to_db(page_context)
    assert isinstance(active_vacancy, Vacancy)
