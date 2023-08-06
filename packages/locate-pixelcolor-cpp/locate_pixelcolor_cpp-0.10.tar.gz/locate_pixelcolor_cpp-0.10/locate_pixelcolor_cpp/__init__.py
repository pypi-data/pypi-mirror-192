import configparser
import os
import re
import subprocess
import numpy as np
from touchtouch import touch
import cv2
import ctypes
from flexible_partial import FlexiblePartialOwnName


try:
    from .locate_pixelcolor_cppmodule import *
except Exception as fe:
    print(fe)
    print("Please compile the module and reload it!")
    print(r'''
Execute:

compile_localize_picture_color_with_cpp(
    vcvarsall_bat=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat",
    cl_exe=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\cl.exe",
    link_exe=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\link.exe",
)

*Compiler:
MSVC ..... C++ x64/x86 build tools from: https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community&channel=Release&version=VS2022&source=VSLandingPage&passive=false&cid=2030

    
    ''')


def get_file(f):
    return os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), f))


def get_file_own_folder(f, folder):
    return os.path.normpath(os.path.join(folder, f))


def compile_cpp(
    modulename,
    fnames,
    vcvarsall_bat,
    cl_exe,
    link_exe,
    cppsource,
    compilerflags=(
        "/std:c++17",
        "/Ferelease",
        "/EHsc",
        "/MT",
        "/O2",
        "/bigobj",
    ),
):
    cfgfile = get_file(f"{modulename}.ini")
    output = get_file(f"{modulename}.dll")

    config = configparser.ConfigParser()
    allcommand = [
        vcvarsall_bat,
        "x64",
        "&&",
        cl_exe,
        "/D_USRDL",
        "/D_WINDLL",
        cppsource,
        *compilerflags,
        "/link",
        "/DLL",
        f'/OUT:"{output}"',
        "/MACHINE:X64",
    ]
    subprocess.run(allcommand, shell=True)

    p = subprocess.run([link_exe, "/dump", "/exports", output], capture_output=True)
    fnamesre = [
        (
            x,
            re.compile(
                rf"[\r\n]+\s+[a-fA-F0-9]+\s+[a-fA-F0-9]+\s+[a-fA-F0-9]+\s+(\?[^\s]*{x}@[^\s]+)"
            ),
        )
        for x in fnames
    ]
    decor = p.stdout.decode("utf-8", "ignore")
    print(decor)
    franmesre = [(x[0], x[1].findall(decor)) for x in fnamesre]
    config["DEFAULT"] = {k: v[0] for k, v in franmesre if v}
    with open(cfgfile, "w") as f:
        config.write(f)


def write_c_code(
    functionname,
    whole_c_code,
    argtypes,
    addtopyfile,
    vcvarsall_bat=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat",
    cl_exe=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\cl.exe",
    link_exe=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\link.exe",
    modulename="strigi",
    compilerflags=(
        "/std:c++17",
        "/Ferelease",
        "/EHsc",
        "/MT",
        "/O2",
    ),
):
    cpath = get_file(f"{modulename}_cppcode.cpp")
    touch(cpath)
    with open(cpath, mode="w", encoding="utf-8") as f:
        f.write(whole_c_code)
    compile_cpp(
        modulename,
        fnames=[functionname],
        vcvarsall_bat=vcvarsall_bat,
        cl_exe=cl_exe,
        link_exe=link_exe,
        cppsource=cpath,
        compilerflags=compilerflags,
    )
    cfgfile = get_file(f"{modulename}.ini")
    output = get_file(f"{modulename}.dll")
    loadfile = rf"""
import sys
import ctypes
from numpy.ctypeslib import ndpointer
import configparser
from flexible_partial import FlexiblePartialOwnName
import numpy as np
def execute_function(f,*args, **kwargs):
    f(*args, **kwargs)

def add_argt():
    allargtypes = [
            {argtypes}
    ]
    allfu = []
    for (fname, descri, function_prefix, functionnormalprefix, restype, argtypes,) in allargtypes:
        fun = lib.__getattr__(funcs[fname])
        fun.restype = restype
        if len(argtypes) != 0:
            fun.argtypes = argtypes
        allfu.append((fname, fun))
        setattr(c_functions, f"{{functionnormalprefix}}{{fname}}", fun)
        setattr(c_functions, f"{{function_prefix}}{{fname}}", FlexiblePartialOwnName(execute_function, descri, True, fun), )


dllpath = r"{output}"
cfgfile = r"{cfgfile}"
lib = ctypes.CDLL(dllpath)
confignew = configparser.ConfigParser()
confignew.read(cfgfile)
funcs = confignew.defaults()
c_functions = sys.modules[__name__]
add_argt()
    """

    loadfile = loadfile + addtopyfile

    pypath = get_file(f"{modulename}module.py")
    touch(pypath)
    with open(pypath, mode="w", encoding="utf-8") as f:
        f.write(loadfile)


