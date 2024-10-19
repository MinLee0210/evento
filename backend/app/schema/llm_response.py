import typing_extensions as typing


class Keyword(typing.TypedDict):
    keyword: str


class RefineQuery(typing.TypedDict):
    refine_response: str
