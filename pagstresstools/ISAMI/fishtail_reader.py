# ISAMI fishtal reader
import sys
import pandas as pd
import os
import time


class fastener_system(object):
    """fastener system class"""

    __Class_Name__ = "fastener system"
    __lib_name__ = "ISAMI_lib"

    def __init__(self, name, pin, nutcollar, diameter):
        self.name = str(name)
        self.pin = str(pin)
        self.nutcollar = str(nutcollar)
        self.diameter = float(diameter)

    def __repr__(self) -> str:
        rep = f"{self.__Class_Name__}({self.name}, {self.pin}, {self.nutcollar}, {self.diameter})"
        return rep


class fishtail(object):
    """read fishtail data from excel file"""

    __Class_Name__ = "fishtail"
    __lib_name__ = "ISAMI_lib"
    __version__ = "0.1"
    __author__ = "K.Koppes"
    __c_msg__ = __Class_Name__ + " " + __version__ + " " + __author__
    __l_msg__ = __c_msg__ + " " + __lib_name__ + " " + __version__

    def __init__(self, file_name=None):

        self.file_name = file_name
        # Metadata
        # TODDO: MSN, analysis, date, time, user, loadloop?
        self.fastener_system_table = None
        self.fastener_system_dict = {}
               

        # check if file exists

        if not self.file_name:
            # no file name given
            print("No file name given")
        else:
            # read info from excel file
            if not file_name.endswith(".xlsx"):
                print("ERROR: file type not supported")
                sys.exit()
            if not os.path.isfile(file_name):
                print("ERROR: file does not exist")
                sys.exit()
            # read fishtail data
            # time the read funtion
            start_time = time.time()
            self.read_fishtail()
            print(
                "INFO: read fishtail data from excel file in %s seconds"
                % (time.time() - start_time)
            )
            self.fishtail_sheets = {}
            for sheet in self.fishtail_sheet_names:
                self.fishtail_sheets[sheet] = self.data[sheet]
            self.fishtail_sheet_names = list(self.fishtail_sheets.keys())
            self.fishtail_sheet_names.sort()
            self.fishtail_sheet_names.sort(key=len)
            self.fishtail_sheet_names.sort(key=str.lower)
            self.fishtail_sheet_names.sort(key=str.upper)

            if "FastenerSystem Table" in self.fishtail_sheet_names:
                self.make_fastener_system_table_from_file()
                self.make_fastener_system_dict_from_table()

    def read_fishtail(self):
        """read fishtail data from excel file"""
        # find fishtail sheet names

        self.data = pd.read_excel(self.file_name, sheet_name=None)
        self.fishtail_sheet_names = list(self.data.keys())

    def make_fastener_system_table_from_file(self):
        """return fastener system table"""
        self.fastener_system_table = self.fishtail_sheets["FastenerSystem Table"]
        return self.fastener_system_table
    
    def get_fastener_system_table(self):
        """return fastener system table"""

        return self.fastener_system_table
    
    def make_fastener_system_dict_from_table(self):
        """return fastener system dictionary"""

        for _, row in self.fastener_system_table.iterrows():
            self.fastener_system_dict[
                row["AirbusEO_TFastenerSystem"]
            ] = fastener_system(
                row["AirbusEO_TFastenerSystem"],
                row["pin"],
                row["nutCollar"],
                row["diameter"],
            )
        return self.fastener_system_dict

    def put_fastener(self, fastener_system):
        """put fastener in dictionary"""

        self.fastener_system_dict[fastener_system.name] = fastener_system
        self.fastener_system_dict2fastener_system_table()
        return self.fastener_system_dict

    def pop_fastener(self, fastener_system):
        """take fastener out of dictionary"""

        self.fastener_system_dict.pop(fastener_system)

        return self.fastener_system_dict

    def get_fastener_system(self, fastener_system):
        """return fastener system"""
        try:
            fastener_system = self.fastener_system_dict[fastener_system]
            return fastener_system
        except KeyError:
            print("ERROR: fastener system not found")
            return None
            
    def get_fastener_system_list(self):
        """return fastener system list"""

        return list(self.fastener_system_dict.keys())

    def fastener_system_dict2fastener_system_table(self):
        """
        It converts the fastener system dictionary to a fastener system table.
        """
        df_list = []
        for name, fs in self.fastener_system_dict.items():
            df_list.append({"AirbusEO_TFastenerSystem" : name, "pin" : fs.pin, "nutCollar" : fs.nutcollar, "diameter" : fs.diameter})
            
        self.fastener_system_table = pd.DataFrame(df_list)


        #'FastenerSystem Table',
        #'Material Table',
        #'Stacking FML',
        #'Metallic Profile Table',
        #'Joint Table',
        #'Panel Table',
        #'Panel FML',
        #'Frame Table',
        #'Stringer Table'
