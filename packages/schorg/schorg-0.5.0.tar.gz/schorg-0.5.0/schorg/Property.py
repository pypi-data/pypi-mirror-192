"""
A property, used to indicate attributes and relationships of some Thing; equivalent to rdf:Property.

https://schema.org/Property
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PropertyInheritedProperties(TypedDict):
    """A property, used to indicate attributes and relationships of some Thing; equivalent to rdf:Property.

    References:
        https://schema.org/Property
    Note:
        Model Depth 3
    Attributes:
    """

    


class PropertyProperties(TypedDict):
    """A property, used to indicate attributes and relationships of some Thing; equivalent to rdf:Property.

    References:
        https://schema.org/Property
    Note:
        Model Depth 3
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
        domainIncludes: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a property to a class that is (one of) the type(s) the property is expected to be used on.
        inverseOf: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a property to a property that is its inverse. Inverse properties relate the same pairs of items to each other, but in reversed direction. For example, the 'alumni' and 'alumniOf' properties are inverseOf each other. Some properties don't have explicit inverses; in these situations RDFa and JSON-LD syntax for reverse properties can be used.
        rangeIncludes: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a property to a class that constitutes (one of) the expected type(s) for values of the property.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    domainIncludes: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    inverseOf: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    rangeIncludes: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#PropertyInheritedPropertiesTd = PropertyInheritedProperties()
#PropertyPropertiesTd = PropertyProperties()


class AllProperties(PropertyInheritedProperties , PropertyProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PropertyProperties, PropertyInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Property"
    return model
    

Property = create_schema_org_model()