import abc
from typing import Dict, List, Any, Tuple
from app.models.page_request import *


class PageHandler(abc.ABC):

    def _parse(
        self, topics: List[Dict[str, Any]] | None, page: PageInfo
    ) -> Tuple[List[Dict[str, Any]] | None, bool]:
        if topics and (len(topics) > page.per_page):
            return (
                [topics[i] for i in range(len(topics) - 1)],
                len(topics) > page.per_page,
            )
        return (topics, False)

    def _offset(self, page: PageInfo) -> int:
        if page.page <= 1:
            return 0
        else:
            return (page.page - 1) * page.per_page
