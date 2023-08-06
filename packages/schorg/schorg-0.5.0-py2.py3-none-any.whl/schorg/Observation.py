"""
Instances of the class [[Observation]] are used to specify observations about an entity (which may or may not be an instance of a [[StatisticalPopulation]]), at a particular time. The principal properties of an [[Observation]] are [[observedNode]], [[measuredProperty]], [[measuredValue]] (or [[median]], etc.) and [[observationDate]] ([[measuredProperty]] properties can, but need not always, be W3C RDF Data Cube "measure properties", as in the [lifeExpectancy example](https://www.w3.org/TR/vocab-data-cube/#dsd-example)).See also [[StatisticalPopulation]], and the [data and datasets](/docs/data-and-datasets.html) overview for more details.  

https://schema.org/Observation
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ObservationInheritedProperties(TypedDict):
    """Instances of the class [[Observation]] are used to specify observations about an entity (which may or may not be an instance of a [[StatisticalPopulation]]), at a particular time. The principal properties of an [[Observation]] are [[observedNode]], [[measuredProperty]], [[measuredValue]] (or [[median]], etc.) and [[observationDate]] ([[measuredProperty]] properties can, but need not always, be W3C RDF Data Cube "measure properties", as in the [lifeExpectancy example](https://www.w3.org/TR/vocab-data-cube/#dsd-example)).See also [[StatisticalPopulation]], and the [data and datasets](/docs/data-and-datasets.html) overview for more details.  

    References:
        https://schema.org/Observation
    Note:
        Model Depth 3
    Attributes:
    """

    


class ObservationProperties(TypedDict):
    """Instances of the class [[Observation]] are used to specify observations about an entity (which may or may not be an instance of a [[StatisticalPopulation]]), at a particular time. The principal properties of an [[Observation]] are [[observedNode]], [[measuredProperty]], [[measuredValue]] (or [[median]], etc.) and [[observationDate]] ([[measuredProperty]] properties can, but need not always, be W3C RDF Data Cube "measure properties", as in the [lifeExpectancy example](https://www.w3.org/TR/vocab-data-cube/#dsd-example)).See also [[StatisticalPopulation]], and the [data and datasets](/docs/data-and-datasets.html) overview for more details.  

    References:
        https://schema.org/Observation
    Note:
        Model Depth 3
    Attributes:
        observedNode: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The observedNode of an [[Observation]], often a [[StatisticalPopulation]].
        marginOfError: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A marginOfError for an [[Observation]].
        measuredValue: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The measuredValue of an [[Observation]].
        observationDate: (Optional[Union[List[Union[datetime, SchemaOrgObj, str]], datetime, SchemaOrgObj, str]]): The observationDate of an [[Observation]].
        measuredProperty: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The measuredProperty of an [[Observation]], either a schema.org property, a property from other RDF-compatible systems, e.g. W3C RDF Data Cube, or schema.org extensions such as [GS1's](https://www.gs1.org/voc/?show=properties).
    """

    observedNode: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    marginOfError: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    measuredValue: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    observationDate: NotRequired[Union[List[Union[datetime, SchemaOrgObj, str]], datetime, SchemaOrgObj, str]]
    measuredProperty: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#ObservationInheritedPropertiesTd = ObservationInheritedProperties()
#ObservationPropertiesTd = ObservationProperties()


class AllProperties(ObservationInheritedProperties , ObservationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ObservationProperties, ObservationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Observation"
    return model
    

Observation = create_schema_org_model()