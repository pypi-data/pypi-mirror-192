"""
Specifies that product returns must be done by mail.

https://schema.org/ReturnByMail
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ReturnByMailInheritedProperties(TypedDict):
    """Specifies that product returns must be done by mail.

    References:
        https://schema.org/ReturnByMail
    Note:
        Model Depth 5
    Attributes:
    """

    


class ReturnByMailProperties(TypedDict):
    """Specifies that product returns must be done by mail.

    References:
        https://schema.org/ReturnByMail
    Note:
        Model Depth 5
    Attributes:
    """

    

#ReturnByMailInheritedPropertiesTd = ReturnByMailInheritedProperties()
#ReturnByMailPropertiesTd = ReturnByMailProperties()


class AllProperties(ReturnByMailInheritedProperties , ReturnByMailProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ReturnByMailProperties, ReturnByMailInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ReturnByMail"
    return model
    

ReturnByMail = create_schema_org_model()