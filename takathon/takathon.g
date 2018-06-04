start: _TEST _NEWLINE _INDENT (_stmt | import_stmt | domain_stmt)+ _DEDENT

import_stmt: IMPORT_STMT _NEWLINE
domain_stmt: DOMAIN_STMT _results_stmt
    | DOMAIN_STMT _NEWLINE+ _INDENT _stmt* _results_stmt _DEDENT

_stmt: mock_stmt

mock_stmt: MOCK_STMT _NEWLINE
_results_stmt: RESULTS_STMT [_NEWLINE]

_TEST: "test:"
DOMAIN_STMT: /domain .*?:/
MOCK_STMT: /mock .+? as .+/
RESULTS_STMT: /results .+/
IMPORT_STMT: /(from .+?)? import .+/

COMMENT: /#[^\n]*/
_NEWLINE: ( /\r?\n[\t ]*/ | COMMENT )+
_INDENT: "<INDENT>"
_DEDENT: "<DEDENT>"

%import common.WS_INLINE
%ignore WS_INLINE
%ignore COMMENT