def compile_localize_picture_color_with_cpp(
    vcvarsall_bat=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat",
    cl_exe=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\cl.exe",
    link_exe=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\link.exe",
):
    whole_c_code = r"""
    //#include <string.h>
    //#include <iostream>
    //#include <conio.h>
    #include <ppl.h>
    //#include <sstream>
    //#include <execution>
    //#include <array>
    #include <cmath>
    #include <cstdlib>
    #include <atomic>  
    std::atomic<size_t> value(0);

    int create_id() {
        return value++;
        }


    __declspec(dllexport) void checkrgbvalues(const unsigned char * r,const  unsigned char * g, const unsigned char * b,const unsigned char * r1,const unsigned char * g1,const unsigned char * b1,const unsigned int * imageshape, int * outdatav, int * outdatav1,const size_t sizearr, const size_t searchcoloarr,unsigned int * finalindex)
    {
        value=0;
        int imagediv = imageshape[1];


        concurrency::parallel_for ( std::size_t(0), sizearr, [&](std::size_t ii)
        {
            for (size_t i = 0; i < searchcoloarr; ++i){


        if((r[ii] == b1[i]) && (g[ii] == g1[i]) && (b[ii] == r1[i])){
        int x; x  = (int) ii;
        auto dv = std::div(x, imagediv);
        size_t bubu = create_id();

        outdatav[bubu] = dv.quot;
        outdatav1[bubu] = dv.rem;

    }

        };});
    finalindex[0] = value;
    }

    """

    functionname = "checkrgbvalues"
    functiondesctiption = ""

    argtypes = rf"""

            (
                "{functionname}",
                "{functiondesctiption}",
                "aa_",
                "bb_",
                None,
                [
                    ctypes.POINTER(ctypes.c_uint8),
                    ctypes.POINTER(ctypes.c_uint8),
                    ctypes.POINTER(ctypes.c_uint8),
                    ctypes.POINTER(ctypes.c_uint8),
                    ctypes.POINTER(ctypes.c_uint8),
                    ctypes.POINTER(ctypes.c_uint8),
                    ctypes.POINTER(ctypes.c_uint32),
                    ctypes.POINTER(ctypes.c_int32),
                    ctypes.POINTER(ctypes.c_int32),
                    ctypes.c_size_t,

                    ctypes.c_size_t,
                    ctypes.POINTER(ctypes.c_uint32),
                ],
            ),
    """

    addtopyfile = ""
    write_c_code(
        functionname,
        whole_c_code,
        argtypes,
        addtopyfile,
        vcvarsall_bat=vcvarsall_bat,
        cl_exe=cl_exe,
        link_exe=link_exe,
        modulename="locate_pixelcolor_cpp",
        compilerflags=(
            "/std:c++20",
            "/Ferelease",
            "/EHsc",
            "/MT",
            "/Og",
            "/Oi",
            "/Ot",
            "/Oy",
            "/Ob3",
            "/GF",
            "/Gy",
            "/fp:fast",
        ),
    )


def search_colors(pic, colors):
    b, g, r = cv2.split(pic)
    rint = r.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))

    gint = g.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))

    bint = b.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))

    r11, g11, b11 = (
        [x[0] for x in colors],
        [x[1] for x in colors],
        [x[2] for x in colors],
    )

    r1np = np.require(np.array(r11), np.uint8, ["ALIGNED", "C_CONTIGUOUS"])
    r1 = r1np.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))

    g1np = np.require(np.array(g11), np.uint8, ["ALIGNED", "C_CONTIGUOUS"])
    g1 = g1np.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))

    b1np = np.require(np.array(b11), np.uint8, ["ALIGNED", "C_CONTIGUOUS"])
    b1 = b1np.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))

    imgshapenp = np.require(
        np.array(pic.shape, dtype=np.uint32), np.uint32, ["ALIGNED", "C_CONTIGUOUS"]
    )
    imgshapenpint = imgshapenp.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
    bshape = b.shape[0] * b.shape[1]
    resu = np.zeros(bshape, dtype=np.int32)
    resuint = resu.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))
    resu1 = np.zeros(bshape, dtype=np.int32)
    resuint1 = resu1.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))

    finalindex = np.zeros((1,), dtype=np.uint32)
    finalindexint1 = finalindex.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))

    size = b.size
    sizecolors = r1np.size
    c_functions.bb_checkrgbvalues(
        rint,
        gint,
        bint,
        r1,
        g1,
        b1,
        imgshapenpint,
        resuint,
        resuint1,
        size,
        sizecolors,
        finalindexint1,
    )
    farind = finalindexint1._arr[0]
    x1 = resuint._arr[:farind]
    y1 = resuint1._arr[:farind]
    return np.array((y1, x1)).T
