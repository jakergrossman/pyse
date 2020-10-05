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
    "access_tokens": {
        "inspect": ("GET", "access-tokens/{access_tokens}"),
        "invalidate": ("POST", "access-tokens/{access_tokens}/invalidate"),
        "de_auth": ("POST", "apps/{access_tokens}/de-authenticate"),
    },
    "answers": {
        "accept": {
            "cast": ("POST", "answers/{id}/accept"),
            "undo": ("POST", "answers/{id}/accept/undo"),
        },
        "all": ("GET", "answers"),
        "by_id": {
            "all": ("GET", "answers/{ids}"),
            "comments": ("GET", "answers/{id}/comments"),
            "delete": ("POST", "answers/{id}/delete"),
            "downvote": {
                "cast": ("POST", "answers/{id}/downvote"),
                "undo": ("POST", "answers/{id}/downvote/undo"),
            },
            "edit": ("POST", "answers/{id}/edit"),
            "flags": {
                "add": ("POST", "answers/{id}/flags/add"),
                "options": ("GET", "answers/{id}/flags/options"),
            },
            "questions": ("GET", "answers/{ids}/questions"),
            "upvote": {
                "cast": ("POST", "answers/{id}/upvote"),
                "undo": ("POST", "answers/{id}/upvote/undo"),
            },
        },
    },
    "badges": {
        "all": ("GET", "badges"),
        "by_id": {
            "all": ("GET", "badges/{ids}"),
            "recipients": ("GET", "badges/{ids}/recipients"),
        },
        "name": ("GET", "badges/name"),
        "recipients": ("GET", "badges/recipients"),
        "tags": ("GET", "badges/tags"),
    },
    "comments": {
        "all": ("GET", "comments"),
        "by_id": {
            "all": ("GET", "comments/{ids}"),
            "delete": ("POST", "comments/{id}/delete"),
            "edit": ("POST", "comments/{id}/delete"),
            "flags": {
                "add": ("POST", "comments/{id}/flags/add"),
                "options": ("GET", "comments/{id}/flags/options"),
            },
            "upvote": {
                "cast": ("POST", "comments/{id}/upvote"),
                "undo": ("POST", "comments/{id}/upvote/undo"),
            },
        },
    },
    "errors": {
        "all": ("GET", "errors"),
        "by_id": ("GET", "errors/{id}"),
    },
    "events": ("GET", "events"),
    "filters": {
        "create": ("GET", "filters/create"),
        "decode": ("GET", "filters/{filter}"),
    },
    "inbox": {
        "all": ("GET", "inbox"),
        "unread": ("GET", "inbox/unread"),
    },
    "notifications": {
        "all": ("GET", "notifications"),
        "unread": ("GET", "notifications/unread"),
    },
    "posts": {
        "all": ("GET", "posts"),
        "by_id": {
            "all": ("GET", "posts/{ids}"),
            "comments": {
                "add": ("POST", "posts/{id}/comments/add"),
                "all": ("GET", "posts/{ids}/comments"),
                "render": ("POST", "posts/{id}/comments/render"),
            },
            "revisions": ("GET", "posts/{ids}/revisions"),
            "suggested_edits": ("GET", "posts/{ids}/suggested_edits"),
        },
    },
    "privileges": ("GET", "privileges"),
    "revisions": ("GET", "revisions/{ids}"),
    "search": {
        "all": ("GET", "search"),
        "advanced": ("GET", "search/advanced"),
        "similar": ("GET", "similar"),
        "excerpts": ("GET", "search/excerpts"),
    },
    "sites": ("GET", "sites"),
    "suggested_edits": {
        "all": ("GET", "suggested-edits"),
        "by_id": ("GET", "suggested-edits/{ids}"),
    },
    "tags": {
        "all": ("GET", "tags"),
        "by_tag": {
            "info": ("GET", "tags/{tags}/info"),
            "faq": ("GET", "tags/{tags}/faq"),
            "related": ("GET", "tags/{tags}/related"),
            "synonyms": ("GET", "tags/{tags}/synonyms"),
            "top_answerers": {
                "all_time": ("GET", "tags/{tags}/top-answerers/all_time"),
                "month": ("GET", "tags/{tags}/top-answerers/month"),
            },
            "wikis": ("GET", "tags/{tags}/wikis"),
        },
        "moderator_only": ("GET", "tags/moderator-only"),
        "required": ("GET", "tags/required"),
        "synonyms": ("GET", "tags/synonyms"),
    },
    "users": {
        "all": ("GET", "users"),
        "by_id": {
            "all": ("GET", "users/{ids}"),
            "associated": ("GET", "users/{ids}"),
            "badges": ("GET", "users/{ids}/badges"),
            "comments": {
                "all": ("GET", "users/{ids}/comments"),
                "to_id": ("GET", "user/{ids}/comments/{to_id}"),
            },
            "favorites": ("GET", "users/{ids}/mentioned"),
            "inbox": {
                "all": ("GET", "users/{ids}/inbox"),
                "unread": ("GET", "users/{ids}/inbox/unread"),
            },
            "merges": ("GET", "users/{id}/merges"),
            "network_activity": ("GET", "users/{id}/network-activity"),
            "notifications": {
                "all": ("GET", "users/{id}/notifications"),
                "unread": ("GET", "users/{id}/notifications/unread"),
            },
            "posts": ("GET", "users/{ids}/posts"),
            "privileges": ("GET", "users/{id}/privileges"),
            "questions": {
                "all":  "users/{ids}/questions",
                "featured": ("GET", "users/{ids}/questions/featured"),
                "no_answers": ("GET", "users/{ids}/questions/no-answers"),
                "unaccepted": ("GET", "users/{ids}/questions/unaccepted"),
                "unanswered": ("GET", "users/{ids}/questions/unanswered"),
            },
            "reputation": {
                "recent": ("GET", "users/{ids}/reputation"),
                "history": {
                    "public": ("GET", "users/{id}/reputation-history"),
                    "full": ("GET", "users/{id}/reputation-history/full"),
                },
            },
            "suggested_edits": ("GET", "users/{ids}/suggested-edits"),
            "tags": {
                "all": ("GET", "users/{id}/tags"),
                "by_tag": {
                    "top_answers": ("GET", "users/{id}/tags/{tags}/top-answers"),
                    "top_questions": ("GET", "users/{id}/tags/{tags}/top-questions"),
                },
                "top_tags": {
                    "all": ("GET", "user/{id}/top-tags"),
                    "answers": ("GET", "user/{id}/top-answer-tags"),
                    "questions": ("GET", "user/{id}/top-answer-tags"),
                },
            },
            "timeline": ("GET", "user/{id}s/timeline"),
            "write_permissions": ("GET", "users/{id}/write-permissions"),
        },
        "me": {
            "all": ("GET", "me"),
            "associated": ("GET", "me"),
            "badges": ("GET", "me/badges"),
            "comments": {
                "all": ("GET", "me/comments"),
                "to_id": ("GET", "user/{ids}/comments/{to_id}"),
            },
            "favorites": ("GET", "me/mentioned"),
            "inbox": {
                "all": ("GET", "me/inbox"),
                "unread": ("GET", "me/inbox/unread"),
            },
            "merges": ("GET", "me/merges"),
            "network_activity": ("GET", "me/network-activity"),
            "notifications": {
                "all": ("GET", "me/notifications"),
                "unread": ("GET", "me/notifications/unread"),
            },
            "posts": ("GET", "me/posts"),
            "privileges": ("GET", "me/privileges"),
            "questions": {
                "all":  "me/questions",
                "featured": ("GET", "me/questions/featured"),
                "no_answers": ("GET", "me/questions/no-answers"),
                "unaccepted": ("GET", "me/questions/unaccepted"),
                "unanswered": ("GET", "me/questions/unanswered"),
            },
            "reputation": {
                "recent": ("GET", "me/reputation"),
                "history": {
                    "public": ("GET", "me/reputation-history"),
                    "full": ("GET", "me/reputation-history/full"),
                },
            },
            "suggested_edits": ("GET", "me/suggested-edits"),
            "tags": {
                "all": ("GET", "me/tags"),
                "by_tag": {
                    "top_answers": ("GET", "me/tags/{tags}/top-answers"),
                    "top_questions": ("GET", "me/tags/{tags}/top-questions"),
                },
                "top_tags": {
                    "all": ("GET", "user/{id}/top-tags"),
                    "answers": ("GET", "user/{id}/top-answer-tags"),
                    "questions": ("GET", "user/{id}/top-answer-tags"),
                },
            },
            "timeline": ("GET", "user/{ids}/timeline"),
            "write_permissions": ("GET", "me/write-permissions"),
        },
        "moderators": {
            "all": ("GET", "users/moderators"),
            "elected": ("GET", "users/moderators/elected"),
        },
    },
    "questions": {
        "add": ("POST", "questions/add"),
        "all": ("GET", "questions"),
        "by_id": {
            "answers": {
                "all": ("GET", "questions/{ids}"),
                "add": ("POST", "questions/{ids}/answers/add"),
                "render": ("POST", "questions/{ids}/answers/render"),
            },
            "comments": ("GET", "questions/{ids}/comments"),
            "close": ("POST", "questions/{id}/close/options"),
            "delete": ("POST", "questions/{id}/delete"),
            "downvote": {
                "cast": ("POST", "questions/{id}/downvote"),
                "undo": ("POST", "questions/{id}/downvote/undo"),
            },
            "edit": ("POST", "questions/{id}/edit"),
            "favorite": {
                "cast": ("POST", "questions/{id}/favorite"),
                "undo": ("POST", "questions/{id}/favorite/undo"),
            },
            "flags": {
                "add": ("POST", "questions/{id}/flags/add"),
                "options": ("GET", "questions/{id}/flags/options"),
            },
            "linked": ("GET", "questions/{id}/linked"),
            "related": ("GET", "questions/{id}/related"),
            "timeline": ("GET", "questions/{id}/timeline"),
            "upvote": {
                "cast": ("POST", "questions/{id}/upvote"),
                "undo": ("POST", "questions/{id}/upvote/undo"),
            },
        },
        "featured": ("GET", "questions/featured"),
        "no_answers": ("GET", "questions/no-answers"),
        "render": ("POST", "questions/render"),
        "unanswered": {
            "all": ("GET", "questions/unanswered"),
            "my_tags": ("GET", "questions/unanswered/my-tags"),
        },
    },
}

"""
A dictionary tree of URL endpoints for API query types.
"""
queries = URLTree(_queries, name="queries")
