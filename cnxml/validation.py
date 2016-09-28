# -*- coding: utf-8 -*-
import subprocess
from pathlib import Path

from .jing import jing
from .util import lookup_resource

__all__ = (
    'CNXML_JING_RNG',
    'validate_cnxml',
)


CNXML_JING_RNG = lookup_resource('xml/cnxml/schema/rng/0.7/cnxml-jing.rng')


def validate_cnxml(content_filepath):
    """Validates the given CNXML file against the cnxml-jing.rng RNG."""
    content_filepath = Path(content_filepath).resolve()
    return jing(CNXML_JING_RNG, content_filepath)