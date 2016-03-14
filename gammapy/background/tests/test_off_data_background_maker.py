# Licensed under a 3-clause BSD style license - see LICENSE.rst
from astropy.table import Table
from ..models import CubeBackgroundModel
from ..models import EnergyOffsetBackgroundModel
from ...data import ObservationTable
from ...data import DataStore
from ..off_data_background_maker import OffDataBackgroundMaker


def test_background_model(tmpdir):
    data_store = DataStore.from_dir('$GAMMAPY_EXTRA/datasets/hess-crab4-hd-hap-prod2/')
    out_dir = tmpdir
    bgmaker = OffDataBackgroundMaker(data_store, out_dir)

    selection = "debug"
    bgmaker.select_observations(selection)
    table = Table.read('run.lis', format='ascii.csv')
    assert table['OBS_ID'][1] == 23526

    bgmaker.group_observations()

    table = ObservationTable.read(str(tmpdir / 'obs.ecsv'), format='ascii.ecsv')
    assert list(table['GROUP_ID']) == [0, 0, 0, 1]
    table = ObservationTable.read(str(tmpdir / 'group-def.ecsv'), format='ascii.ecsv')
    assert list(table['ZEN_PNT_MAX']) == [49, 90]

    bgmaker.make_model("3D")
    bgmaker.save_models("3D")
    model = CubeBackgroundModel.read(str(tmpdir / 'background_3D_group_001_table.fits.gz'))
    assert model.counts_cube.data.sum() == 1527

    bgmaker.make_model("2D")
    bgmaker.save_models("2D")
    model = EnergyOffsetBackgroundModel.read(str(tmpdir / 'background_2D_group_001_table.fits.gz'))
    assert model.counts.data.value.sum() == 1398