"""
A single season of a podcast. Many podcasts do not break down into separate seasons. In that case, PodcastSeries should be used.

https://schema.org/PodcastSeason
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PodcastSeasonInheritedProperties(TypedDict):
    """A single season of a podcast. Many podcasts do not break down into separate seasons. In that case, PodcastSeries should be used.

    References:
        https://schema.org/PodcastSeason
    Note:
        Model Depth 4
    Attributes:
        seasonNumber: (Optional[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]): Position of the season within an ordered group of seasons.
        actor: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): An actor, e.g. in TV, radio, movie, video games etc., or in an event. Actors can be associated with individual items or with a series, episode, clip.
        trailer: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The trailer of a movie or TV/radio series, season, episode, etc.
        productionCompany: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The production company or studio responsible for the item, e.g. series, video game, episode etc.
        episodes: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): An episode of a TV/radio series or season.
        partOfSeries: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The series to which this episode or season belongs.
        episode: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): An episode of a TV, radio or game media within a series or season.
        director: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A director of e.g. TV, radio, movie, video gaming etc. content, or of an event. Directors can be associated with individual items or with a series, episode, clip.
        startDate: (Optional[Union[List[Union[datetime, SchemaOrgObj, str, date]], datetime, SchemaOrgObj, str, date]]): The start date and time of the item (in [ISO 8601 date format](http://en.wikipedia.org/wiki/ISO_8601)).
        numberOfEpisodes: (Optional[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]): The number of episodes in this season or series.
        endDate: (Optional[Union[List[Union[datetime, SchemaOrgObj, str, date]], datetime, SchemaOrgObj, str, date]]): The end date and time of the item (in [ISO 8601 date format](http://en.wikipedia.org/wiki/ISO_8601)).
    """

    seasonNumber: NotRequired[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]
    actor: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    trailer: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    productionCompany: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    episodes: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    partOfSeries: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    episode: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    director: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    startDate: NotRequired[Union[List[Union[datetime, SchemaOrgObj, str, date]], datetime, SchemaOrgObj, str, date]]
    numberOfEpisodes: NotRequired[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]
    endDate: NotRequired[Union[List[Union[datetime, SchemaOrgObj, str, date]], datetime, SchemaOrgObj, str, date]]
    


class PodcastSeasonProperties(TypedDict):
    """A single season of a podcast. Many podcasts do not break down into separate seasons. In that case, PodcastSeries should be used.

    References:
        https://schema.org/PodcastSeason
    Note:
        Model Depth 4
    Attributes:
    """

    

#PodcastSeasonInheritedPropertiesTd = PodcastSeasonInheritedProperties()
#PodcastSeasonPropertiesTd = PodcastSeasonProperties()


class AllProperties(PodcastSeasonInheritedProperties , PodcastSeasonProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PodcastSeasonProperties, PodcastSeasonInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PodcastSeason"
    return model
    

PodcastSeason = create_schema_org_model()