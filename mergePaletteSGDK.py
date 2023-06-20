from PIL import Image
import glob

def indexedPaste(im1, im2, pal_shift):
    cur_img_size = im1.size
    px1 = im1.load()
    px2 = im2.load()
    cols = int(cur_img_size[0]/8)
    rows = int(cur_img_size[1]/8)
    
    used_tiles = [[0 for x in range(rows)] for y in range(cols)]
    #Finding used tiles on image
    for tileX in range( 0, cols ):
        for tileY in range( 0, rows ):
            for y in range(0,8):
              for x in range(0,8):
                if((px2[x + tileX * 8,y + tileY * 8 ]) != pal_shift):
                    #If, tile have pixel with not first color of palette, than, tile is used
                    used_tiles[tileX][tileY] = 1
                    break

    #Pasting one tile on another if tile is used
    for tileX in range( 0, cols ):
        for tileY in range( 0, rows ):
            for y in range(0,8):
              for x in range(0,8):
                if(used_tiles[tileX][tileY] == 1):
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
    pal_pic_layers = [-1, -1, -1, -1]
    pal_pic_paths_priority = ["", "", "", ""]
    pal_pic_mask_paths = ["", "", "", ""]
    
    files = glob.glob("*")
    for path in files:
        if path.find("-") == -1:
            continue
        cur_pal = path.split("-")[1]
        cur_pal = cur_pal[:cur_pal.find(".")] #remove extension
        layer_num = -1
        if (cur_pal.find("_") != -1):
            print(cur_pal, "settings")
            settings_arr = cur_pal.split("_")
            cur_pal = settings_arr[0] 
            layer_num = int(settings_arr[1])
            print(cur_pal, "settings2")
        
       
        if(cur_pal == "pal0"):
            pal_pic_paths[0] = path
            pal_pic_layers[0] = layer_num
        elif(cur_pal == "pal1"):
            pal_pic_paths[1] = path
            pal_pic_layers[1] = layer_num
        elif(cur_pal == "pal2"):
            pal_pic_paths[2] = path
            pal_pic_layers[2] = layer_num
        elif(cur_pal == "pal3"):
            pal_pic_paths[3] = path
            pal_pic_layers[3] = layer_num
        elif(cur_pal == "pal0P"):
            pal_pic_paths_priority[0] = path
            pal_pic_layers[0] = layer_num
        elif(cur_pal == "pal1P"):
            pal_pic_paths_priority[1] = path
            pal_pic_layers[1] = layer_num
        elif(cur_pal == "pal2P"):
            pal_pic_paths_priority[2] = path
            pal_pic_layers[2] = layer_num
        elif(cur_pal == "pal3P"):
            pal_pic_paths_priority[3] = path
            pal_pic_layers[3] = layer_num
        elif(cur_pal == "pal0Mask"):
            pal_pic_mask_paths[0] = path
            pal_pic_layers[0] = layer_num
        elif(cur_pal == "pal1Mask"):
            pal_pic_mask_paths[1] = path
            pal_pic_layers[1] = layer_num
        elif(cur_pal == "pal2Mask"):
            pal_pic_mask_paths[2] = path
            pal_pic_layers[2] = layer_num
        elif(cur_pal == "pal3Mask"):
            pal_pic_mask_paths[3] = path
            pal_pic_layers[3] = layer_num
    
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
        shift_ind_mirr = palette_shifts_priority[i]

        cur_img = Image.open(pal_pic_paths[i])
        cur_img_pal = cur_img.getpalette()

        for j in range(16*3):
            temp_palette[(shift_ind*3)+j] = cur_img_pal[j]
            temp_palette[(shift_ind_mirr*3)+j] = cur_img_pal[j]
        cur_img.close()
    
    #Merging palette from images WITH priority
    for i in range(len(pal_pic_paths_priority)):
        if pal_pic_paths_priority[i] == "":
            continue
        shift_ind = palette_shifts[i]
        shift_ind_mirr = palette_shifts_priority[i]

        cur_img = Image.open(pal_pic_paths_priority[i])
        cur_img_pal = cur_img.getpalette()

        for j in range(16*3):
            temp_palette[(shift_ind*3)+j] = cur_img_pal[j]
            temp_palette[(shift_ind_mirr*3)+j] = cur_img_pal[j]
        cur_img.close()
    
    resultImage.putpalette(temp_palette)
    
    cols = int(cur_img_size[0]/8)
    rows = int(cur_img_size[1]/8)

    #ordering layers according to layer number
    mergeOrder = [0,1,2,3]
    for i in range(4):
        layer_num = pal_pic_layers[i]
        if layer_num == -1: #If layer is unspecified
            continue
        mergeOrder[i] = layer_num
    mergeOrder = [0,1,2,3]
    print("Merge order")
    print(mergeOrder)
    #Merging images without priority
    for cur_layer in range(4):
        for i in range(4):
            if(pal_pic_layers[i] != cur_layer):
                continue
            if pal_pic_paths[i] != "":
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
            if pal_pic_paths_priority[i] != "":
                cur_img = Image.open(pal_pic_paths_priority[i])
                cur_px = cur_img.load()

                for tileX in range( 0, cols ):
                  for tileY in range( 0, rows ) :
                    for y in range(0,8):
                      for x in range(0,8):
                        cur_px[x + tileX * 8,y + tileY * 8 ] += palette_shifts_priority[i]
                if pal_pic_mask_paths[i] == "":
                    indexedPaste(resultImage, cur_img, palette_shifts_priority[i])
                else:
                    indexedPasteMask(resultImage, cur_img, pal_pic_paths_priority[i])
                cur_img.close()
    
    #Saving result
    resultImage.save("result.png")
    print("Done")
    
mergePicsSGDK()