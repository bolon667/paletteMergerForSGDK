from PIL import Image
import glob

def indexedPaste(im1, im2, pal_shift):
    cur_img_size = im1.size
    px1 = im1.load()
    px2 = im2.load()
    cols = int(cur_img_size[0]/8)
    rows = int(cur_img_size[1]/8)

    for tileX in range( 0, cols ):
        for tileY in range( 0, rows ):
            for y in range(0,8):
              for x in range(0,8):
                if((px2[x + tileX * 8,y + tileY * 8 ]) != pal_shift):
                    px1[x + tileX * 8,y + tileY * 8 ] = px2[x + tileX * 8,y + tileY * 8 ]
    return im1
    
def indexedPasteMask(im1, im2, mask_path):
    cur_img_size = im1.size
    px1 = im1.load()
    px2 = im2.load()
    
    img_mask = Image.open(mask_path)
    px_mask = img_mask.load()
    cols = int(cur_img_size[0]/8)
    rows = int(cur_img_size[1]/8)

    for tileX in range( 0, cols ):
        for tileY in range( 0, rows ):
            for y in range(0,8):
              for x in range(0,8):
                if((px_mask[x + tileX * 8,y + tileY * 8 ]) != 0):
                    px1[x + tileX * 8,y + tileY * 8 ] = px2[x + tileX * 8,y + tileY * 8 ]
    img_mask.close()
    return im1


def mergePicsSGDK():
    print("Merging pics")
    pal_pic_paths = ["", "", "", ""]
    pal_pic_paths_priority = ["", "", "", ""]
    pal_pic_mask_paths = ["", "", "", ""]
    
    files = glob.glob("*")
    for path in files:
        if path.find("-") == -1:
            continue
        cur_pal = path.split("-")[1]
        if(cur_pal == "pal0.png"):
            pal_pic_paths[0] = path
        elif(cur_pal == "pal1.png"):
            pal_pic_paths[1] = path
        elif(cur_pal == "pal2.png"):
            pal_pic_paths[2] = path
        elif(cur_pal == "pal3.png"):
            pal_pic_paths[3] = path
        elif(cur_pal == "pal0_p.png"):
            pal_pic_paths_priority[0] = path
        elif(cur_pal == "pal1_p.png"):
            pal_pic_paths_priority[1] = path
        elif(cur_pal == "pal2_p.png"):
            pal_pic_paths_priority[2] = path
        elif(cur_pal == "pal3_p.png"):
            pal_pic_paths_priority[3] = path
        elif(cur_pal == "pal0_mask.png"):
            pal_pic_mask_paths[0] = path
        elif(cur_pal == "pal1_mask.png"):
            pal_pic_mask_paths[1] = path
        elif(cur_pal == "pal2_mask.png"):
            pal_pic_mask_paths[2] = path
        elif(cur_pal == "pal3_mask.png"):
            pal_pic_mask_paths[3] = path
    
    #Find first cur_image_size
    cur_img_size = (0,0)
    for i in range(len(pal_pic_paths)):
        if pal_pic_paths[i] == "":
            continue
        cur_image = Image.open(pal_pic_paths[i])
        print("Found ", cur_image.size)
        cur_img_size = cur_image.size
        cur_image.close()
        break
    if cur_img_size == (0,0):
        for i in range(len(pal_pic_paths_priority)):
            if pal_pic_paths_priority[i] == "":
                continue
            cur_image = Image.open(pal_pic_paths_priority[i])
            print("Found ", cur_image.size)
            cur_img_size = cur_image.size
            cur_image.close()
            break
    if cur_img_size == (0,0):
        print("Images not found")
        return
    #Creating a new image
    resultImage = Image.new(mode="P", size=cur_img_size)
    
    #Generating a palette
    palette_shifts = [0,16,32,48]
    palette_shifts_priority = [128,144,160,176]
    
    temp_palette = []       
    for i in range(256):
       temp_palette.extend([0,0,i])
    #Merging palette from images WITHOUT priority
    for i in range(len(pal_pic_paths)):
        if pal_pic_paths[i] == "":
            continue
        shift_ind = palette_shifts[i]

        cur_img = Image.open(pal_pic_paths[i])
        cur_img_pal = cur_img.getpalette()

        for j in range(16*3):
            temp_palette[(shift_ind*3)+j] = cur_img_pal[j]
        cur_img.close()
    
    #Merging palette from images WITH priority
    for i in range(len(pal_pic_paths_priority)):
        if pal_pic_paths_priority[i] == "":
            continue
        shift_ind = palette_shifts_priority[i]

        cur_img = Image.open(pal_pic_paths_priority[i])
        cur_img_pal = cur_img.getpalette()

        for j in range(16*3):
            temp_palette[(shift_ind*3)+j] = cur_img_pal[j]
        cur_img.close()
    
    resultImage.putpalette(temp_palette)
    
    cols = int(cur_img_size[0]/8)
    rows = int(cur_img_size[1]/8)

    
    #Merging images without priority
    for i in range(len(pal_pic_paths)):
        if pal_pic_paths[i] == "":
            continue
        print(pal_pic_paths[i])
        cur_img = Image.open(pal_pic_paths[i])
        cur_px = cur_img.load()
        
        for tileX in range( 0, cols ):
          for tileY in range( 0, rows ) :
            for y in range(0,8):
              for x in range(0,8):
                cur_px[x + tileX * 8,y + tileY * 8 ] += palette_shifts[i]
        if pal_pic_mask_paths[i] == "":
            indexedPaste(resultImage, cur_img, palette_shifts[i])
        else:
            indexedPasteMask(resultImage, cur_img, pal_pic_mask_paths[i])
        
        cur_img.close()
    #Merging images with priority
    
    for i in range(len(pal_pic_paths_priority)):
        if pal_pic_paths_priority[i] == "":
            continue
        print(pal_pic_paths_priority[i])
        cur_img = Image.open(pal_pic_paths_priority[i])
        cur_px = cur_img.load()

        for tileX in range( 0, cols ):
          for tileY in range( 0, rows ) :
            for y in range(0,8):
              for x in range(0,8):
                cur_px[x + tileX * 8,y + tileY * 8 ] += palette_shifts_priority[i]
        if pal_pic_mask_paths[i] == "":
            indexedPaste(resultImage, cur_img, palette_shifts[i])
        else:
            indexedPasteMask(resultImage, cur_img, pal_pic_mask_paths[i])
        cur_img.close()
    
    #Saving result
    resultImage.save("result.png")
    print("Done")
    
mergePicsSGDK()