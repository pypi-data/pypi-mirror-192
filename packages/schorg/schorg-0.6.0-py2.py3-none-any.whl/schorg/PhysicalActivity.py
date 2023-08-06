"""
Any bodily activity that enhances or maintains physical fitness and overall health and wellness. Includes activity that is part of daily living and routine, structured exercise, and exercise prescribed as part of a medical treatment or recovery plan.

https://schema.org/PhysicalActivity
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PhysicalActivityInheritedProperties(TypedDict):
    """Any bodily activity that enhances or maintains physical fitness and overall health and wellness. Includes activity that is part of daily living and routine, structured exercise, and exercise prescribed as part of a medical treatment or recovery plan.

    References:
        https://schema.org/PhysicalActivity
    Note:
        Model Depth 4
    Attributes:
    """

    


class PhysicalActivityProperties(TypedDict):
    """Any bodily activity that enhances or maintains physical fitness and overall health and wellness. Includes activity that is part of daily living and routine, structured exercise, and exercise prescribed as part of a medical treatment or recovery plan.

    References:
        https://schema.org/PhysicalActivity
    Note:
        Model Depth 4
    Attributes:
        pathophysiology: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Changes in the normal mechanical, physical, and biochemical functions that are associated with this activity or condition.
        epidemiology: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The characteristics of associated patients, such as age, gender, race etc.
        category: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): A category for the item. Greater signs or slashes can be used to informally indicate a category hierarchy.
        associatedAnatomy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The anatomy of the underlying organ system or structures associated with this entity.
    """

    pathophysiology: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    epidemiology: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    category: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    associatedAnatomy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#PhysicalActivityInheritedPropertiesTd = PhysicalActivityInheritedProperties()
#PhysicalActivityPropertiesTd = PhysicalActivityProperties()


class AllProperties(PhysicalActivityInheritedProperties , PhysicalActivityProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PhysicalActivityProperties, PhysicalActivityInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PhysicalActivity"
    return model
    

PhysicalActivity = create_schema_org_model()