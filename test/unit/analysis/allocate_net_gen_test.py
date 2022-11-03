"""Unit tests for allocation of net generation."""

from typing import Literal

import numpy as np
import pandas as pd
import pytest

from pudl.analysis import allocate_net_gen
from pudl.metadata.fields import apply_pudl_dtypes

# Reusable input files...

# inputs for example 1:
#  multi-generator-plant with one primary fuel type that fully reports to the
#  generation_eia923 table
GEN_1 = pd.DataFrame(
    {
        "plant_id_eia": [50307, 50307, 50307, 50307],
        "generator_id": ["GEN1", "GEN2", "GEN3", "GEN4"],
        "report_date": [
            "2018-01-01",
            "2018-01-01",
            "2018-01-01",
            "2018-01-01",
        ],
        "net_generation_mwh": [14.0, 1.0, 0.0, 0.0],
    }
).pipe(apply_pudl_dtypes, group="eia")

GF_1 = pd.DataFrame(
    {
        "plant_id_eia": [50307, 50307, 50307, 50307],
        "prime_mover_code": ["ST", "IC", "IC", "ST"],
        "fuel_type": ["NG", "DFO", "RFO", "RFO"],
        "report_date": [
            "2018-01-01",
            "2018-01-01",
            "2018-01-01",
            "2018-01-01",
        ],
        "net_generation_mwh": [15.0, 0.0, np.nan, np.nan],
        "fuel_consumed_mmbtu": [100000.0, 0.0, np.nan, np.nan],
    }
).pipe(apply_pudl_dtypes, group="eia")

GENS_1 = pd.DataFrame(
    {
        "plant_id_eia": [50307, 50307, 50307, 50307, 50307],
        "generator_id": ["GEN1", "GEN2", "GEN3", "GEN4", "GEN5"],
        "report_date": [
            "2018-01-01",
            "2018-01-01",
            "2018-01-01",
            "2018-01-01",
            "2018-01-01",
        ],
        "prime_mover_code": ["ST", "ST", "ST", "ST", "IC"],
        "capacity_mw": [7.5, 2.5, 2.5, 4.3, 1.8],
        "fuel_type_count": [2, 2, 2, 2, 2],
        "retirement_date": [pd.NA, pd.NA, "2069-10-31", pd.NA, pd.NA],
        "operational_status": [
            "existing",
            "existing",
            "existing",
            "existing",
            "existing",
        ],
        "energy_source_code_1": ["NG", "NG", "NG", "NG", "DFO"],
        "energy_source_code_2": [pd.NA, pd.NA, pd.NA, pd.NA, pd.NA],
        "energy_source_code_3": [pd.NA, pd.NA, pd.NA, pd.NA, pd.NA],
        "energy_source_code_4": [pd.NA, pd.NA, pd.NA, pd.NA, pd.NA],
        "energy_source_code_5": [pd.NA, pd.NA, pd.NA, pd.NA, pd.NA],
        "energy_source_code_6": [pd.NA, pd.NA, pd.NA, pd.NA, pd.NA],
        "planned_energy_source_code_1": [pd.NA, pd.NA, pd.NA, pd.NA, pd.NA],
    }
).pipe(apply_pudl_dtypes, group="eia")


