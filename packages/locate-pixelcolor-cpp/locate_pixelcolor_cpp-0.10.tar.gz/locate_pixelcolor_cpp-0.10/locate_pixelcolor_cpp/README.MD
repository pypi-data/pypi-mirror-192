# Locate RGB values in a picture! Up to 10x faster than NumPy, 100x faster than PIL. 

## How to install 

### pip install locate-pixelcolor-cpp

### Please install this C++ compiler:

MSVC ..... C++ x64/x86 build tools from: https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community&channel=Release&version=VS2022&source=VSLandingPage&passive=false&cid=2030

Localize the following files (Version number might vary) and copy their path:
vcvarsall_bat = r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat"

cl_exe = r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\cl.exe"

link_exe = r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\link.exe"


## Compile the code
```python
from locate_pixelcolor_cpp import compile_localize_picture_color_with_cpp
compile_localize_picture_color_with_cpp(
    vcvarsall_bat=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat",
    cl_exe=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\cl.exe",
    link_exe=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\link.exe",
)
```

### Benchmark 

```python
# Let's use a 4525 x 6623 x 3 picture https://www.pexels.com/pt-br/foto/foto-da-raposa-sentada-no-chao-2295744/

from locate_pixelcolor_cpp import search_colors # The function can only be imported when the compilation was successful ( compile_localize_picture_color_with_cpp )
import cv2
path=r"C:\Users\Gamer\Documents\Downloads\pexels-alex-andrews-2295744.jpg"
im = cv2.imread(path)


colors=[(66,  71,  69),(62,  67,  65),(144, 155, 153),(52,  57,  55),(127, 138, 136),(53,  58,  56),(51,  56,  54),(32,  27,  18),(24,  17,   8),]
#%timeit search_colors(im, colors=colors)
##127 ms ± 3.61 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)

from locate_pixelcolor import search_colors as search_colors2
# first version with numexpr
# https://github.com/hansalemaos/locate_pixelcolor
#%timeit search_colors2(im,colors)
##400 ms ± 18.9 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

import numpy as np 
b,g,r = im[...,0],im[...,1],im[...,2]
#%timeit np.where(((b==66)&(g==71)&(r==69))|((b==62)&(g==67)&(r==65))|((b==144)&(g==155)&(r==153))|((b==52)&(g==57)&(r==55))|((b==127)&(g==138)&(r==136))|((b==53)&(g==58)&(r==56))|((b==51)&(g==56)&(r==54))|((b==32)&(g==27)&(r==18))|((b==24)&(g==17)&(r==8)))
##1 s ± 16.1 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)


from PIL import Image
img = Image.open(path)
img = img.convert("RGB")
datas = img.getdata()

def pi():
    newData = []
    for item in datas:
        if (item[0] == 66 and item[1] == 71 and item[2] == 69) or (item[0] == 62 and item[1] == 67 and item[2] == 65) or (item[0] == 144 and item[1] == 155 and item[2] == 153) or (item[0] == 52 and item[1] == 57 and item[2] == 55) or (item[0] == 127 and item[1] == 138 and item[2] == 136) or (item[0] == 53 and item[1] == 58 and item[2] == 56) or (item[0] == 51 and item[1] == 56 and item[2] == 54) or (item[0] == 32 and item[1] == 27 and item[2] == 18) or (item[0] == 24 and item[1] == 17 and item[2] == 8):
            newData.append(item)
    return newData
%timeit pi()

##10.6 s ± 51.6 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)


## One color 

from locate_pixelcolor_cpp import search_colors
import cv2
path=r"C:\Users\Gamer\Documents\Downloads\pexels-alex-andrews-2295744.jpg"
im = cv2.imread(path)
#%timeit search_colors(im, colors=[(255,255,255)])
#75.3 ms ± 247 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)



# first version with numexpr
# https://github.com/hansalemaos/locate_pixelcolor
from locate_pixelcolor import search_colors
import cv2
path=r"C:\Users\Gamer\Documents\Downloads\pexels-alex-andrews-2295744.jpg"
im = cv2.imread(path)
# %timeit search_colors(im, colors=[(255,255,255)])
# 98 ms ± 422 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)


b,g,r = im[...,0],im[...,1],im[...,2]
# %timeit np.where(((b==255)&(g==255)&(r==255)))
# 150 ms ± 209 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)



from PIL import Image
img = Image.open(path)
img = img.convert("RGB")
datas = img.getdata()
def get_coords_with_pil(col):
    newData = []
    for item in datas:
        if item[0] == col[0] and item[1] == col[1] and item[2] == col[2]:
            newData.append(item)
    return newData
%timeit get_coords_with_pil(col=(255,255,255))
3.41 s ± 14.6 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

```