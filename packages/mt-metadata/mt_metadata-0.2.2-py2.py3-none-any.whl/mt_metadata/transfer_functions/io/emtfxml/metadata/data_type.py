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

# =============================================================================
attr_dict = get_schema("data_type", SCHEMA_FN_PATHS)
# =============================================================================


class DataType(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        self.name = None
        self.type = None
        self.description = None
        self.tag = None
        self.external_url = None
        self.intention = None
        self.input = None
        self.output = None
        self.units = None

        super().__init__(attr_dict=attr_dict, **kwargs)
