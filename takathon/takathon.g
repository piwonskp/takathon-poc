start: _TEST _NEWLINE _INDENT (_stmt | import_stmt | domain_stmt)+ _DEDENT

import_stmt: IMPORT_STMT _NEWLINE
domain_stmt: DOMAIN_STMT fun_call
    | DOMAIN_STMT _NEWLINE+ _INDENT _stmt* fun_call _DEDENT

_stmt: mock_stmt

mock_stmt: MOCK_STMT _NEWLINE
fun_call: _results_stmt | _throws_stmt
_results_stmt: RESULTS_STMT [_NEWLINE]
_throws_stmt: THROWS_STMT [_NEWLINE]

_TEST: "test:"
DOMAIN_STMT: /domain .*?:/
MOCK_STMT: /mock .+? as .+/
RESULTS_STMT: /results .+/
IMPORT_STMT: /(from .+? )?import .+/
THROWS_STMT: /throws .+/

COMMENT: /#[^\n]*/
_NEWLINE: ( /\r?\n[\t ]*/ | COMMENT )+
_INDENT: "<INDENT>"
_DEDENT: "<DEDENT>"

%import common.WS_INLINE
%ignore WS_INLINE
%ignore COMMENT
