""" profiles """
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Rectangle
from matplotlib.collections import PatchCollection


## Class definition for sub-elements. Used in cross-section definition. profile class combines defined subels and returns combined values.


class subel(object):
    """sub-element class"""

    __Class_Name__ = "sub element"
    __lib_name__ = "ISAMI_lib"

    def __init__(self, sub_type, pos_x, pos_y):
        self.sub_type = sub_type
        self.x = pos_x
        self.y = pos_y

    def __repr__(self) -> str:
        rep = f"{self.__Class_Name__}({self.sub_type}, {self.x}, {self.y})"
        return rep


class free_elm_body(object):
    """class for attribute calc of freely defined body"""

    # TODO: add hight and width to class

    def __init__(self, subelement_list):

        self.subelement_list = subelement_list

        self.area = (sum(i.A for i in self.subelement_list) * 100) / 100
        self.x_cg = (
            sum(i.A * i.xcg for i in self.subelement_list) * 100 / self.area
        ) / 100
        self.y_cg = (
            sum(i.A * i.ycg for i in self.subelement_list) * 100 / self.area
        ) / 100
        self.Ix = int(
            sum(i.Ixx + i.A * (i.ycg - self.y_cg) ** 2 for i in self.subelement_list)
        )
        self.Iy = int(
            sum(i.Iyy + i.A * (i.xcg - self.x_cg) ** 2 for i in self.subelement_list)
        )
        self.height = max((i.y + 0.5 * i.h) for i in self.subelement_list) - min(
            (i.y - 0.5 * i.h) for i in self.subelement_list
        )
        self.width = max((i.x + 0.5 * i.b) for i in self.subelement_list) - min(
            (i.x - 0.5 * i.b) for i in self.subelement_list
        )


class arc(subel):
    """Class for arc sub-element"""

    __Class_Name__ = "arc"

    def __init__(self, x, y, R, r):
        self.sub_type = "arc"
        super().__init__(self.sub_type, x, y)
        self.xcg = x + R
        self.ycg = y + (1.333 / math.pi) * (R**3 - r**3) / (R**2 - r**2)
        self.R = R
        self.r = r
        self.A = math.pi / 2 * (R**2 - r**2)
        self.Ixx = (9 * math.pi**2 - 64) * (R**4 - (r) ** 4) / (
            72 * math.pi
        ) + math.pi / 2 * (
            R**2 * (1.333 / math.pi * R - self.ycg + y) ** 2
            - (r) ** 2 * (1.333 / math.pi * (r) - self.ycg + y) ** 2
        )
        self.Iyy = (math.pi / 8) * (R**4 - r**4)

        # TODO: check
        self.h = R
        self.b = 2 * R

    def get_data(self):
        data_dict = {
            "sub_type": self.sub_type,
            "x": self.x,
            "y": self.y,
            "xcg": self.xcg,
            "ycg": self.ycg,
            "R": self.R,
            "r": self.r,
            "A": self.A,
            "Ixx": self.Ixx,
            "Iyy": self.Iyy,
        }
        return data_dict

    def __repr__(self) -> str:
        rep = f"{self.__Class_Name__}: {self.sub_type}, {self.x}, {self.y}"
        return rep


class rect(subel):
    """Rectangle sub-element"""

    __Class_Name__ = "rect"

    def __init__(self, x, y, b, h):

        self.sub_type = "rect"
        super().__init__(self.sub_type, x, y)
        self.xcg = x + b / 2
        self.ycg = y + h / 2
        self.b = b
        self.h = h
        self.A = b * h
        self.Ixx = b * h**3 / 12
        self.Iyy = h * b**3 / 12

    def get_data(self):
        data_dict = {
            "sub_type": self.sub_type,
            "x": self.x,
            "y": self.y,
            "xcg": self.xcg,
            "ycg": self.ycg,
            "b": self.b,
            "h": self.h,
            "A": self.A,
            "Ixx": self.Ixx,
            "Iyy": self.Iyy,
        }
        return data_dict

    def __repr__(self) -> str:
        """Return string representation of subel"""
        rep = f"{self.__Class_Name__}({self.sub_type}, {self.x}, {self.y})"
        return rep


