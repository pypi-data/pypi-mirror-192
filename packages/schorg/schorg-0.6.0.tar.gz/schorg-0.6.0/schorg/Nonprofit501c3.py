"""
Nonprofit501c3: Non-profit type referring to Religious, Educational, Charitable, Scientific, Literary, Testing for Public Safety, Fostering National or International Amateur Sports Competition, or Prevention of Cruelty to Children or Animals Organizations.

https://schema.org/Nonprofit501c3
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class Nonprofit501c3InheritedProperties(TypedDict):
    """Nonprofit501c3: Non-profit type referring to Religious, Educational, Charitable, Scientific, Literary, Testing for Public Safety, Fostering National or International Amateur Sports Competition, or Prevention of Cruelty to Children or Animals Organizations.

    References:
        https://schema.org/Nonprofit501c3
    Note:
        Model Depth 6
    Attributes:
    """

    


class Nonprofit501c3Properties(TypedDict):
    """Nonprofit501c3: Non-profit type referring to Religious, Educational, Charitable, Scientific, Literary, Testing for Public Safety, Fostering National or International Amateur Sports Competition, or Prevention of Cruelty to Children or Animals Organizations.

    References:
        https://schema.org/Nonprofit501c3
    Note:
        Model Depth 6
    Attributes:
    """

    

#Nonprofit501c3InheritedPropertiesTd = Nonprofit501c3InheritedProperties()
#Nonprofit501c3PropertiesTd = Nonprofit501c3Properties()


class AllProperties(Nonprofit501c3InheritedProperties , Nonprofit501c3Properties, TypedDict):
    pass


def create_schema_org_model(type_: Union[Nonprofit501c3Properties, Nonprofit501c3InheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nonprofit501c3"
    return model
    

Nonprofit501c3 = create_schema_org_model()