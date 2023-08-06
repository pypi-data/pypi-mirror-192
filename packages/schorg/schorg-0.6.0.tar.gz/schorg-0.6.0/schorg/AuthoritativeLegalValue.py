"""
Indicates that the publisher gives some special status to the publication of the document. ("The Queens Printer" version of a UK Act of Parliament, or the PDF version of a Directive published by the EU Office of Publications.) Something "Authoritative" is considered to be also [[OfficialLegalValue]].

https://schema.org/AuthoritativeLegalValue
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AuthoritativeLegalValueInheritedProperties(TypedDict):
    """Indicates that the publisher gives some special status to the publication of the document. ("The Queens Printer" version of a UK Act of Parliament, or the PDF version of a Directive published by the EU Office of Publications.) Something "Authoritative" is considered to be also [[OfficialLegalValue]].

    References:
        https://schema.org/AuthoritativeLegalValue
    Note:
        Model Depth 5
    Attributes:
    """

    


class AuthoritativeLegalValueProperties(TypedDict):
    """Indicates that the publisher gives some special status to the publication of the document. ("The Queens Printer" version of a UK Act of Parliament, or the PDF version of a Directive published by the EU Office of Publications.) Something "Authoritative" is considered to be also [[OfficialLegalValue]].

    References:
        https://schema.org/AuthoritativeLegalValue
    Note:
        Model Depth 5
    Attributes:
    """

    

#AuthoritativeLegalValueInheritedPropertiesTd = AuthoritativeLegalValueInheritedProperties()
#AuthoritativeLegalValuePropertiesTd = AuthoritativeLegalValueProperties()


class AllProperties(AuthoritativeLegalValueInheritedProperties , AuthoritativeLegalValueProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AuthoritativeLegalValueProperties, AuthoritativeLegalValueInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "AuthoritativeLegalValue"
    return model
    

AuthoritativeLegalValue = create_schema_org_model()