class fillet(subel):
    """Fillet sub-element"""

    __Class_Name__ = "fillet"

    def __init__(self, x, y, r):
        self.sub_type = "fillet"
        super().__init__(self.sub_type, x, y)
        self.xcg = x + r / 2

        self.ycg = y + r / 2

        self.r = r

        self.A = r**2 * (1 - math.pi / 4)
        self.Ixx = 0

        self.Iyy = 0

    def get_data(self):
        data_dict = {
            "sub_type": self.sub_type,
            "x": self.x,
            "y": self.y,
            "xcg": self.xcg,
            "ycg": self.ycg,
            "r": self.r,
            "A": self.A,
            "Ixx": self.Ixx,
            "Iyy": self.Iyy,
        }
        return data_dict

    def __repr__(self) -> str:
        rep = f"{self.__Class_Name__}: {self.sub_type}, {self.x}, {self.y}"
        return rep


class qarc(subel):
    """Quarter-arc sub-element"""

    __Class_Name__ = "quarter arc"

    def __init__(self, x, y, R, r, beta):
        self.sub_type = "qarc"
        super().__init__(self.sub_type, x, y)
        alpha = 45

        self.R = R

        self.r = r

        self.beta = beta

        self.xcg = x + math.cos(math.radians(beta)) * 0.6667 * math.sin(
            math.radians(alpha)
        ) / math.radians(alpha) * (R**3 - r**3) / (R**2 - r**2)
        self.ycg = y + math.sin(math.radians(beta)) * 0.6667 * math.sin(
            math.radians(alpha)
        ) / math.radians(alpha) * (R**3 - r**3) / (R**2 - r**2)
        self.A = math.radians(alpha) * (R**2 - r**2)
        self.Ixx = (
            math.radians(alpha) / 4 * (R**4 - r**4) - self.A * (self.ycg - y) ** 2
        )
        self.Iyy = (
            math.radians(alpha) / 4 * (R**4 - r**4) - self.A * (self.xcg - x) ** 2
        )
        self.h = R
        self.b = R

    def get_data(self):
        data_dict = {
            "sub_type": self.sub_type,
            "x": self.x,
            "y": self.y,
            "xcg": self.xcg,
            "ycg": self.ycg,
            "R": self.R,
            "r": self.r,
            "beta": self.beta,
            "A": self.A,
            "Ixx": self.Ixx,
            "Iyy": self.Iyy,
        }
        return data_dict

    def __repr__(self) -> str:
        rep = f"{self.__Class_Name__}: {self.sub_type}, {self.x}, {self.y}"
        return rep


class clp_L_01_a(object):
    """Class for clp_L_01_a"""

    def __init__(self, **kwargs):
        self.struct_type = kwargs.get("struct_type")
        self.struct_name = kwargs.get("struct_name")

        self.ba = kwargs.get("ba")
        self.h = kwargs.get("h")
        self.ra = kwargs.get("ra")
        self.ta = kwargs.get("ta")
        self.tw = kwargs.get("tw")

        self.calculate_attributes()

    def calculate_attributes(self):
        self.of = rect(0, 0, self.ba, self.ta)
        self.web = rect(0, self.ta, self.tw, self.h - self.ta)
        self.f1 = fillet(self.tw, self.ta, self.ra)

        self.subel_list = [self.of, self.web, self.f1]

        self.area = (sum(i.A for i in self.subel_list) * 100) / 100
        self.x_cg = (sum(i.A * i.xcg for i in self.subel_list) * 100 / self.area) / 100
        self.y_cg = (sum(i.A * i.ycg for i in self.subel_list) * 100 / self.area) / 100

        self.Ix = int(
            sum(i.Ixx + i.A * (i.ycg - self.y_cg) ** 2 for i in self.subel_list)
        )
        self.Iy = int(
            sum(i.Iyy + i.A * (i.xcg - self.x_cg) ** 2 for i in self.subel_list)
        )

        self.measurements = {}
        self.measurements["h"] = {
            "xy": (self.of.x - 1, 0),
            "xytext": (self.of.x - 1, self.web.h + self.of.h),
        }
        self.measurements["tw"] = {
            "xy": (0, self.web.h / 2),
            "xytext": (self.web.b + 0.3, self.web.h / 2 + 0.2),
        }
        self.measurements["ba"] = {
            "xy": ((self.of.x, -3)),
            "xytext": ((self.of.b, -2.8)),
        }
        self.measurements["ta"] = {
            "xy": ((self.of.b / 2, 0)),
            "xytext": (self.of.b / 2, self.of.h + 0.5),
        }


