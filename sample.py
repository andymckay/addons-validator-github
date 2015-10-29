data = {
    'pull_request': {
        'head': {
            'repo': {
                'archive_url': 'https://api.github.com/repos/andymckay/sort-tabs-by-url/{archive_format}{/ref}',
                'statuses_url': 'https://api.github.com/repos/andymckay/sort-tabs-by-url/statuses/{sha}',
                'pulls_url': 'https://api.github.com/repos/andymckay/sort-tabs-by-url/pulls{/number}'
            },
            # Note this is going to change.
            'sha': '7dc78ba0f8aa7d8cc7cd23bdbf5523fb5b00015d'
        },
        'number': 1,
    },
    'repository': {
        'commits_url': 'https://api.github.com/repos/andymckay/sort-tabs-by-url/commits{/sha}'
    }
}
result = {
    u'count': 2,
    u'_notices': [{
        u'_type': u'notice',
        u'code': u'TYPE_NO_INSTALL_RDF',
        u'message': u'install.rdf was not found',
        u'description': u"The type should be determined by install.rdf if present. As there's no install.rdf, type detection will be attempted to be inferred by package layout."
    }],
    u'errors': [{
        u'_type': u'error',
        u'code': u'JS_SYNTAX_ERROR',
        u'description': u'There is a JavaScript syntax error in your code; validation cannot continue on this file.',
        u'column': 13,
        u'file': u'andymckay-sort-tabs-by-url-e2dacfd/lib/main.js',
        u'message': u'JavaScript syntax error',
        u'line': 1
    }],
    u'warnings': [],
    u'summary': {
        u'notices': 1,
        u'errors': 1,
        u'warnings': 0
    }
}
