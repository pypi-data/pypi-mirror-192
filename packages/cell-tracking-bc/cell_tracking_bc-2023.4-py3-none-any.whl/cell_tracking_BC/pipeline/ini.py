# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

from configparser import DEFAULTSECT as DEFAULT_SECTION
from configparser import ConfigParser as config_t
from typing import Any

from cell_tracking_BC.standard.path import path_h


def NewConfigFromPath(path: path_h, /) -> dict[str, dict[str, Any]]:
    """"""
    config = config_t(
        delimiters=("=",), comment_prefixes=("#",), inline_comment_prefixes=("#",)
    )
    config.read(path)

    # TODO: check if config.sections() can be used instead. it does not list the default one
    return {
        _nme: {_prm: _ValueFromStr(_vle) for _prm, _vle in _sct.items()}
        for _nme, _sct in config.items()
        if _nme != DEFAULT_SECTION
    }


def _ValueFromStr(value: str, /) -> Any:
    """"""
    if value.capitalize() == "None":
        output = None
    elif value.capitalize() == "False":
        output = False
    elif value.capitalize() == "True":
        output = True
    elif str.isdigit(value):
        output = int(value)
    elif (output := _AsFloat(value)) is not None:
        pass
    elif "," in value:
        top_level = []
        pieces = value.split(",")
        first_idx = 0
        status = 0
        for last_idx, piece in enumerate(pieces):
            if "(" in piece:
                status += 1
            elif ")" in piece:
                status -= 1
            if status == 0:
                stripped = ",".join(pieces[first_idx : (last_idx + 1)]).strip(" ()")
                top_level.append(stripped)
                first_idx = last_idx + 1
        output = tuple(_ValueFromStr(_vle) for _vle in top_level)
    else:
        output = value

    return output


def _AsFloat(value: str, /) -> float | None:
    """"""
    try:
        output = float(value)
    except ValueError:
        output = None

    return output
