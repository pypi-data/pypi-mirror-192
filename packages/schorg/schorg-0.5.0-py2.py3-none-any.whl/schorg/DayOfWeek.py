"""
The day of the week, e.g. used to specify to which day the opening hours of an OpeningHoursSpecification refer.Originally, URLs from [GoodRelations](http://purl.org/goodrelations/v1) were used (for [[Monday]], [[Tuesday]], [[Wednesday]], [[Thursday]], [[Friday]], [[Saturday]], [[Sunday]] plus a special entry for [[PublicHolidays]]); these have now been integrated directly into schema.org.      

https://schema.org/DayOfWeek
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DayOfWeekInheritedProperties(TypedDict):
    """The day of the week, e.g. used to specify to which day the opening hours of an OpeningHoursSpecification refer.Originally, URLs from [GoodRelations](http://purl.org/goodrelations/v1) were used (for [[Monday]], [[Tuesday]], [[Wednesday]], [[Thursday]], [[Friday]], [[Saturday]], [[Sunday]] plus a special entry for [[PublicHolidays]]); these have now been integrated directly into schema.org.      

    References:
        https://schema.org/DayOfWeek
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class DayOfWeekProperties(TypedDict):
    """The day of the week, e.g. used to specify to which day the opening hours of an OpeningHoursSpecification refer.Originally, URLs from [GoodRelations](http://purl.org/goodrelations/v1) were used (for [[Monday]], [[Tuesday]], [[Wednesday]], [[Thursday]], [[Friday]], [[Saturday]], [[Sunday]] plus a special entry for [[PublicHolidays]]); these have now been integrated directly into schema.org.      

    References:
        https://schema.org/DayOfWeek
    Note:
        Model Depth 4
    Attributes:
    """

    

#DayOfWeekInheritedPropertiesTd = DayOfWeekInheritedProperties()
#DayOfWeekPropertiesTd = DayOfWeekProperties()


class AllProperties(DayOfWeekInheritedProperties , DayOfWeekProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DayOfWeekProperties, DayOfWeekInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DayOfWeek"
    return model
    

DayOfWeek = create_schema_org_model()