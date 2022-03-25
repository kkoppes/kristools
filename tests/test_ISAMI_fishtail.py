# test for ISAMI fishtail class

import math
import numpy as np
import pytest

from pagstresstools.ISAMI.fishtail_reader import fishtail, fastener_system, material_system

# test for fishtail class
def test_fishtail_class():
    """ test fishtail class """
    # test for fishtail class init
    fishtail_test = fishtail('./tests/test_fishtails/ISAMI_fishtail_tests.xlsx')
    assert fishtail_test.__Class_Name__ == "fishtail"
    assert fishtail_test.__lib_name__ == "ISAMI_lib"
    assert fishtail_test.__version__ == "0.1"
    assert fishtail_test.__author__ == "K.Koppes"
    assert fishtail_test.__c_msg__ == "fishtail 0.1 K.Koppes"
    assert fishtail_test.__l_msg__ == "fishtail 0.1 K.Koppes ISAMI_lib 0.1"
    assert fishtail_test.file_name == "./tests/test_fishtails/ISAMI_fishtail_tests.xlsx"
    assert list(fishtail_test.data.keys()) == ['fishtail_1', 'fishtail_2', 'fishtail_3']
    assert fishtail_test.fishtail_sheet_names == ['fishtail_1', 'fishtail_2', 'fishtail_3']
    assert fishtail_test.fishtail_sheets['fishtail_1'].shape == (3, 2)
    assert fishtail_test.fishtail_sheets['fishtail_2'].shape == (3, 2)
    assert fishtail_test.fishtail_sheets['fishtail_3'].shape == (3, 2)
    assert fishtail_test.fishtail_sheets['fishtail_1'].iloc[0,0] == 'A2'
    assert fishtail_test.fishtail_sheets['fishtail_1'].iloc[0,1] == 'B2'
    assert fishtail_test.fishtail_sheets['fishtail_1'].iloc[1,0] == 'A3'
    assert fishtail_test.fishtail_sheets['fishtail_1'].iloc[1,1] == 'B3'
    assert fishtail_test.fishtail_sheets['fishtail_1'].iloc[2,0] == 'A4'

    # test for fishtail class fastener_system_table
    fishtail_test_fast = fishtail('./tests/test_fishtails/FS_test_1.xlsx')
    assert fishtail_test_fast.__Class_Name__ == "fishtail"
    assert fishtail_test_fast.fastener_system_table.shape == (23, 4)
    assert fishtail_test_fast.fastener_system_table.iloc[0,0] == 'System_1'
    assert fishtail_test_fast.fastener_system_table.iloc[0,1] == 'pin_1'
    assert math.isnan(fishtail_test_fast.fastener_system_table.iloc[0,2])
    assert fishtail_test_fast.fastener_system_table.iloc[0,3] == 3.96
    assert fishtail_test_fast.fastener_system_table.iloc[2,2] == 'nut_1'
    assert fishtail_test_fast.fastener_system_table.iloc[5,0] == 'System_6'
    
    assert fishtail_test_fast.get_fastener_system('System_1').name == 'System_1'
    assert fishtail_test_fast.get_fastener_system('System_1').pin == 'pin_1'
    assert fishtail_test_fast.get_fastener_system('System_3').nutcollar == 'nut_1' 
    assert fishtail_test_fast.get_fastener_system('System_1').diameter == 3.96 
    
    # test for put_fastener
    fishtail_test_fast.put_fastener(fastener_system('System_28', 'pin_28', 'nut_28', 22.22))
    assert fishtail_test_fast.get_fastener_system('System_1').name == 'System_1'
    assert fishtail_test_fast.get_fastener_system('System_28').name == 'System_28'
    assert fishtail_test_fast.get_fastener_system('System_28').pin == 'pin_28'
    assert fishtail_test_fast.get_fastener_system('System_28').nutcollar == 'nut_28'
    assert fishtail_test_fast.get_fastener_system('System_28').diameter == 22.22

    # test for pop_fastener
    fishtail_test_fast.pop_fastener('System_28')
    assert fishtail_test_fast.get_fastener_system('System_1').name == 'System_1'
    assert fishtail_test_fast.get_fastener_system('System_28') == None

    # test for get_fastener_system_list
    assert fishtail_test_fast.get_fastener_system_list()[:7] == ['System_1', 'System_2', 'System_3', 'System_4', 'System_5', 'System_6', 'System_7']

    # test dict to dataframe
    # add a fastener system
    fishtail_test_fast.put_fastener(fastener_system('System_28', 'pin_28', 'nut_28', 22.22))
    assert fishtail_test_fast.get_fastener_system('System_28').name == 'System_28'
    assert fishtail_test_fast.fastener_system_table.iloc[-1,0] == 'System_28'
    assert fishtail_test_fast.fastener_system_table.iloc[-1,1] == 'pin_28'
    assert fishtail_test_fast.fastener_system_table.iloc[-1,2] == 'nut_28'

    # test for material_system_table
    fishtail_test_mat = fishtail('./tests/test_fishtails/MAT_test_1.xlsx')
    assert fishtail_test_mat.material_system_table.shape == (21, 4)
    assert fishtail_test_mat.material_system_table.iloc[0,0] == 'mat_label_1'
    assert fishtail_test_mat.material_system_table.iloc[0,1] == 'Referenced'
    assert fishtail_test_mat.material_system_table.iloc[0,2] == 'mat_name_1'
    assert fishtail_test_mat.material_system_table.iloc[0,3] == 'spec_1'
    assert fishtail_test_mat.material_system_table.iloc[1,0] == 'mat_label_2'

    assert fishtail_test_mat.get_material_system('mat_label_1').name == 'mat_label_1'
    assert fishtail_test_mat.get_material_system('mat_label_1').spec == 'spec_1'
    assert fishtail_test_mat.get_material_system('mat_label_1').library == 'Referenced'
    assert fishtail_test_mat.get_material_system('mat_label_1').mat_name == 'mat_name_1'

    # test for put_material
    fishtail_test_mat.put_material(material_system('mat_label_28', 'Referenced', 'mat_name_28', 'spec_28'))
    assert fishtail_test_mat.get_material_system('mat_label_28').name == 'mat_label_28'
    assert fishtail_test_mat.material_system_table.iloc[-1,0] == 'mat_label_28'
    assert fishtail_test_mat.material_system_table.iloc[-1,1] == 'Referenced'
    assert fishtail_test_mat.material_system_table.iloc[-1,2] == 'mat_name_28'
    assert fishtail_test_mat.material_system_table.iloc[-1,3] == 'spec_28'

    # test for pop_material
    fishtail_test_mat.pop_material('mat_label_28')
    assert fishtail_test_mat.get_material_system('mat_label_28') == None
    assert fishtail_test_mat.material_system_table.iloc[-1,0] == 'mat_label_28'
    assert fishtail_test_mat.material_system_table.iloc[-1,1] == 'Referenced'
    assert fishtail_test_mat.material_system_table.iloc[-1,2] == 'mat_name_28'
    assert fishtail_test_mat.material_system_table.iloc[-1,3] == 'spec_28'

    # test for get_material_system_list
    assert fishtail_test_mat.get_material_system_list()[:7] == ['mat_label_1', 'mat_label_2', 'mat_label_3', 'mat_label_4', 'mat_label_5', 'mat_label_6', 'mat_label_7']


    