"""
Individual comic issues are serially published as    	part of a larger series. For the sake of consistency, even one-shot issues    	belong to a series comprised of a single issue. All comic issues can be    	uniquely identified by: the combination of the name and volume number of the    	series to which the issue belongs; the issue number; and the variant    	description of the issue (if any).

https://schema.org/ComicIssue
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ComicIssueInheritedProperties(TypedDict):
    """Individual comic issues are serially published as    	part of a larger series. For the sake of consistency, even one-shot issues    	belong to a series comprised of a single issue. All comic issues can be    	uniquely identified by: the combination of the name and volume number of the    	series to which the issue belongs; the issue number; and the variant    	description of the issue (if any).

    References:
        https://schema.org/ComicIssue
    Note:
        Model Depth 4
    Attributes:
        pageEnd: (Optional[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]): The page on which the work ends; for example "138" or "xvi".
        issueNumber: (Optional[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]): Identifies the issue of publication; for example, "iii" or "2".
        pagination: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Any description of pages that is not separated into pageStart and pageEnd; for example, "1-6, 9, 55" or "10-12, 46-49".
        pageStart: (Optional[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]): The page on which the work starts; for example "135" or "xiii".
    """

    pageEnd: NotRequired[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]
    issueNumber: NotRequired[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]
    pagination: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    pageStart: NotRequired[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]
    


class ComicIssueProperties(TypedDict):
    """Individual comic issues are serially published as    	part of a larger series. For the sake of consistency, even one-shot issues    	belong to a series comprised of a single issue. All comic issues can be    	uniquely identified by: the combination of the name and volume number of the    	series to which the issue belongs; the issue number; and the variant    	description of the issue (if any).

    References:
        https://schema.org/ComicIssue
    Note:
        Model Depth 4
    Attributes:
        inker: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The individual who traces over the pencil drawings in ink after pencils are complete.
        letterer: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The individual who adds lettering, including speech balloons and sound effects, to artwork.
        penciler: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The individual who draws the primary narrative artwork.
        variantCover: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): A description of the variant cover    	for the issue, if the issue is a variant printing. For example, "Bryan Hitch    	Variant Cover" or "2nd Printing Variant".
        artist: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The primary artist for a work    	in a medium other than pencils or digital line art--for example, if the    	primary artwork is done in watercolors or digital paints.
        colorist: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The individual who adds color to inked drawings.
    """

    inker: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    letterer: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    penciler: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    variantCover: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    artist: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    colorist: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#ComicIssueInheritedPropertiesTd = ComicIssueInheritedProperties()
#ComicIssuePropertiesTd = ComicIssueProperties()


class AllProperties(ComicIssueInheritedProperties , ComicIssueProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ComicIssueProperties, ComicIssueInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ComicIssue"
    return model
    

ComicIssue = create_schema_org_model()