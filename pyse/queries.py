r"""
The ``queries`` object defineds a mapping from semantic API endpoints to URL
endpoints, accessible either as attributes or as dictionary items. URL endpoints
may have format arguments in them.

Example::

    >>> import pyse
    >>> pyse.queries['questions']['ALL']
    'questions'
    >>> pyse.queries.answers.by_id.accept.CAST
    'answers/{id}/accept'

This object also has a `method()` method to lookup the HTTP request method for any
given endpoint.

Example::

    >>> import pyse
    >>> pyse.queries.method(pyse.queries.questions.ALL)
    'GET'
    >>> pyse.queries.method(pyse.queries.answers.by_id.accept.UNDO)
    'POST'

Both upper- and lower-case versions of the names are allowed. For example,
``queries.questions.ALL`` and ``queries.questions.all`` both correspond to the
API URL endpoint 'questions'.
"""

from .structures import URLTree

_queries = {
    "GET": {
        "access_tokens": {
            "inspect": "access-tokens/{access_tokens}",
        },
        "answers": {
            "all": "answers",
            "by_id": {
                "all": "answers/{ids}",
                "comments": "answers/{id}/comments",
                "flags": {
                    "options": "answers/{id}/flags/options",
                },
                "questions": "answers/{ids}/questions",
            }
        },
        "badges": {
            "all": "badges",
            "by_id": {
                "all": "badges/{ids}",
                "recipients": "badges/{ids}/recipients"
            },
            "name": "badges/name",
            "recipients": "badges/recipients",
            "tags": "badges/tags"
        },
        "comments": {
            "all": "comments",
            "by_id": {
                "all": "comments/{ids}",
                "flags": {
                    "options": "comments/{id}/flags/options",
                },
            },
        },
        "errors": {
            "all": "errors",
            "by_id": "errors/{id}"
        },
        "events": "events",
        "filters": {
            "create": "filters/create",
            "decode": "filters/{filter}"
        },
        "inbox": {
            "all": "inbox",
            "unread": "inbox/unread"
        },
        "notifications": {
            "all": "notifications",
            "unread": "notifications/unread"
        },
        "posts": {
            "all": "posts",
            "by_id": {
                "all": "posts/{ids}",
                "comments": {
                    "all": "posts/{ids}/comments",
                },
                "revisions": "posts/{ids}/revisions",
                "suggested_edits": "posts/{ids}/suggested_edits"
            }
        },
        "privileges": "privileges",
        "revisions": "revisions/{ids}",
        "search": {
            "all": "search",
            "advanced": "search/advanced",
            "similar": "similar",
            "excerpts": "search/excerpts"
        },
        "sites": "sites",
        "suggested_edits": {
            "all": "suggested-edits",
            "by_id": "suggested-edits/{ids}"
        },
        "tags": {
            "all": "tags",
            "by_tag": {
                "info": "tags/{tags}/info",
                "faq": "tags/{tags}/faq",
                "related": "tags/{tags}/related",
                "synonyms": "tags/{tags}/synonyms",
                "top_answerers": {
                    "all_time": "tags/{tags}/top-answerers/all_time",
                    "month": "tags/{tags}/top-answerers/month",
                },
                "wikis": "tags/{tags}/wikis"
            },
            "moderator_only": "tags/moderator-only",
            "required": "tags/required",
            "synonyms": "tags/synonyms",
        },
        "users": {
            "all": "users",
            "by_id": {
                "all": "users/{ids}",
                "associated": "users/{ids}",
                "badges": "users/{ids}/badges",
                "comments": {
                    "all": "users/{ids}/comments",
                    "to_id": "user/{ids}/comments/{to_id}"
                },
                "favorites": "users/{ids}/mentioned",
                "inbox": {
                    "all": "users/{ids}/inbox",
                    "unread": "users/{ids}/inbox/unread"
                },
                "merges": "users/{id}/merges",
                "network_activity": "users/{id}/network-activity",
                "notifications": {
                    "all": "users/{id}/notifications",
                    "unread": "users/{id}/notifications/unread"
                },
                "posts": "users/{ids}/posts",
                "privileges": "users/{id}/privileges",
                "questions": {
                    "all":  "users/{ids}/questions",
                    "featured": "users/{ids}/questions/featured",
                    "no_answers": "users/{ids}/questions/no-answers",
                    "unaccepted": "users/{ids}/questions/unaccepted",
                    "unanswered": "users/{ids}/questions/unanswered",
                },
                "reputation": {
                    "recent": "users/{ids}/reputation",
                    "history": {
                        "public": "users/{id}/reputation-history",
                        "full": "users/{id}/reputation-history/full"
                    }
                },
                "suggested_edits": "users/{ids}/suggested-edits",
                "tags": {
                    "all": "users/{id}/tags",
                    "by_tag": {
                        "top_answers": "users/{id}/tags/{tags}/top-answers",
                        "top_questions": "users/{id}/tags/{tags}/top-questions",
                    },
                    "top_tags": {
                        "all": "user/{id}/top-tags",
                        "answers": "user/{id}/top-answer-tags",
                        "questions": "user/{id}/top-answer-tags"
                    }
                },
                "timeline": "user/{id}s/timeline",
                "write_permissions": "users/{id}/write-permissions",
            },
            "me": {
                "all": "me",
                "associated": "me",
                "badges": "me/badges",
                "comments": {
                    "all": "me/comments",
                    "to_id": "user/{ids}/comments/{to_id}"
                },
                "favorites": "me/mentioned",
                "inbox": {
                    "all": "me/inbox",
                    "unread": "me/inbox/unread"
                },
                "merges": "me/merges",
                "network_activity": "me/network-activity",
                "notifications": {
                    "all": "me/notifications",
                    "unread": "me/notifications/unread"
                },
                "posts": "me/posts",
                "privileges": "me/privileges",
                "questions": {
                    "all":  "me/questions",
                    "featured": "me/questions/featured",
                    "no_answers": "me/questions/no-answers",
                    "unaccepted": "me/questions/unaccepted",
                    "unanswered": "me/questions/unanswered",
                },
                "reputation": {
                    "recent": "me/reputation",
                    "history": {
                        "public": "me/reputation-history",
                        "full": "me/reputation-history/full"
                    }
                },
                "suggested_edits": "me/suggested-edits",
                "tags": {
                    "all": "me/tags",
                    "by_tag": {
                        "top_answers": "me/tags/{tags}/top-answers",
                        "top_questions": "me/tags/{tags}/top-questions",
                    },
                    "top_tags": {
                        "all": "user/{id}/top-tags",
                        "answers": "user/{id}/top-answer-tags",
                        "questions": "user/{id}/top-answer-tags"
                    }
                },
                "timeline": "user/{ids}/timeline",
                "write_permissions": "me/write-permissions",
            },
            "moderators": {
                "all": "users/moderators",
                "elected": "users/moderators/elected"
            }
        },
        "questions": {
            "all": "questions",
            "by_id": {
                "all": "questions/{ids}",
                "answers": {
                    "all": "questions/{ids}/answers",
                },
                "comments": "questions/{ids}/comments",
                "flags": {
                    "options": "questions/{id}/flags/options"
                },
                "linked": "questions/{id}/linked",
                "related": "questions/{id}/related",
                "timeline": "questions/{id}/timeline",
            },
            "featured": "questions/featured",
            "no_answers": "questions/no-answers",
            "unanswered": {
                "all": "questions/unanswered",
                "my_tags": "questions/unanswered/my-tags"
            }
        }
    },
    "POST": {
        "access_tokens": {
            "invalidate": "access-tokens/{access_tokens}/invalidate",
            "de_auth": "apps/{access_tokens}/de-authenticate"
        },
        "answers": {
            "by_id": {
                "accept": {
                    "cast": "answers/{id}/accept",
                    "undo": "answers/{id}/accept/undo"
                },
                "delete": "answers/{id}/delete",
                "downvote": {
                    "cast": "answers/{id}/downvote",
                    "undo": "answers/{id}/downvote/undo"
                },
                "edit": "answers/{id}/edit",
                "flags": {
                    "add": "answers/{id}/flags/add"
                },
                "upvote": {
                    "cast": "answers/{id}/upvote",
                    "undo": "answers/{id}/upvote/undo"
                }
            }
        },
        "comments": {
            "by_id": {
                "delete": "comments/{id}/delete",
                "edit": "comments/{id}/delete",
                "flags": {
                    "add": "comments/{id}/flags/add"
                },
                "upvote": {
                    "cast": "comments/{id}/upvote",
                    "undo": "comments/{id}/upvote/undo"
                }
            },
        },
        "posts": {
            "by_id": {
                "comments": {
                    "add": "posts/{id}/comments/add",
                    "render": "posts/{id}/comments/render",
                },
            }
        },
        "questions": {
            "by_id": {
                "answers": {
                    "add": "questions/{ids}/answers/add",
                    "render": "questions/{ids}/answers/render"
                },
                "close": "questions/{id}/close/options",
                "delete": "questions/{id}/delete",
                "downvote": {
                    "cast": "questions/{id}/downvote",
                    "undo": "questions/{id}/downvote/undo"
                },
                "edit": "questions/{id}/edit",
                "favorite": {
                    "cast": "questions/{id}/favorite",
                    "undo": "questions/{id}/favorite/undo"
                },
                "flags": {
                    "cast": "questions/{id}/flags/add",
                },
                "upvote": {
                    "cast": "questions/{id}/upvote",
                    "undo": "questions/{id}/upvote/undo"
                },
            },
            "add": "questions/add",
            "render": "questions/render",
        }
    }
}


"""
A dictionary tree of URL endpoints for API query types.
"""
queries = URLTree(
    dictionaries = [(method, url_dict) for method, url_dict in _queries.items()],
    name = "queries"
)

