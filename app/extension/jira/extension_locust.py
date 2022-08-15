import re
from locustio.common_utils import init_logger, jira_measure, run_as_specific_user, raise_if_login_failed  # noqa F401

logger = init_logger(app_type='jira')


@jira_measure("locust_app_specific_action_config")
@run_as_specific_user(username='admin', password='admin')  # run as specific user
def app_specific_action(locust):
    raise_if_login_failed(locust)
    r = locust.get('/rest/datarocks/1.0/configuration', catch_response=True)
    response_json = r.json()
    assert 'hideJiraSearchField' in response_json, "invalid response from combined-search config endpoint"


@jira_measure("locust_app_specific_action_jira_search")
# @run_as_specific_user(username='admin', password='admin')  # run as specific user
def app_specific_action(locust):
    raise_if_login_failed(locust)
    data = {
        'searchTerm': "AppIssue",
        'pagination': {
            'limit': 20,
            'offset': 0
        }
    }
    r = locust.post('/rest/datarocks/1.0/search/jira', catch_response=True, json=data)
    response_json = r.json()
    assert 'searchValid' in response_json, "invalid response from combined-search search/jira endpoint"
    assert response_json['searchValid'] is True, "invalid response from combined-search search/jira endpoint"
    assert 'resultList' in response_json, "invalid response from combined-search search/jira endpoint"
    assert len(response_json['resultList']) > 0, "invalid response from combined-search search/jira endpoint"
