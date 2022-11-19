# Constructs a DISCOSWeb query with the given parameters.



from .filtering import APIFilter

from typing import Optional


class Query:
    def __init__(self, filter: Optional[APIFilter]=None):
        if filter is None:
            self.filter = APIFilter()
        else:
            self.filter = filter

    def build(self) -> str:
        """Buils the full URL to perform this query"""

        return f"https://discosweb.esoc.esa.int/api/objects?filter={self.filter.apistring}"
