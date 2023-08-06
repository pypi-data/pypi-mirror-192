"""
A brand is a name used by an organization or business person for labeling a product, product group, or similar.

https://schema.org/Brand
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BrandInheritedProperties(TypedDict):
    """A brand is a name used by an organization or business person for labeling a product, product group, or similar.

    References:
        https://schema.org/Brand
    Note:
        Model Depth 3
    Attributes:
    """

    


class BrandProperties(TypedDict):
    """A brand is a name used by an organization or business person for labeling a product, product group, or similar.

    References:
        https://schema.org/Brand
    Note:
        Model Depth 3
    Attributes:
        slogan: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): A slogan or motto associated with the item.
        review: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A review of the item.
        logo: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): An associated logo.
        aggregateRating: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The overall rating, based on a collection of reviews or ratings, of the item.
    """

    slogan: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    review: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    logo: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    aggregateRating: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#BrandInheritedPropertiesTd = BrandInheritedProperties()
#BrandPropertiesTd = BrandProperties()


class AllProperties(BrandInheritedProperties , BrandProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BrandProperties, BrandInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Brand"
    return model
    

Brand = create_schema_org_model()