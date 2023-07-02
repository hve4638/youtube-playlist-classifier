class ParseFailException(Exception):
    pass

class SymbolMissingException(ParseFailException):
    pass

class SymbolConflictException(ParseFailException):
    pass

FILTER_PASS = {"filtertype":  "filterpass"}
FILTER_DROP = {"filtertype":  "filterdrop"}

