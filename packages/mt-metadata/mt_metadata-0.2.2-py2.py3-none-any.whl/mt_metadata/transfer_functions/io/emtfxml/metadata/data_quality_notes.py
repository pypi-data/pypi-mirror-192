# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 21:30:36 2020

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS
from . import Comment

# =============================================================================
attr_dict = get_schema("data_quality_notes", SCHEMA_FN_PATHS)
attr_dict.add_dict(get_schema("comment", SCHEMA_FN_PATHS), "comments")
# =============================================================================


class DataQualityNotes(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        self.good_from_period = None
        self.good_to_period = None
        self.rating = 0
        self.comments = Comment()
        super().__init__(attr_dict=attr_dict, **kwargs)
