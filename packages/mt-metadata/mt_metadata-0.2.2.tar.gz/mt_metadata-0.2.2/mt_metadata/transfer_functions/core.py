# -*- coding: utf-8 -*-
"""
.. module:: TF
   :synopsis: The main container for transfer functions

.. moduleauthor:: Jared Peacock <jpeacock@usgs.gov>
"""

# ==============================================================================
from pathlib import Path
from copy import deepcopy

import numpy as np
import xarray as xr

from mt_metadata.transfer_functions.tf import (
    Survey,
    Station,
    Run,
    Electric,
    Magnetic,
)
from mt_metadata.utils.mt_logger import setup_logger
from mt_metadata.transfer_functions.io.readwrite import read_file, write_file
from mt_metadata.base.helpers import validate_name

DEFAULT_CHANNEL_NOMENCLATURE = {
    "hx": "hx",
    "hy": "hy",
    "hz": "hz",
    "ex": "ex",
    "ey": "ey",
}
# =============================================================================
class TF:
    """
    Generic container to hold information about an electromagnetic
    transfer funtion

    The thought here is to have a central container TF.dataset which is an
    xarray.Dataset that contains the impedance, tipper, errors and covariance
    values.  There are helper functions to get and set these from the
    TF.dataset.  Cause most of the time the user will want just the impedance
    or the tipper and associated errors.  We are accommodating EMTF style
    covariances to accurately rotated data errors.

    When reading and writing edi files this information will be lost.

    """

    def __init__(self, fn=None, **kwargs):
        self.logger = setup_logger(f"{__name__}.{self.__class__.__name__}")

        # set metadata for the station
        self.survey_metadata = Survey(id="unknown_survey")
        self.station_metadata = Station()
        self.station_metadata.add_run(Run())
        self.station_metadata.runs[0].ex = Electric(component="ex")
        self.station_metadata.runs[0].ey = Electric(component="ey")
        self.station_metadata.runs[0].hx = Magnetic(component="hx")
        self.station_metadata.runs[0].hy = Magnetic(component="hy")
        self.station_metadata.runs[0].hz = Magnetic(component="hz")
        self.channel_nomenclature = kwargs.get(
            "channel_nomenclature", DEFAULT_CHANNEL_NOMENCLATURE
        )

        self._rotation_angle = 0
        self.save_dir = Path.cwd()

        self._dataset_attr_dict = {
            "survey": "survey_metadata.id",
            "project": "survey_metadata.project",
            "id": "station_metadata.id",
            "name": "station_metadata.geographic_name",
            "latitude": "station_metadata.location.latitude",
            "longitude": "station_metadata.location.longitude",
            "elevation": "station_metadata.location.elevation",
            "declination": "station_metadata.location.declination.value",
            "datum": "station_metadata.location.datum",
            "acquired_by": "station_metadata.acquired_by.author",
            "start": "station_metadata.time_period.start",
            "end": "station_metadata.time_period.end",
            "runs_processed": "station_metadata.run_list",
            "coordinate_system": "station_metadata.orientation.reference_frame",
        }
        # unpack channel nomenclature dict
        self.ex = self.channel_nomenclature["ex"]
        self.ey = self.channel_nomenclature["ey"]
        self.hx = self.channel_nomenclature["hx"]
        self.hy = self.channel_nomenclature["hy"]
        self.hz = self.channel_nomenclature["hz"]
        self.ex_ey = [self.ex, self.ey]
        self.hx_hy = [self.hx, self.hy]
        self.ex_ey_hz = [self.ex, self.ey, self.hz]

        self._ch_input_dict = {
            "impedance": self.hx_hy,
            "tipper": self.hx_hy,
            "impedance_error": self.hx_hy,
            "impedance_model_error": self.hx_hy,
            "tipper_error": self.hx_hy,
            "tipper_model_error": self.hx_hy,
            "isp": self.hx_hy,
            "res": self.ex_ey_hz,
            "tf": self.hx_hy,
            "tf_error": self.hx_hy,
        }

        self._ch_output_dict = {
            "impedance": self.ex_ey,
            "tipper": [self.hz],
            "impedance_error": self.ex_ey,
            "impedance_model_error": self.ex_ey,
            "tipper_error": [self.hz],
            "tipper_model_error": [self.hz],
            "isp": self.hx_hy,
            "res": self.ex_ey_hz,
            "tf": self.ex_ey_hz,
            "tf_error": self.ex_ey_hz,
        }

        self._transfer_function = self._initialize_transfer_function()

        # provide key words to fill values if an edi file does not exist
        for key in list(kwargs.keys()):
            setattr(self, key, kwargs[key])

        self.fn = fn

    def __str__(self):
        lines = [f"Station: {self.station}", "-" * 50]
        lines.append(f"\tSurvey:            {self.survey_metadata.id}")
        lines.append(f"\tProject:           {self.survey_metadata.project}")
        lines.append(
            f"\tAcquired by:       {self.station_metadata.acquired_by.author}"
        )
        lines.append(
            f"\tAcquired date:     {self.station_metadata.time_period.start_date}"
        )
        lines.append(f"\tLatitude:          {self.latitude:.3f}")
        lines.append(f"\tLongitude:         {self.longitude:.3f}")
        lines.append(f"\tElevation:         {self.elevation:.3f}")
        lines.append("\tDeclination:   ")
        lines.append(
            f"\t\tValue:     {self.station_metadata.location.declination.value}"
        )
        lines.append(
            f"\t\tModel:     {self.station_metadata.location.declination.model}"
        )
        lines.append(
            f"\tCoordinate System: {self.station_metadata.orientation.reference_frame}"
        )

        lines.append(f"\tImpedance:         {self.has_impedance()}")
        lines.append(f"\tTipper:            {self.has_tipper()}")

        if self.period is not None:
            lines.append(f"\tN Periods:     {len(self.period)}")

            lines.append("\tPeriod Range:")
            lines.append(f"\t\tMin:   {self.period.min():.5E} s")
            lines.append(f"\t\tMax:   {self.period.max():.5E} s")

            lines.append("\tFrequency Range:")
            lines.append(f"\t\tMin:   {1./self.period.max():.5E} Hz")
            lines.append(f"\t\tMax:   {1./self.period.min():.5E} Hz")
        return "\n".join(lines)

    def __repr__(self):
        lines = []
        lines.append(f"station='{self.station}'")
        lines.append(f"latitude={self.latitude:.2f}")
        lines.append(f"longitude={self.longitude:.2f}")
        lines.append(f"elevation={self.elevation:.2f}")

        return f"TF( {(', ').join(lines)} )"

    def __eq__(self, other):
        is_equal = True
        if not isinstance(other, TF):
            self.logger.info(f"Comparing object is not TF, type {type(other)}")
            is_equal = False
        if self.station_metadata != other.station_metadata:
            self.logger.info("Station metadata is not equal")
            is_equal = False
        if self.survey_metadata != other.survey_metadata:
            self.logger.info("Survey Metadata is not equal")
            is_equal = False
        if (self.transfer_function != other.transfer_function).any():
            self.logger.info("TF is not equal")
            is_equal = False
        return is_equal

    def copy(self):
        return deepcopy(self)

    def _initialize_transfer_function(self, periods=[1]):
        """
        create an empty x array for the data.  For now this accommodates
        a single processed station.


        :return: DESCRIPTION
        :rtype: TYPE

        """
        # create an empty array for the transfer function
        tf = xr.DataArray(
            data=0 + 0j,
            dims=["period", "output", "input"],
            coords={
                "period": periods,
                "output": self._ch_output_dict["tf"],
                "input": self._ch_input_dict["tf"],
            },
            name="transfer_function",
        )

        tf_err = xr.DataArray(
            data=0,
            dims=["period", "output", "input"],
            coords={
                "period": periods,
                "output": self._ch_output_dict["tf"],
                "input": self._ch_input_dict["tf"],
            },
            name="transfer_function_error",
        )

        tf_model_err = xr.DataArray(
            data=0,
            dims=["period", "output", "input"],
            coords={
                "period": periods,
                "output": self._ch_output_dict["tf"],
                "input": self._ch_input_dict["tf"],
            },
            name="transfer_function_model_error",
        )

        inv_signal_power = xr.DataArray(
            data=0 + 0j,
            dims=["period", "output", "input"],
            coords={
                "period": periods,
                "output": self._ch_output_dict["isp"],
                "input": self._ch_input_dict["isp"],
            },
            name="inverse_signal_power",
        )

        residual_covariance = xr.DataArray(
            data=0 + 0j,
            dims=["period", "output", "input"],
            coords={
                "period": periods,
                "output": self._ch_output_dict["res"],
                "input": self._ch_input_dict["res"],
            },
            name="residual_covariance",
        )

        # will need to add in covariance in some fashion
        return xr.Dataset(
            {
                tf.name: tf,
                tf_err.name: tf_err,
                tf_model_err.name: tf_model_err,
                inv_signal_power.name: inv_signal_power,
                residual_covariance.name: residual_covariance,
            }
        )

    # ==========================================================================
    # Properties
    # ==========================================================================
    @property
    def fn(self):
        """reference to original data file"""
        return self._fn

    @fn.setter
    def fn(self, value):
        """set file name"""
        if value is None:
            self._fn = None
            return
        self._fn = Path(value)
        self.save_dir = self._fn.parent

    @property
    def latitude(self):
        """Latitude"""
        return self.station_metadata.location.latitude

    @latitude.setter
    def latitude(self, latitude):
        """
        set latitude making sure the input is in decimal degrees

        upon setting utm coordinates are recalculated
        """
        self.station_metadata.location.latitude = latitude

    @property
    def longitude(self):
        """Longitude"""
        return self.station_metadata.location.longitude

    @longitude.setter
    def longitude(self, longitude):
        """
        set longitude making sure the input is in decimal degrees

        upon setting utm coordinates are recalculated
        """
        self.station_metadata.location.longitude = longitude

    @property
    def elevation(self):
        """Elevation"""
        return self.station_metadata.location.elevation

    @elevation.setter
    def elevation(self, elevation):
        """
        set elevation, should be input as meters
        """
        self.station_metadata.location.elevation = elevation

    @property
    def dataset(self):
        """
        This will return an xarray dataset with proper metadata

        :return: DESCRIPTION
        :rtype: TYPE

        """

        for key, mkey in self._dataset_attr_dict.items():
            obj, attr = mkey.split(".", 1)
            value = getattr(self, obj).get_attr_from_name(attr)

            self._transfer_function.attrs[key] = value
        return self._transfer_function

    def _validate_input_ndarray(self, ndarray, atype="impedance"):
        """
        Validate the input based on array type and component
        :param atype: DESCRIPTION, defaults to "impedance"
        :type atype: TYPE, optional
        :return: DESCRIPTION
        :rtype: TYPE

        """
        shape_dict = {
            "impedance": (2, 2),
            "tipper": (1, 2),
            "impedance_error": (2, 2),
            "impedance_model_error": (2, 2),
            "tipper_error": (1, 2),
            "tipper_model_error": (1, 2),
            "isp": (2, 2),
            "res": (3, 3),
            "transfer_function": (3, 2),
            "transfer_function_error": (3, 2),
            "tf": (3, 2),
            "tf_error": (3, 2),
        }

        shape = shape_dict[atype]
        if ndarray.shape[1:] != shape:
            msg = "%s must be have shape (n_periods, %s, %s), not %s"
            self.logger.error(msg, atype, shape[0], shape[1], ndarray.shape)
            raise TFError(msg % (atype, shape[0], shape[1], ndarray.shape))
        if ndarray.shape[0] != self.period.size:
            msg = "New %s shape %s not same as old %s, suggest creating a new instance."
            self.logger.error(msg, atype, ndarray.shape, shape)
            raise TFError(msg % (atype, ndarray.shape, shape))

    def _validate_input_dataarray(self, da, atype="impedance"):
        """
        Validate an input data array

        :param da: DESCRIPTION
        :type da: TYPE
        :param atype: DESCRIPTION, defaults to "impedance"
        :type atype: TYPE, optional
        :return: DESCRIPTION
        :rtype: TYPE

        """

        ch_in = self._ch_input_dict[atype]
        ch_out = self._ch_output_dict[atype]

        # should test for shape
        if "period" not in da.coords.keys() or "input" not in da.coords.keys():
            msg = "Coordinates must be period, output, input, not %s"
            self.logger.error(msg, list(da.coords.keys()))
            raise TFError(msg % da.coords.keys())
        if sorted(ch_out) != sorted(da.coords["output"].data.tolist()):
            msg = "Output dimensions must be %s not %s"
            self.logger.error(msg, ch_out, da.coords["output"].data.tolist())
            raise TFError(msg % (ch_out, da.coords["output"].data.tolist()))
        if sorted(ch_in) != sorted(da.coords["input"].data.tolist()):
            msg = "Input dimensions must be %s not %s"
            self.logger.error(msg, ch_in, da.coords["input"].data.tolist())
            raise TFError(msg % (ch_in, da.coords["input"].data.tolist()))
        # need to reorder the data array to the expected coordinates
        da = da.reindex(output=ch_out, input=ch_in)
        # if this is the first instantiation then just resize the
        # transfer function to fit the input
        if (
            self._transfer_function.transfer_function.data.shape[0] == 1
            and not self.has_tipper()
            and not self.has_impedance()
        ):
            self._transfer_function = self._initialize_transfer_function(
                da.period
            )
            return da
        elif (
            self._transfer_function.transfer_function.data.shape[0]
            == da.data.shape[0]
        ):
            return da
        else:
            msg = "Reassigning with a different shape is dangerous.  Should re-initialize transfer_function or make a new instance of TF"
            self.logger.error(msg)
            raise TFError(msg)

    def _set_data_array(self, value, atype):
        """

        :param value: DESCRIPTION
        :type value: TYPE
        :param atype: DESCRIPTION
        :type atype: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        if value is None:
            return

        key_dict = {
            "tf": "transfer_function",
            "impedance": "transfer_function",
            "tipper": "transfer_function",
            "isp": "inverse_signal_power",
            "res": "residual_covariance",
            "transfer_function": "transfer_function",
            "impedance_error": "transfer_function_error",
            "impedance_model_error": "transfer_function_model_error",
            "tipper_error": "transfer_function_error",
            "tipper_model_error": "transfer_function_model_error",
            "tf_error": "transfer_function_error",
            "tf_model_error": "transfer_function_model_error",
            "transfer_function_error": "transfer_function_error",
            "transfer_function_model_error": "transfer_function_model_error",
        }
        key = key_dict[atype]
        ch_in = self._ch_input_dict[atype]
        ch_out = self._ch_output_dict[atype]
        comps = dict(input=ch_in, output=ch_out)

        if isinstance(value, (list, tuple, np.ndarray)):
            value = np.array(value)
            self._validate_input_ndarray(value, atype=atype)

            self._transfer_function[key].loc[comps] = value
        elif isinstance(value, xr.DataArray):
            nda = self._validate_input_dataarray(value, atype=atype)

            self._transfer_function[key].loc[comps] = nda
        else:
            msg = "Data type %s not supported use a numpy array or xarray.DataArray"
            self.logger.error(msg, type(value))
            raise TFError(msg % type(value))

    def has_transfer_function(self):
        """
        Check to see if the transfer function is not 0 and has
        transfer function components

        :return: DESCRIPTION
        :rtype: TYPE

        """
        outputs = self._transfer_function.transfer_function.coords[
            "output"
        ].data.tolist()
        if self.ex in outputs or self.ey in outputs or self.hz in outputs:
            if np.all(
                self._transfer_function.transfer_function.sel(
                    input=self._ch_input_dict["tf"],
                    output=self._ch_output_dict["tf"],
                ).data
                == 0
            ):
                return False
            return True
        return False

    @property
    def transfer_function(self):
        """

        :return: DESCRIPTION
        :rtype: TYPE

        """
        if self.has_transfer_function():
            ds = self.dataset.transfer_function.sel(
                input=self.hx_hy, output=self.ex_ey_hz
            )
            for key, mkey in self._dataset_attr_dict.items():
                obj, attr = mkey.split(".", 1)
                value = getattr(self, obj).get_attr_from_name(attr)

                ds.attrs[key] = value
            return ds

    @transfer_function.setter
    def transfer_function(self, value):
        """
        Set the impedance from values

        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        self._set_data_array(value, "tf")

    @property
    def transfer_function_error(self):
        """

        :return: DESCRIPTION
        :rtype: TYPE

        """
        if self.has_transfer_function():
            ds = self.dataset.transfer_function_error.sel(
                input=self.hx_hy, output=self.ex_ey_hz
            )
            for key, mkey in self._dataset_attr_dict.items():
                obj, attr = mkey.split(".", 1)
                value = getattr(self, obj).get_attr_from_name(attr)

                ds.attrs[key] = value
            return ds

    @transfer_function_error.setter
    def transfer_function_error(self, value):
        """
        Set the impedance from values

        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        self._set_data_array(value, "tf_error")

    @property
    def transfer_function_model_error(self):
        """

        :return: DESCRIPTION
        :rtype: TYPE

        """
        if self.has_transfer_function():
            ds = self.dataset.transfer_function_model_error.sel(
                input=self.hx_hy, output=self.ex_ey_hz
            )
            for key, mkey in self._dataset_attr_dict.items():
                obj, attr = mkey.split(".", 1)
                value = getattr(self, obj).get_attr_from_name(attr)

                ds.attrs[key] = value
            return ds

    @transfer_function_model_error.setter
    def transfer_function_model_error(self, value):
        """
        Set the impedance from values

        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        self._set_data_array(value, "tf_model_error")

    def has_impedance(self):
        """
        Check to see if the transfer function is not 0 and has
        transfer function components

        :return: DESCRIPTION
        :rtype: TYPE

        """
        outputs = self._transfer_function.transfer_function.coords[
            "output"
        ].data.tolist()
        if self.ex in outputs or self.ey in outputs:
            if np.all(
                self._transfer_function.transfer_function.sel(
                    input=self._ch_input_dict["impedance"],
                    output=self._ch_output_dict["impedance"],
                ).data
                == 0
            ):
                return False
            return True
        return False

    @property
    def impedance(self):
        """

        :return: DESCRIPTION
        :rtype: TYPE

        """
        if self.has_impedance():
            z = self.dataset.transfer_function.sel(
                input=self._ch_input_dict["impedance"],
                output=self._ch_output_dict["impedance"],
            )
            z.name = "impedance"
            for key, mkey in self._dataset_attr_dict.items():
                obj, attr = mkey.split(".", 1)
                value = getattr(self, obj).get_attr_from_name(attr)

                z.attrs[key] = value
            return z

    @impedance.setter
    def impedance(self, value):
        """
        Set the impedance from values

        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        self._set_data_array(value, "impedance")

    @property
    def impedance_error(self):
        """

        :return: DESCRIPTION
        :rtype: TYPE

        """
        if self.has_impedance():
            z_err = self.dataset.transfer_function_error.sel(
                input=self._ch_input_dict["impedance"],
                output=self._ch_output_dict["impedance"],
            )
            z_err.name = "impedance_error"

            for key, mkey in self._dataset_attr_dict.items():
                obj, attr = mkey.split(".", 1)
                value = getattr(self, obj).get_attr_from_name(attr)

                z_err.attrs[key] = value
            return z_err

    @impedance_error.setter
    def impedance_error(self, value):
        """
        Set the impedance from values

        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        self._set_data_array(value, "impedance_error")

    @property
    def impedance_model_error(self):
        """

        :return: DESCRIPTION
        :rtype: TYPE

        """
        if self.has_impedance():
            z_err = self.dataset.transfer_function_model_error.sel(
                input=self._ch_input_dict["impedance"],
                output=self._ch_output_dict["impedance"],
            )
            z_err.name = "impedance_model_error"

            for key, mkey in self._dataset_attr_dict.items():
                obj, attr = mkey.split(".", 1)
                value = getattr(self, obj).get_attr_from_name(attr)

                z_err.attrs[key] = value
            return z_err

    @impedance_model_error.setter
    def impedance_model_error(self, value):
        """
        Set the impedance model errors from values

        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        self._set_data_array(value, "impedance_model_error")

    def has_tipper(self):
        """
        Check to see if the transfer function is not 0 and has
        transfer function components

        :return: DESCRIPTION
        :rtype: TYPE

        """
        outputs = self._transfer_function.transfer_function.coords[
            "output"
        ].data.tolist()
        if self.hz in outputs:
            if np.all(
                self._transfer_function.transfer_function.sel(
                    input=self._ch_input_dict["tipper"],
                    output=self._ch_output_dict["tipper"],
                ).data
                == 0
            ):
                return False
            return True
        return False

    @property
    def tipper(self):
        """

        :return: DESCRIPTION
        :rtype: TYPE

        """
        if self.has_tipper():
            t = self.dataset.transfer_function.sel(
                input=self._ch_input_dict["tipper"],
                output=self._ch_output_dict["tipper"],
            )
            t.name = "tipper"

            for key, mkey in self._dataset_attr_dict.items():
                obj, attr = mkey.split(".", 1)
                value = getattr(self, obj).get_attr_from_name(attr)

                t.attrs[key] = value
            return t

    @tipper.setter
    def tipper(self, value):
        """

        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        self._set_data_array(value, "tipper")

    @property
    def tipper_error(self):
        """

        :return: DESCRIPTION
        :rtype: TYPE

        """
        if self.has_tipper():
            t = self.dataset.transfer_function_error.sel(
                input=self._ch_input_dict["tipper"],
                output=self._ch_output_dict["tipper"],
            )
            t.name = "tipper_error"
            for key, mkey in self._dataset_attr_dict.items():
                obj, attr = mkey.split(".", 1)
                value = getattr(self, obj).get_attr_from_name(attr)

                t.attrs[key] = value
            return t

    @tipper_error.setter
    def tipper_error(self, value):
        """

        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        self._set_data_array(value, "tipper_error")

    @property
    def tipper_model_error(self):
        """

        :return: DESCRIPTION
        :rtype: TYPE

        """
        if self.has_tipper():
            t = self.dataset.transfer_function_model_error.sel(
                input=self._ch_input_dict["tipper"],
                output=self._ch_output_dict["tipper"],
            )
            t.name = "tipper_model_error"
            for key, mkey in self._dataset_attr_dict.items():
                obj, attr = mkey.split(".", 1)
                value = getattr(self, obj).get_attr_from_name(attr)

                t.attrs[key] = value
            return t

    @tipper_model_error.setter
    def tipper_model_error(self, value):
        """

        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        self._set_data_array(value, "tipper_model_error")

    def has_inverse_signal_power(self):
        """
        Check to see if the transfer function is not 0 and has
        transfer function components

        :return: DESCRIPTION
        :rtype: TYPE

        """

        if np.all(
            self._transfer_function.inverse_signal_power.sel(
                input=self._ch_input_dict["isp"],
                output=self._ch_output_dict["isp"],
            ).data
            == 0
        ):
            return False
        return True

    @property
    def inverse_signal_power(self):
        if self.has_inverse_signal_power():
            ds = self.dataset.inverse_signal_power.sel(
                input=self._ch_input_dict["isp"],
                output=self._ch_output_dict["isp"],
            )
            for key, mkey in self._dataset_attr_dict.items():
                obj, attr = mkey.split(".", 1)
                value = getattr(self, obj).get_attr_from_name(attr)

                ds.attrs[key] = value
            return ds
        return None

    @inverse_signal_power.setter
    def inverse_signal_power(self, value):
        """
        Set the inverse signal power


        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        self._set_data_array(value, "isp")
        if self.has_residual_covariance():
            self._compute_error_from_covariance()

    def has_residual_covariance(self):
        """
        Check to see if the transfer function is not 0 and has
        transfer function components

        :return: DESCRIPTION
        :rtype: TYPE

        """

        if np.all(
            self._transfer_function.residual_covariance.sel(
                input=self._ch_input_dict["res"],
                output=self._ch_output_dict["res"],
            ).data
            == 0
        ):
            return False
        return True

    @property
    def residual_covariance(self):
        if self.has_residual_covariance():
            ds = self.dataset.residual_covariance.sel(
                input=self._ch_input_dict["res"],
                output=self._ch_output_dict["res"],
            )
            for key, mkey in self._dataset_attr_dict.items():
                obj, attr = mkey.split(".", 1)
                value = getattr(self, obj).get_attr_from_name(attr)

                ds.attrs[key] = value
            return ds
        return None

    @residual_covariance.setter
    def residual_covariance(self, value):
        """
        Set the residual covariance

        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        self._set_data_array(value, "res")
        if self.has_inverse_signal_power():
            self._compute_error_from_covariance()

    def _compute_impedance_error_from_covariance(self):
        """
        Compute transfer function errors from covariance matrices

        This will become important when writing edi files.

        Translated from code written by Ben Murphy.

        :return: DESCRIPTION
        :rtype: TYPE

        """
        sigma_e = self.residual_covariance.loc[
            dict(input=self.ex_ey, output=self.ex_ey)
        ]
        sigma_s = self.inverse_signal_power.loc[
            dict(input=self.hx_hy, output=self.hx_hy)
        ]

        z_err = np.zeros((self.period.size, 2, 2), dtype=float)
        z_err[:, 0, 0] = np.real(
            sigma_e.loc[dict(input=[self.ex], output=[self.ex])].data.flatten()
            * sigma_s.loc[
                dict(input=[self.hx], output=[self.hx])
            ].data.flatten()
        )
        z_err[:, 0, 1] = np.real(
            sigma_e.loc[dict(input=[self.ex], output=[self.ex])].data.flatten()
            * sigma_s.loc[
                dict(input=[self.hy], output=[self.hy])
            ].data.flatten()
        )
        z_err[:, 1, 0] = np.real(
            sigma_e.loc[dict(input=[self.ey], output=[self.ey])].data.flatten()
            * sigma_s.loc[
                dict(input=[self.hx], output=[self.hx])
            ].data.flatten()
        )
        z_err[:, 1, 1] = np.real(
            sigma_e.loc[dict(input=[self.ey], output=[self.ey])].data.flatten()
            * sigma_s.loc[
                dict(input=[self.hy], output=[self.hy])
            ].data.flatten()
        )

        z_err = np.sqrt(np.abs(z_err))

        self.dataset.transfer_function_error.loc[
            dict(input=self.hx_hy, output=self.ex_ey)
        ] = z_err

    def _compute_tipper_error_from_covariance(self):
        """
        Compute transfer function errors from covariance matrices

        This will become important when writing edi files.

        Translated from code written by Ben Murphy.

        :return: DESCRIPTION
        :rtype: TYPE

        """
        sigma_e = self.residual_covariance.loc[
            dict(input=[self.hz], output=[self.hz])
        ]
        sigma_s = self.inverse_signal_power.loc[
            dict(input=self.hx_hy, output=self.hx_hy)
        ]

        t_err = np.zeros((self.period.size, 1, 2), dtype=float)
        t_err[:, 0, 0] = np.real(
            sigma_e.loc[dict(input=[self.hz], output=[self.hz])].data.flatten()
            * sigma_s.loc[
                dict(input=[self.hx], output=[self.hx])
            ].data.flatten()
        )
        t_err[:, 0, 1] = np.real(
            sigma_e.loc[dict(input=[self.hz], output=[self.hz])].data.flatten()
            * sigma_s.loc[
                dict(input=[self.hy], output=[self.hy])
            ].data.flatten()
        )

        t_err = np.sqrt(np.abs(t_err))

        self.dataset.transfer_function_error.loc[
            dict(input=self.hx_hy, output=[self.hz])
        ] = t_err

    def _compute_error_from_covariance(self):
        """
        convenience method to compute errors from covariance

        :return: DESCRIPTION
        :rtype: TYPE

        """
        self._compute_impedance_error_from_covariance()
        self._compute_tipper_error_from_covariance()

    @property
    def period(self):
        return self.dataset.period.data

    @period.setter
    def period(self, value):
        if self.period is not None:
            if len(self.period) == 1 and self.period == np.array([1]):
                self._transfer_function = self._initialize_transfer_function(
                    periods=value
                )
            if len(value) != len(self.period):
                msg = "New period size %s is not the same size as old ones %s, suggest creating a new instance of TF"
                self.logger.error(msg, value.size, self.period.size)
                raise TFError(msg % (value.size, self.period.size))
            else:
                self.dataset["period"] = value
        else:
            self._transfer_function = self._initialize_transfer_function(
                periods=value
            )
        return

    @property
    def frequency(self):
        if self.period is not None:
            return 1.0 / self.period
        return None

    @frequency.setter
    def frequency(self, value):
        self.period = 1.0 / value

    @property
    def station(self):
        """station name"""
        return self.station_metadata.id

    @station.setter
    def station(self, station_name):
        """
        set station name
        """
        self.station_metadata.id = validate_name(station_name)

    @property
    def survey(self):
        """
        Survey ID
        """
        return self.survey_metadata.id

    @survey.setter
    def survey(self, survey_id):
        """
        set survey id
        """
        if survey_id is None:
            survey_id = "unkown_survey"
        self.survey_metadata.id = validate_name(survey_id)

    @property
    def tf_id(self):
        """transfer function id"""
        return self.station_metadata.transfer_function.id

    @tf_id.setter
    def tf_id(self, value):
        """set transfer function id"""
        self.station_metadata.transfer_function.id = validate_name(value)

    def to_ts_station_metadata(self):
        """
        need a convinience function to translate to ts station metadata
        for MTH5

        """

        from mt_metadata.timeseries import Station as TSStation

        ts_station_metadata = TSStation()
        for key, value in self.station_metadata.to_dict(single=True).items():
            if "transfer_function" in key:
                continue
            try:
                ts_station_metadata.set_attr_from_name(key, value)
            except AttributeError:
                continue
        return ts_station_metadata

    def from_ts_station_metadata(self, ts_station_metadata):
        """
        need a convinience function to translate to ts station metadata
        for MTH5

        """

        for key, value in ts_station_metadata.to_dict(single=True).items():
            try:
                self.station_metadata.set_attr_from_name(key, value)
            except AttributeError:
                continue

    def write_tf_file(
        self,
        fn=None,
        save_dir=None,
        fn_basename=None,
        file_type="edi",
        **kwargs,
    ):
        """
        Write an mt file, the supported file types are EDI and XML.

        .. todo:: j-files and avg files

        :param fn: full path to file to save to
        :type fn: :class:`pathlib.Path` or string

        :param save_dir: full path save directory
        :type save_dir: string

        :param fn_basename: name of file with or without extension
        :type fn_basename: string

        :param file_type: [ 'edi' | 'xml' | "zmm" ]
        :type file_type: string

        keyword arguments include

        :param longitude_format:  whether to write longitude as longitude or LONG.
                                  options are 'longitude' or 'LONG', default 'longitude'
        :type longitude_format:  string
        :param latlon_format:  format of latitude and longitude in output edi,
                               degrees minutes seconds ('dms') or decimal
                               degrees ('dd')
        :type latlon_format:  string

        :returns: full path to file
        :rtype: string

        :Example: ::

            >>> tf_obj.write_mtf_file(file_type='xml')

        """

        if fn is not None:
            new_fn = Path(fn)
            self.save_dir = new_fn.parent
            fn_basename = new_fn.name
            file_type = new_fn.suffix.lower()[1:]
            if file_type in ["xml"]:
                file_type = "emtfxml"
        if save_dir is not None:
            self.save_dir = Path(save_dir)
        if fn_basename is not None:
            fn_basename = Path(fn_basename)
            if fn_basename.suffix in ["", None]:
                fn_basename = fn_basename.with_name(
                    f"{fn_basename.name}.{file_type}"
                )
        if fn_basename is None:
            fn_basename = Path(f"{self.station}.{file_type}")
        if file_type is None:
            file_type = fn_basename.suffix.lower()[1:]
        if file_type == "xml":
            file_type = "emtfxml"
        if file_type not in ["edi", "emtfxml", "j", "zmm", "zrr", "zss"]:
            msg = f"File type {file_type} not supported yet."
            self.logger.error(msg)
            raise TFError(msg)
        fn = self.save_dir.joinpath(fn_basename)

        return write_file(self, fn, file_type=file_type, **kwargs)

    def read_tf_file(self, fn=None, file_type=None, **kwargs):
        """

        Read an TF response file.

        .. note:: Currently only .edi, .xml, .j, .zmm/rr/ss, .avg
           files are supported

        :param fn: full path to input file
        :type fn: string

        :param file_type: ['edi' | 'j' | 'xml' | 'avg' | 'zmm' | 'zrr' | 'zss' | ... ]
                          if None, automatically detects file type by
                          the extension.
        :type file_type: string

        :Example: ::

            >>> import mt_metadata.transfer_functions.core import TF
            >>> tf_obj = TF()
            >>> tf_obj.read_tf_file(fn=r"/home/mt/mt01.xml")

        """
        if fn is not None:
            self.fn = fn

        tf_obj = read_file(self.fn, file_type=file_type, **kwargs)
        if tf_obj.station_metadata.transfer_function.id is None:
            tf_obj.station_metadata.transfer_function.id = (
                tf_obj.station_metadata.id
            )
        self.__dict__.update(tf_obj.__dict__)
        self.save_dir = self.fn.parent


# ==============================================================================
#             Error
# ==============================================================================


class TFError(Exception):
    pass