class profile(object):
    """Class for profile build out of sub-elements"""

    __Class_Name__ = "profile"
    __lib_name__ = "ISAMI_lib"

    def __init__(self, **kwargs):

        self.struct_type = kwargs.get("StructType")

        # This code is checking if the structure type is manual.
        if self.struct_type.lower() == "manual":
            self.name = kwargs.get("Profile")
            self.subel_list = kwargs.get("subel_list")
            # check if the subel_list is a list of subel objects
            if all(isinstance(x, (arc, qarc, fillet, rect)) for x in self.subel_list):
                # calculate the area, xcg, ycg, Ixx, Iyy
                self.calculate_profile_manually()
            else:
                print("Error: profile elements must be of type arc, qarc, fillet, rect")

        else:
            # Get ISAMI values
            self.name = kwargs.get("Profile")
            self.family = kwargs.get("Family")
            self.number = int(kwargs.get("Number"))
            self.variant = kwargs.get("Variant")
            self.struct_name = (
                f"{self.struct_type}_{self.family}_{self.number}_{self.variant}"
            )
            self.data_dict = kwargs
            self.attributes = {}
            # clean up the data_dict from nan values
            self.clean_dict()
            # get the profile attributes
            self.calculate_profile()

    def calculate_profile_manually(self):
        """Calculate the profile manually"""

        self.struct_name = "manual"
        self.data_dict = {}
        self.attributes = {}

        # build data dict from subel_list
        for n, i in enumerate(self.subel_list):
            self.data_dict[n] = {i.__class__.__name__: i.get_data()}

        self.profile = free_elm_body(self.subel_list)
        self.area = self.profile.area
        self.x_cg = self.profile.x_cg
        self.y_cg = self.profile.y_cg
        self.Ix = self.profile.Ix
        self.Iy = self.profile.Iy
        self.set_profile_attributes()

    def __repr__(self) -> str:
        rep = f"{self.__Class_Name__}({self.struct_name}, {self.data_dict})"
        return rep

    def clean_dict(self):
        """Clean data_dict of nan values"""
        for key in list(self.data_dict):
            if isinstance(self.data_dict[key], float):
                if math.isnan(self.data_dict[key]):
                    del self.data_dict[key]

    def calculate_profile(self):
        """Calculate profile from sub-elements"""
        print(f"Calculating {self.struct_name}")
        print(f"struct_type: {self.struct_type.lower()}")
        # TODO: maybe set up ISAMI class for all profile types instead of nesting it in here
        if self.struct_type.lower() == "stg":
            print(f"family: {self.family}")
            if self.family.lower() == "l":
                print(f"number: {self.number}")
                if self.number == 1:
                    print(f"variant: {self.variant}")
                    if self.variant.lower() == "a":
                        self.profile = clp_L_01_a(
                            struct_type=self.struct_type,
                            struct_name=self.struct_name,
                            ba=self.data_dict["ba"],
                            h=self.data_dict["h"],
                            ra=self.data_dict["ra"],
                            ta=self.data_dict["ta"],
                            tw=self.data_dict["tw"],
                        )
                        self.area = self.profile.area
                        self.x_cg = self.profile.x_cg
                        self.y_cg = self.profile.y_cg
                        self.Ix = self.profile.Ix
                        self.Iy = self.profile.Iy
                        self.subel_list = self.profile.subel_list

                        self.set_profile_attributes()
                    else:
                        print("Variant not defined")
                else:
                    print("Number not defined")

    def set_profile_attributes(self):
        """Set profile attributes"""
        self.attributes["name"] = self.name
        self.attributes["struct_name"] = self.struct_name
        self.attributes["area"] = self.area
        self.attributes["x_cg"] = self.x_cg
        self.attributes["y_cg"] = self.y_cg
        self.attributes["Ix"] = self.Ix
        self.attributes["Iy"] = self.Iy

    def get_profile_data(self):
        """Return profile data"""
        return self.data_dict

    def get_profile_attributes(self):
        """Return profile attributes"""
        return self.attributes

    def generate_prof_elem_list(self):
        """generate list of profile elements"""

        prof_elem_list = []
        for i in self.subel_list:
            if isinstance(i, rect):
                prof_elem_list.append(Rectangle((i.x, i.y), i.b, i.h))
            if isinstance(i, arc):
                prof_elem_list.append(
                    Wedge((i.x, i.y), i.R, 0, 180, width=(i.R - i.r))
                )
            if isinstance(i, qarc):
                prof_elem_list.append(
                    Wedge(
                        (i.x, i.y), i.R, i.beta - 45, i.beta + 45, width=(i.R - i.r)
                    )
                )
        return prof_elem_list

    def plot_profile(self):
        """plot profile"""

        # It creates a figure with two subplots, ax1 and ax2. ax1 is the main plot, and ax2 is the text plot.
        fig, (ax1, ax2) = plt.subplots(
            1, 2, figsize=(20, 10), gridspec_kw={"width_ratios": [2.5, 1]}
        )

        label = label_name(self.name)
        # plot the profile
        ax1.set_title(label, fontsize=22, color="navy")
        ax1.set_aspect("equal", adjustable="box")
        ax1.grid(which="major", linestyle="solid", color="black", alpha=0.5)
        ax1.grid(which="minor", linestyle="dotted", linewidth="0.5", color="darkgreen")

        profile_list = self.generate_prof_elem_list()

        ax1.add_collection(PatchCollection(profile_list))
        ax1 = generate_info_text(ax1, self)
        ax1 = generate_measurements(ax1, self)
        ax1.autoscale_view()

        # profile attributes

        # A way to set the background color of the text plot.
        ax2.set_facecolor("#76F9BD")

        # Adding the text to the plot.
        ax2 = add_text(ax2, self.get_profile_attributes())

        # It removes the ticks from the x and y axis.
        ax2.set_xticks([])
        ax2.set_yticks([])
        plt.close()
        return fig