BF_1 = pd.DataFrame(
    {
        "plant_id_eia": [
            41,
            41,
            41,
            41,
            41,
            41,
            41,
            41,
            41,
            41,
            41,
            41,
            41,
            41,
            41,
            41,
            41,
            41,
            41,
            41,
            41,
            41,
            41,
            41,
            200,
            200,
            200,
            200,
            200,
            200,
            200,
            200,
            200,
            200,
            200,
            200,
            200,
            200,
            200,
            200,
            200,
            200,
            200,
            200,
            200,
            200,
            200,
            200,
        ],
        "report_date": [
            "2021-01-01",
            "2021-02-01",
            "2021-03-01",
            "2021-04-01",
            "2021-05-01",
            "2021-06-01",
            "2021-07-01",
            "2021-08-01",
            "2021-09-01",
            "2021-10-01",
            "2021-11-01",
            "2021-12-01",
            "2020-01-01",
            "2020-02-01",
            "2020-03-01",
            "2020-04-01",
            "2020-05-01",
            "2020-06-01",
            "2020-07-01",
            "2020-08-01",
            "2020-09-01",
            "2020-10-01",
            "2020-11-01",
            "2020-12-01",
            "2021-01-01",
            "2021-02-01",
            "2021-03-01",
            "2021-04-01",
            "2021-05-01",
            "2021-06-01",
            "2021-07-01",
            "2021-08-01",
            "2021-09-01",
            "2021-10-01",
            "2021-11-01",
            "2021-12-01",
            "2020-01-01",
            "2020-02-01",
            "2020-03-01",
            "2020-04-01",
            "2020-05-01",
            "2020-06-01",
            "2020-07-01",
            "2020-08-01",
            "2020-09-01",
            "2020-10-01",
            "2020-11-01",
            "2020-12-01",
        ],
        "boiler_id": [
            "a",
            "a",
            "a",
            "a",
            "a",
            "a",
            "a",
            "a",
            "a",
            "a",
            "a",
            "a",
            "a",
            "a",
            "a",
            "a",
            "a",
            "a",
            "a",
            "a",
            "a",
            "a",
            "a",
            "a",
            "B1",
            "B1",
            "B1",
            "B1",
            "B1",
            "B1",
            "B1",
            "B1",
            "B1",
            "B1",
            "B1",
            "B1",
            "B1",  #
            "B1",
            "B1",
            "B1",
            "B1",
            "B1",
            "B1",
            "B1",
            "B1",
            "B1",
            "B1",
            "B1",
        ],
        "energy_source_code": [
            "gas",
            "gas",
            "gas",
            "gas",
            "gas",
            "gas",
            "gas",
            "gas",
            "gas",
            "gas",
            "gas",
            "gas",
            "gas",
            "gas",
            "gas",
            "gas",
            "gas",
            "gas",
            "gas",
            "gas",
            "gas",
            "gas",
            "gas",
            "gas",
            "coal",
            "coal",
            "coal",
            "coal",
            "coal",
            "coal",
            "coal",
            "coal",
            "coal",
            "coal",
            "coal",
            "coal",
            "coal",
            "coal",
            "coal",
            "coal",
            "coal",
            "coal",
            "coal",
            "coal",
            "coal",
            "coal",
            "coal",
            "coal",
        ],
        "prime_mover_code": [
            "GT",
            "GT",
            "GT",
            "GT",
            "GT",
            "GT",
            "GT",
            "GT",
            "GT",
            "GT",
            "GT",
            "GT",
            "GT",
            "GT",
            "GT",
            "GT",
            "GT",
            "GT",
            "GT",
            "GT",
            "GT",
            "GT",
            "GT",
            "GT",
            "ST",
            "ST",
            "ST",
            "ST",
            "ST",
            "ST",
            "ST",
            "ST",
            "ST",
            "ST",
            "ST",
            "ST",
            "ST",
            "ST",
            "ST",
            "ST",
            "ST",
            "ST",
            "ST",
            "ST",
            "ST",
            "ST",
            "ST",
            "ST",
        ],
        "fuel_consumed_mmbtu": [
            1,
            2,
            3,
            4,
            5,
            6,
            6,
            5,
            4,
            3,
            2,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            7,
            6,
            5,
            4,
            3,
            2,
            22222,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            20202,
        ],
    }
).pipe(apply_pudl_dtypes, group="eia")


