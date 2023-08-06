# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 17:03:51 2021

@author: jpeacock
"""

# =============================================================================
#
# =============================================================================
import unittest

from collections import OrderedDict
from mt_metadata.transfer_functions.io import edi
from mt_metadata.utils.mttime import MTime
from mt_metadata import TF_EDI_CGG

# =============================================================================
# CGG
# =============================================================================
class TestCGGEDI(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.edi_obj = edi.EDI(fn=TF_EDI_CGG)
        self.maxDiff = None

    def test_header(self):
        head = {
            "ACQBY": "GSC_CGG",
            "COORDINATE_SYSTEM": "geographic",
            "DATAID": "TEST01",
            "DATUM": "WGS84",
            "ELEV": 175.270,
            "EMPTY": 1.000000e32,
            "FILEBY": None,
            "LAT": -30.930285,
            "LOC": "Australia",
            "LON": 127.22923,
        }

        for key, value in head.items():
            with self.subTest(key):
                h_value = getattr(self.edi_obj.Header, key.lower())
                self.assertEqual(h_value, value)

        with self.subTest("acquire date"):
            self.assertEqual(self.edi_obj.Header._acqdate, MTime("06/05/14"))

        with self.subTest("units"):
            self.assertNotEqual(
                self.edi_obj.Header.units,
                "millivolts_per_kilometer_per_nanotesla",
            )

    def test_info(self):
        info_list = sorted(
            [
                "SITE INFO:",
                "H_SITE=E_SITE",
                "PROCESSING PARAMETERS:",
            ]
        )

        self.assertListEqual(info_list, self.edi_obj.Info.info_list)

    def test_measurement_ex(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
                ("azm", 0.0),
                ("chtype", "EX"),
                ("id", 1004.001),
                ("x", 0.0),
                ("x2", 0.0),
                ("y", 0.0),
                ("y2", 0.0),
                ("z", 0.0),
                ("z2", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.meas_ex.to_dict(single=True)
        )

    def test_measurement_ey(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
                ("azm", 0.0),
                ("chtype", "EY"),
                ("id", 1005.001),
                ("x", 0.0),
                ("x2", 0.0),
                ("y", 0.0),
                ("y2", 0.0),
                ("z", 0.0),
                ("z2", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.meas_ey.to_dict(single=True)
        )

    def test_measurement_hx(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
                ("azm", 0.0),
                ("chtype", "HX"),
                ("dip", 0.0),
                ("id", 1001.001),
                ("x", 0.0),
                ("y", 0.0),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.meas_hx.to_dict(single=True)
        )

    def test_measurement_hy(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
                ("azm", 90.0),
                ("chtype", "HY"),
                ("dip", 0.0),
                ("id", 1002.001),
                ("x", 0.0),
                ("y", 0.0),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.meas_hy.to_dict(single=True)
        )

    def test_measurement_hz(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
                ("azm", 0.0),
                ("chtype", "HZ"),
                ("dip", 0.0),
                ("id", 1003.001),
                ("x", 0.0),
                ("y", 0.0),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.meas_hz.to_dict(single=True)
        )

    def test_measurement_rrhx(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
                ("azm", 0.0),
                ("chtype", "RRHX"),
                ("dip", 0.0),
                ("id", 1006.001),
                ("x", 0.0),
                ("y", 0.0),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.meas_rrhx.to_dict(single=True)
        )

    def test_measurement_rrhy(self):
        ch = OrderedDict(
            [
                ("acqchan", None),
                ("azm", 90.0),
                ("chtype", "RRHY"),
                ("dip", 0.0),
                ("id", 1007.001),
                ("x", 0.0),
                ("y", 0.0),
                ("z", 0.0),
            ]
        )

        self.assertDictEqual(
            ch, self.edi_obj.Measurement.meas_rrhy.to_dict(single=True)
        )

    def test_measurement(self):
        m_list = [
            'REFLOC="EGC022"',
            "REFLAT=-30:55:49.026",
            "REFLONG=+127:13:45.228",
            "REFELEV=175.27",
            "UNITS=M",
        ]

        self.assertListEqual(
            m_list, self.edi_obj.Measurement.measurement_list[0 : len(m_list)]
        )

        with self.subTest("reflat"):
            self.assertAlmostEqual(
                -30.930285, self.edi_obj.Measurement.reflat, 5
            )

        with self.subTest("reflon"):
            self.assertAlmostEqual(
                127.22923, self.edi_obj.Measurement.reflon, 5
            )

        with self.subTest("reflong"):
            self.assertAlmostEqual(
                127.22923, self.edi_obj.Measurement.reflong, 5
            )

        with self.subTest("refelev"):
            self.assertAlmostEqual(175.27, self.edi_obj.Measurement.refelev, 2)

    def test_data_section(self):
        d_list = ["NFREQ=73"]

        self.assertListEqual(d_list, self.edi_obj.Data.data_list)

    def test_impedance(self):
        with self.subTest("shape"):
            self.assertTupleEqual(self.edi_obj.z.shape, (73, 2, 2))

        with self.subTest("err shape"):
            self.assertTupleEqual(self.edi_obj.z_err.shape, (73, 2, 2))

        with self.subTest("has zero"):
            self.assertEqual(self.edi_obj.z[0, 0, 0], 0 + 0j)

        with self.subTest("not zero"):
            self.assertNotEqual(self.edi_obj.z[1, 0, 0], 0 + 0j)

    def test_tipper(self):
        with self.subTest("shape"):
            self.assertTupleEqual(self.edi_obj.t.shape, (73, 1, 2))
        with self.subTest("err shape"):
            self.assertTupleEqual(self.edi_obj.t_err.shape, (73, 1, 2))

    def test_rotation_angle(self):
        with self.subTest("all zeros"):
            self.assertTrue((self.edi_obj.rotation_angle == 0).all())

        with self.subTest("shape"):
            self.assertTupleEqual(self.edi_obj.rotation_angle.shape, (73,))


# =============================================================================
# run
# =============================================================================
if __name__ == "__main__":
    unittest.main()
