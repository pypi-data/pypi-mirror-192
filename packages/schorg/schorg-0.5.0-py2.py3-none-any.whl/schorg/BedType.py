"""
A type of bed. This is used for indicating the bed or beds available in an accommodation.

https://schema.org/BedType
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BedTypeInheritedProperties(TypedDict):
    """A type of bed. This is used for indicating the bed or beds available in an accommodation.

    References:
        https://schema.org/BedType
    Note:
        Model Depth 5
    Attributes:
        greater: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): This ordering relation for qualitative values indicates that the subject is greater than the object.
        additionalProperty: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A property-value pair representing an additional characteristic of the entity, e.g. a product feature or another characteristic for which there is no matching property in schema.org.Note: Publishers should be aware that applications designed to use specific schema.org properties (e.g. https://schema.org/width, https://schema.org/color, https://schema.org/gtin13, ...) will typically expect such data to be provided using those properties, rather than using the generic property/value mechanism.
        valueReference: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): A secondary value that provides additional information on the original value, e.g. a reference temperature or a type of measurement.
        equal: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): This ordering relation for qualitative values indicates that the subject is equal to the object.
        lesser: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): This ordering relation for qualitative values indicates that the subject is lesser than the object.
        greaterOrEqual: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): This ordering relation for qualitative values indicates that the subject is greater than or equal to the object.
        lesserOrEqual: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): This ordering relation for qualitative values indicates that the subject is lesser than or equal to the object.
        nonEqual: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): This ordering relation for qualitative values indicates that the subject is not equal to the object.
    """

    greater: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    additionalProperty: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    valueReference: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    equal: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    lesser: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    greaterOrEqual: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    lesserOrEqual: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    nonEqual: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class BedTypeProperties(TypedDict):
    """A type of bed. This is used for indicating the bed or beds available in an accommodation.

    References:
        https://schema.org/BedType
    Note:
        Model Depth 5
    Attributes:
    """

    

#BedTypeInheritedPropertiesTd = BedTypeInheritedProperties()
#BedTypePropertiesTd = BedTypeProperties()


class AllProperties(BedTypeInheritedProperties , BedTypeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BedTypeProperties, BedTypeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "BedType"
    return model
    

BedType = create_schema_org_model()