def test_distribute_annually_reported_data_to_months_if_annual():
    """Test :func:`distribute_annually_reported_data_to_months_if_annual`."""
    out = allocate_net_gen.distribute_annually_reported_data_to_months_if_annual(
        df=BF_1,
        key_columns=allocate_net_gen.IDX_B_PM_ESC,
        data_column_name="fuel_consumed_mmbtu",
        freq="MS",
    )
    expected = pd.DataFrame(
        {
            "plant_id_eia": [
                41,
                41,
                41,
                41,
                41,
                41,
                41,
                41,
                41,
                41,
                41,
                41,
                41,
                41,
                41,
                41,
                41,
                41,
                41,
                41,
                41,
                41,
                41,
                41,
                200,
                200,
                200,
                200,
                200,
                200,
                200,
                200,
                200,
                200,
                200,
                200,
                200,
                200,
                200,
                200,
                200,
                200,
                200,
                200,
                200,
                200,
                200,
                200,
            ],
            "report_date": [
                "2021-01-01",
                "2021-02-01",
                "2021-03-01",
                "2021-04-01",
                "2021-05-01",
                "2021-06-01",
                "2021-07-01",
                "2021-08-01",
                "2021-09-01",
                "2021-10-01",
                "2021-11-01",
                "2021-12-01",
                "2020-01-01",
                "2020-02-01",
                "2020-03-01",
                "2020-04-01",
                "2020-05-01",
                "2020-06-01",
                "2020-07-01",
                "2020-08-01",
                "2020-09-01",
                "2020-10-01",
                "2020-11-01",
                "2020-12-01",
                "2021-01-01",
                "2021-02-01",
                "2021-03-01",
                "2021-04-01",
                "2021-05-01",
                "2021-06-01",
                "2021-07-01",
                "2021-08-01",
                "2021-09-01",
                "2021-10-01",
                "2021-11-01",
                "2021-12-01",
                "2020-01-01",
                "2020-02-01",
                "2020-03-01",
                "2020-04-01",
                "2020-05-01",
                "2020-06-01",
                "2020-07-01",
                "2020-08-01",
                "2020-09-01",
                "2020-10-01",
                "2020-11-01",
                "2020-12-01",
            ],
            "boiler_id": [
                "a",
                "a",
                "a",
                "a",
                "a",
                "a",
                "a",
                "a",
                "a",
                "a",
                "a",
                "a",
                "a",
                "a",
                "a",
                "a",
                "a",
                "a",
                "a",
                "a",
                "a",
                "a",
                "a",
                "a",
                "B1",
                "B1",
                "B1",
                "B1",
                "B1",
                "B1",
                "B1",
                "B1",
                "B1",
                "B1",
                "B1",
                "B1",
                "B1",
                "B1",
                "B1",
                "B1",
                "B1",
                "B1",
                "B1",
                "B1",
                "B1",
                "B1",
                "B1",
                "B1",
            ],
            "energy_source_code": [
                "gas",
                "gas",
                "gas",
                "gas",
                "gas",
                "gas",
                "gas",
                "gas",
                "gas",
                "gas",
                "gas",
                "gas",
                "gas",
                "gas",
                "gas",
                "gas",
                "gas",
                "gas",
                "gas",
                "gas",
                "gas",
                "gas",
                "gas",
                "gas",
                "coal",
                "coal",
                "coal",
                "coal",
                "coal",
                "coal",
                "coal",
                "coal",
                "coal",
                "coal",
                "coal",
                "coal",
                "coal",
                "coal",
                "coal",
                "coal",
                "coal",
                "coal",
                "coal",
                "coal",
                "coal",
                "coal",
                "coal",
                "coal",
            ],
            "prime_mover_code": [
                "GT",
                "GT",
                "GT",
                "GT",
                "GT",
                "GT",
                "GT",
                "GT",
                "GT",
                "GT",
                "GT",
                "GT",
                "GT",
                "GT",
                "GT",
                "GT",
                "GT",
                "GT",
                "GT",
                "GT",
                "GT",
                "GT",
                "GT",
                "GT",
                "ST",
                "ST",
                "ST",
                "ST",
                "ST",
                "ST",
                "ST",
                "ST",
                "ST",
                "ST",
                "ST",
                "ST",
                "ST",
                "ST",
                "ST",
                "ST",
                "ST",
                "ST",
                "ST",
                "ST",
                "ST",
                "ST",
                "ST",
                "ST",
            ],
            "fuel_consumed_mmbtu": [
                1,
                2,
                3,
                4,
                5,
                6,
                6,
                5,
                4,
                3,
                2,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                7,
                6,
                5,
                4,
                3,
                2,
                22222 / 12,
                22222 / 12,
                22222 / 12,
                22222 / 12,
                22222 / 12,
                22222 / 12,
                22222 / 12,
                22222 / 12,
                22222 / 12,
                22222 / 12,
                22222 / 12,
                22222 / 12,
                20202 / 12,
                20202 / 12,
                20202 / 12,
                20202 / 12,
                20202 / 12,
                20202 / 12,
                20202 / 12,
                20202 / 12,
                20202 / 12,
                20202 / 12,
                20202 / 12,
                20202 / 12,
            ],
        }
    )
    out = out.sort_values(["plant_id_eia", "report_date"]).reset_index(drop=True)
    expected = (
        expected.sort_values(["plant_id_eia", "report_date"])[out.columns]
        .pipe(apply_pudl_dtypes, group="eia")
        .reset_index(drop=True)
    )
    pd.testing.assert_frame_equal(out, expected, check_like=True)


