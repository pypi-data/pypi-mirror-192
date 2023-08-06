"""
A country.

https://schema.org/Country
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class CountryInheritedProperties(TypedDict):
    """A country.

    References:
        https://schema.org/Country
    Note:
        Model Depth 4
    Attributes:
    """

    


class CountryProperties(TypedDict):
    """A country.

    References:
        https://schema.org/Country
    Note:
        Model Depth 4
    Attributes:
    """

    

#CountryInheritedPropertiesTd = CountryInheritedProperties()
#CountryPropertiesTd = CountryProperties()


class AllProperties(CountryInheritedProperties , CountryProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[CountryProperties, CountryInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Country"
    return model
    

Country = create_schema_org_model()