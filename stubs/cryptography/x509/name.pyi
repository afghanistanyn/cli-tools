# Stubs for cryptography.x509.name (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from enum import Enum
from typing import Any

class _ASN1Type(Enum):
    UTF8String: int = ...
    NumericString: int = ...
    PrintableString: int = ...
    T61String: int = ...
    IA5String: int = ...
    UTCTime: int = ...
    GeneralizedTime: int = ...
    VisibleString: int = ...
    UniversalString: int = ...
    BMPString: int = ...

class NameAttribute:
    def __init__(self, oid: Any, value: Any, _type: Any = ...) -> None: ...
    oid: Any = ...
    value: Any = ...
    def rfc4514_string(self): ...
    def __eq__(self, other: Any): ...
    def __ne__(self, other: Any): ...
    def __hash__(self): ...

class RelativeDistinguishedName:
    def __init__(self, attributes: Any) -> None: ...
    def get_attributes_for_oid(self, oid: Any): ...
    def rfc4514_string(self): ...
    def __eq__(self, other: Any): ...
    def __ne__(self, other: Any): ...
    def __hash__(self): ...
    def __iter__(self): ...
    def __len__(self): ...

class Name:
    def __init__(self, attributes: Any) -> None: ...
    def rfc4514_string(self): ...
    def get_attributes_for_oid(self, oid: Any): ...
    @property
    def rdns(self): ...
    def public_bytes(self, backend: Any): ...
    def __eq__(self, other: Any): ...
    def __ne__(self, other: Any): ...
    def __hash__(self): ...
    def __iter__(self) -> None: ...
    def __len__(self): ...