class PudlTablMock:
    """Mock ``pudl_out`` object."""

    freq: Literal["AS", "MS"]

    def gens_eia860():
        """Access to generators_eia860 table."""
        return GENS_1

    def gen_eia923():
        """Access to generation_eia923 table."""
        return GEN_1

    def gf_eia923():
        """Access to generation_fuel_eia923 table."""
        return GF_1

    def plants_eia860():
        """Access to plants_eia860 table."""
        return  # PLANTS_1

    def bf_eia923():
        """Access to boiler_fuel_eia923 table."""
        return  # BF_1

    def bga_eia860():
        """Access to boiler_generators_assn_eia860 table."""
        return  # BGA_1


@pytest.mark.xfail(
    reason="Tests need to be updated. See https://github.com/catalyst-cooperative/pudl/issues/1371"
)
def test_associate_generator_tables_1():
    """Test associate_generator_tables function with example 1."""
    gen_assoc_1_expected = pd.DataFrame(
        {
            "plant_id_eia": [50307, 50307, 50307, 50307, 50307, 50307, 50307],
            "generator_id": ["GEN1", "GEN2", "GEN3", "GEN4", "GEN5", np.nan, np.nan],
            "report_date": [
                "2018-01-01",
                "2018-01-01",
                "2018-01-01",
                "2018-01-01",
                "2018-01-01",
                "2018-01-01",
                "2018-01-01",
            ],
            "prime_mover_code": ["ST", "ST", "ST", "ST", "IC", "IC", "ST"],
            "capacity_mw": [7.5, 2.5, 2.5, 4.3, 1.8, np.nan, np.nan],
            "fuel_type_count": [2.0, 2.0, 2.0, 2.0, 2.0, np.nan, np.nan],
            "energy_source_code_num": [
                "energy_source_code_1",
                "energy_source_code_1",
                "energy_source_code_1",
                "energy_source_code_1",
                "energy_source_code_1",
                np.nan,
                np.nan,
            ],
            "fuel_type": ["NG", "NG", "NG", "NG", "DFO", "RFO", "RFO"],
            "net_generation_mwh_g_tbl": [14.0, 1.0, 0.0, 0.0, np.nan, np.nan, np.nan],
            "net_generation_mwh_gf_tbl": [15.0, 15.0, 15.0, 15.0, 0.0, np.nan, np.nan],
            "fuel_consumed_mmbtu": [
                100000.0,
                100000.0,
                100000.0,
                100000.0,
                0.0,
                np.nan,
                np.nan,
            ],
            "capacity_mw_fuel": [16.8, 16.8, 16.8, 16.8, 1.8, np.nan, np.nan],
            "net_generation_mwh_g_tbl_fuel": [
                15.0,
                15.0,
                15.0,
                15.0,
                np.nan,
                np.nan,
                np.nan,
            ],
        }
    ).pipe(apply_pudl_dtypes, group="eia")

    gen_assoc_1_actual = allocate_net_gen.associate_generator_tables(
        gf=GF_1, gen=GEN_1, gens=GENS_1
    ).pipe(apply_pudl_dtypes, group="eia")

    pd.testing.assert_frame_equal(gen_assoc_1_expected, gen_assoc_1_actual)


