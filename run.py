from pathlib import Path
import sys
from PIL import Image
import numpy as np

def RGBtoHSL(x):
    r, g, b = x
    h = s = l = 0
    # 色相
    if max([r,g,b])==r:
        h = 60 * ((g - b)/(r-min([r,g,b])))
    elif max([r,g,b])==g:
        h = 60 * ((b - r)/(g-min([r,g,b])))+120
    elif max([r,g,b])==b:
        h = 60 * ((r - g)/(b-min([r,g,b])))+240
    else:
        h = 0
    h = int(h+360) if h<0 else int(h)
 
    # 彩度
    CNT = (max([r,g,b])+min([r,g,b]))/2
    s = (max([r,g,b])-min([r,g,b]))/(max([r,g,b])+min([r,g,b])) if CNT<128 else (max([r,g,b])-min([r,g,b]))/(510-max([r,g,b])-min([r,g,b]))
    s = int(s*100)
    

    # 輝度
    l = int((max([r,g,b])+min([r,g,b]))/2/255*100)

    return (h, s, l)

def convert(inputpath:str):
    # 32×32で15色に減色
    img = Image.open(inputpath)
    img2 = (img.resize((32, 32), Image.LANCZOS)
               .quantize(15)
               .convert("RGB")
    )

    # RGBデータをピクセル単位で取得
    pict = img2.getdata()
    # 仕様RGBリストを取得
    colorList2  = sorted(list(set(pict)))
    print(colorList2)
    # numpy配列に変換
    pltimg = np.array([list(map(list, colorList2))])
    # プロット
    """ 
    import matplotlib.pyplot as plt
    plt.imshow(pltimg, vmin=0, vmax=255, interpolation='none')
    plt.show() 
    """

    # HSBに変換
    colorList = list(map(RGBtoHSL, colorList2))
    path = 'dst.txt'

    with open(path, mode='w') as f:
        f.write('ColorList:\n')
        for x in range(len(colorList)):
            f.write('{0}: ({1}, {2}, {3})\n'.format(x+1, int(colorList[x][0]*30/360)+1, int(colorList[x][1]*15/100)+1, int(colorList[x][2]*15/100)+1))

        f.write('PictList:\n')
        for x in range(len(pict)):
            f.write("{0},".format(colorList2.index(pict[x])+1))
            if x%32==31:
                f.write("\n")

if __name__ == '__main__':
    args = sys.argv

    if len(args) != 2:
        print("Error: Image file path is missing.")
        print(" -> python3 run.py (imageFilePath)")
        sys.exit()
    
    filePath = args[1]
    if not Path(filePath).exists():
        print("Error: Spefified Image file is not exists.")
        sys.exit()

    convert(filePath)
