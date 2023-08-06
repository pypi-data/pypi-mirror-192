"""
A single feed providing structured information about one or more entities or topics.

https://schema.org/DataFeed
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DataFeedInheritedProperties(TypedDict):
    """A single feed providing structured information about one or more entities or topics.

    References:
        https://schema.org/DataFeed
    Note:
        Model Depth 4
    Attributes:
        catalog: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A data catalog which contains this dataset.
        datasetTimeInterval: (Optional[Union[List[Union[datetime, SchemaOrgObj, str]], datetime, SchemaOrgObj, str]]): The range of temporal applicability of a dataset, e.g. for a 2011 census dataset, the year 2011 (in ISO 8601 time interval format).
        variableMeasured: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The variableMeasured property can indicate (repeated as necessary) the  variables that are measured in some dataset, either described as text or as pairs of identifier and description using PropertyValue.
        includedDataCatalog: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A data catalog which contains this dataset (this property was previously 'catalog', preferred name is now 'includedInDataCatalog').
        measurementTechnique: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): A technique or technology used in a [[Dataset]] (or [[DataDownload]], [[DataCatalog]]),corresponding to the method used for measuring the corresponding variable(s) (described using [[variableMeasured]]). This is oriented towards scientific and scholarly dataset publication but may have broader applicability; it is not intended as a full representation of measurement, but rather as a high level summary for dataset discovery.For example, if [[variableMeasured]] is: molecule concentration, [[measurementTechnique]] could be: "mass spectrometry" or "nmr spectroscopy" or "colorimetry" or "immunofluorescence".If the [[variableMeasured]] is "depression rating", the [[measurementTechnique]] could be "Zung Scale" or "HAM-D" or "Beck Depression Inventory".If there are several [[variableMeasured]] properties recorded for some given data object, use a [[PropertyValue]] for each [[variableMeasured]] and attach the corresponding [[measurementTechnique]].      
        distribution: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A downloadable form of this dataset, at a specific location, in a specific format. This property can be repeated if different variations are available. There is no expectation that different downloadable distributions must contain exactly equivalent information (see also [DCAT](https://www.w3.org/TR/vocab-dcat-3/#Class:Distribution) on this point). Different distributions might include or exclude different subsets of the entire dataset, for example.
        includedInDataCatalog: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A data catalog which contains this dataset.
        issn: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The International Standard Serial Number (ISSN) that identifies this serial publication. You can repeat this property to identify different formats of, or the linking ISSN (ISSN-L) for, this serial publication.
    """

    catalog: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    datasetTimeInterval: NotRequired[Union[List[Union[datetime, SchemaOrgObj, str]], datetime, SchemaOrgObj, str]]
    variableMeasured: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    includedDataCatalog: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    measurementTechnique: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    distribution: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    includedInDataCatalog: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    issn: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    


class DataFeedProperties(TypedDict):
    """A single feed providing structured information about one or more entities or topics.

    References:
        https://schema.org/DataFeed
    Note:
        Model Depth 4
    Attributes:
        dataFeedElement: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): An item within a data feed. Data feeds may have many elements.
    """

    dataFeedElement: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    

#DataFeedInheritedPropertiesTd = DataFeedInheritedProperties()
#DataFeedPropertiesTd = DataFeedProperties()


class AllProperties(DataFeedInheritedProperties , DataFeedProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DataFeedProperties, DataFeedInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DataFeed"
    return model
    

DataFeed = create_schema_org_model()