def label_name(name):
    return "profile plot: " + name


def add_text(ax, text_dict):
    """add text to plot"""

    for n, (k, v) in enumerate(text_dict.items()):
        ax.text(
            0.2,
            (0.9 - (0.05 * n)),
            str(f"{k} : {v}"),
            transform=ax.transAxes,
            style="italic",
        )
    return ax


def generate_info_text(ax, inp_profile):
    """generate text for profile plot"""

    infotext = f"A = {inp_profile.area} mm2\nx_cg = {inp_profile.x_cg} mm\ny_cg = {inp_profile.y_cg} mm\nIxx = {inp_profile.Ix} mm4\nIyy = {inp_profile.Iy} mm4"

    ax.text(
        0.1,
        0.8,
        infotext,
        transform=ax.transAxes,
        bbox=dict(linewidth=2, ec="red", fc="powderblue", alpha=0.5, pad=10),
    )
    return ax


def generate_measurements(ax, inp_profile):
    """generate measurements for profile plot"""

    mstyle = dict(
        arrowstyle="|-|", ec="red", shrinkA=0, shrinkB=0, relpos=(0, 0), linewidth=1
    )
    if inp_profile.struct_name == "Stg_L_1_a":
        for k, v in inp_profile.profile.measurements.items():
            ax.annotate(text=k, xy=v["xy"], xytext=v["xytext"], arrowprops=mstyle)

    return ax
