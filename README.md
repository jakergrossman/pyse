# pyse
A Python wrapper for the Stack Exchange API.

## Main Features
pyse has 2 core aspects:

  - The `pyse.queries` object. This is a lookup dictionary of API URL endpoints.
    For example, `pyse.queries.questions.ALL` maps to the `questions` API
    endpoint, and `pyse.queries.questions.upvote.CAST` maps to the
    `questions/{id}/upvote` API endpoint.

  - The `pyse.query()` method. This method takes a site (either a full domain
    name, like "stackoverflow.com", or one of the short forms identified by the
    `api_site_parameter` on the API `site` object), an API URL endpoint,
    and API parameters in the form of keyword arguments.