@pytest.mark.xfail(
    reason="Tests need to be updated. See https://github.com/catalyst-cooperative/pudl/issues/1371"
)
def test_allocate_gen_fuel_by_gen_pm_fuel_1():
    """Test allocate_gen_fuel_by_gen_pm_fuel function with example 1."""
    gen_pm_fuel_1_expected = pd.DataFrame(
        {
            "plant_id_eia": [50307, 50307, 50307, 50307, 50307],
            "prime_mover_code": ["ST", "ST", "ST", "ST", "IC"],
            "fuel_type": ["NG", "NG", "NG", "NG", "DFO"],
            "report_date": [
                "2018-01-01",
                "2018-01-01",
                "2018-01-01",
                "2018-01-01",
                "2018-01-01",
            ],
            "generator_id": ["GEN1", "GEN2", "GEN3", "GEN4", "GEN5"],
            "frac": [0.93, 0.066, 0.0, 0.0, 1.0],
            "net_generation_mwh_gf_tbl": [15.0, 15.0, 15.0, 15.0, 0.0],
            "net_generation_mwh_g_tbl": [14.0, 1.0, 0.0, 0.0, 0.0],
            "capacity_mw": [7.5, 2.5, 2.5, 4.3, 1.8],
            "fuel_consumed_mmbtu": [93333.33, 6666.66, 0.0, 0.0, 0.0],
            "net_generation_mwh": [14.0, 1.0, 0.0, 0.0, 0.0],
            "fuel_consumed_mmbtu_gf_tbl": [100000.0, 100000.0, 100000.0, 100000.0, 0.0],
        }
    ).pipe(apply_pudl_dtypes, group="eia")

    gen_pm_fuel_1_actual = (
        allocate_net_gen.allocate_gen_fuel_by_generator_energy_source(
            pudl_out=PudlTablMock(), drop_interim_cols=True
        )
    )

    pd.testing.assert_frame_equal(gen_pm_fuel_1_expected, gen_pm_fuel_1_actual)

    # gen_pm_fuel_1_expected is an inputs into agg_by_generator().. so should I
    # test this here??
    #
    # testing the aggregation to the generator level for example 1.
    # in this case, each generator has one prime mover and one fuel source so
    # they are effectively the same.
    gen_out_1_expected = pd.DataFrame(
        {
            "plant_id_eia": [50307, 50307, 50307, 50307, 50307],
            "generator_id": ["GEN1", "GEN2", "GEN3", "GEN4", "GEN5"],
            "report_date": [
                "2018-01-01",
                "2018-01-01",
                "2018-01-01",
                "2018-01-01",
                "2018-01-01",
            ],
            "net_generation_mwh": [14.0, 1.0, 0.0, 0.0, 0.0],
            "fuel_consumed_mmbtu": [93333.33, 6666.66, 0.0, 0.0, 0.0],
        }
    ).pipe(apply_pudl_dtypes, group="eia")
    gen_out_1_actual = allocate_net_gen.agg_by_generator(gen_pm_fuel_1_actual)
    pd.testing.assert_frame_equal(gen_out_1_expected, gen_out_1_actual)
