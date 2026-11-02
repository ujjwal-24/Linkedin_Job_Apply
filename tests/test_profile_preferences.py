"""Location exclusions and unanswered CV fields must survive the application flow."""
import sys
import types
from types import SimpleNamespace

import pytest
from selenium.common.exceptions import NoSuchElementException

from modules.profile_rules import excluded_location, numeric_answers


@pytest.mark.parametrize('location,expected', [
    ('Chennai, Tamil Nadu, India (Hybrid)', 'Chennai'),
    ('CHENNAI Metropolitan Area', 'Chennai'),
    ('Madras, India', 'Madras'),
    ('Chennai / Bengaluru', 'Chennai'),
    ('Noida, Uttar Pradesh, India', None),
    ('Remote, India', None),
    ('Chennaipalli, India', None),
])
def test_city_exclusions(location, expected):
    assert excluded_location(location, ['Chennai', 'Madras']) == expected


def test_missing_numeric_answers_stay_unanswered():
    assert numeric_answers(None, salary=True) == ('', '', '')
    assert numeric_answers(None) == ('', '', '')
    assert numeric_answers(0) == ('0', '0', '0')
    assert numeric_answers(1200000, salary=True) == ('1200000', '100000.0', '12.0')
    assert numeric_answers(60) == ('60', '2', '8')


@pytest.mark.parametrize('value', [None, ''])
def test_blank_salary_is_saved_as_null(client, monkeypatch, tmp_path, value):
    import app
    from config import _overrides
    path = str(tmp_path / 'user_config.json')
    monkeypatch.setattr(app, 'USER_CONFIG_PATH', path)
    monkeypatch.setattr(_overrides, 'USER_CONFIG_PATH', path)
    response = client.post('/api/config', json={'questions': {
        'current_ctc': value, 'desired_salary': value, 'notice_period': value,
    }})
    assert response.status_code == 200
    assert response.get_json()['questions'] == {
        'current_ctc': None, 'desired_salary': None, 'notice_period': None,
    }


@pytest.mark.parametrize('location', ['Chennai, Tamil Nadu, India (Remote)', 'Unknown'])
def test_excluded_or_unknown_card_never_opens_application(monkeypatch, location):
    fake_chrome = types.ModuleType('modules.open_chrome')
    fake_chrome.options = fake_chrome.driver = fake_chrome.actions = fake_chrome.wait = None
    monkeypatch.setitem(sys.modules, 'modules.open_chrome', fake_chrome)
    import runAiBot as bot
    clicks = []
    link = SimpleNamespace(text='Performance Test Engineer',
        get_dom_attribute=lambda _: 'Performance Test Engineer',
        click=lambda: clicks.append(True))

    class Card:
        def get_dom_attribute(self, name):
            return 'job-1'

        def find_element(self, by, query):
            if 'lockup__title' in query:
                return link
            if 'lockup__subtitle' in query:
                return SimpleNamespace(text='Example employer')
            raise NoSuchElementException(query)

    monkeypatch.setattr(bot, 'excluded_locations', ['Chennai', 'Madras'])
    monkeypatch.setattr(bot, 'scroll_to_view', lambda *args: None)
    monkeypatch.setattr(bot, 'try_xp', lambda *args: SimpleNamespace(text=location))
    result = bot.get_job_main_details(Card(), set(), set())
    assert result[-1] is True
    assert clicks == []
