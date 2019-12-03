import os
import shutil
import struct
from tqdm import tqdm
INPUT_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "/input/"
OUTPUT_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "/output/"
DDS_HEADER_32 = b'DDS |\x00\x00\x00\x07\x10\x08\x00 \x00\x00\x00 \x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \x00\x00\x00\x04\x00\x00\x00DXT1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
DDS_HEADER_1024 = b'DDS |\x00\x00\x00\x07\x10\x08\x00\x00\x04\x00\x00\x00\x04\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \x00\x00\x00\x04\x00\x00\x00DXT1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

def get_spring_map_files():
    """ Returns a list of dae files in the input directory """
    files = []
    for file in os.listdir(INPUT_DIRECTORY):
        if ".sd7" not in file:
            continue
        files.append(file)
    return files

def convert_maps():
    """ Generate a skeleton for every file in the input folder """
    if not os.path.exists(OUTPUT_DIRECTORY + 'mod/'):
        os.makedirs(OUTPUT_DIRECTORY + 'mod/')

    if not os.path.exists(OUTPUT_DIRECTORY + 'mod/maps'):
        os.makedirs(OUTPUT_DIRECTORY + 'mod/maps')

    if not os.path.exists(OUTPUT_DIRECTORY + 'mod/art/textures/ui/session/icons/mappreview'):
        os.makedirs(OUTPUT_DIRECTORY + 'mod/art/textures/ui/session/icons/mappreview')


    for file in get_spring_map_files():
        print('Converting ' + INPUT_DIRECTORY + file + '...')
        os.system( '7z x -aoa ' + INPUT_DIRECTORY + file + ' -o'+ INPUT_DIRECTORY + file[0:-4] + ' > NUL' )
        if os.path.exists(INPUT_DIRECTORY + file[0:-4]  + '/Mini.png'):
            print('Found preview. Copying...')
            dest = shutil.copyfile(INPUT_DIRECTORY + file[0:-4]  + '/Mini.png'  , OUTPUT_DIRECTORY +  'mod/art/textures/ui/session/icons/mappreview/' + file[0:-4]+ '.png')
        if os.path.exists(INPUT_DIRECTORY + file[0:-4]  + '/maps/' + file[0:-4] + '.smt'):
            print('Found Spring Tile File. Translating...')
            with open(INPUT_DIRECTORY + file[0:-4]  + '/maps/' + file[0:-4] + '.smt', "rb") as f:
                # https://springrts.com/wiki/Mapdev:SMT_format

                print('Header: ' +  str(f.read(16))[2:-5])
                print('Version: ' + str(int.from_bytes(f.read(4), "little")))
                num_tiles = int.from_bytes(f.read(4), "little") # Number of tiles
                print('Tile number: ' + str(num_tiles))
                tile_size = int.from_bytes(f.read(4), "little") # Tile_size 32
                print('Tile size: ' + str(tile_size))
                print('Compression: ' + str(int.from_bytes(f.read(4), "little")) + ' (DXT1).')
                print('Extracting Textures')
                files = []
                for i in tqdm(range(0, num_tiles)):
                    files.append(DDS_HEADER_32 + f.read(680))
                    # with open(OUTPUT_DIRECTORY + 'tex_' + str(i) + '.dds','wb') as dds_texture:
                        # dds_texture.write(DDS_HEADER_32 + f.read(680))

                print("Nb de textures de terrain", len(files))
        if os.path.exists(INPUT_DIRECTORY + file[0:-4]  + '/maps/' + file[0:-4] + '.smf'):
            print('Found Spring Tile File. Translating...')
            with open(INPUT_DIRECTORY + file[0:-4]  + '/maps/' + file[0:-4] + '.smf', "rb") as f:
                # https://springrts.com/wiki/Mapdev:SMF_format
                print('Header: ' +  str(f.read(16))[2:-5])
                print('Version: ' + str(int.from_bytes(f.read(4), "little")))
                print('Id: ' + str(int.from_bytes(f.read(4), "little")))
                width = int.from_bytes(f.read(4), "little")
                print('Width: ' + str(width))
                length = int.from_bytes(f.read(4), "little")
                print('Length: ' + str(length))
                print('Square size: ' + str(int.from_bytes(f.read(4), "little")))
                print('Texels per square size: ' + str(int.from_bytes(f.read(4), "little")))
                print('Tile size: ' + str(int.from_bytes(f.read(4), "little")))
                print('Depth min: ' + str(struct.unpack('f', f.read(4))))
                print('Depth max: ' + str(struct.unpack('f', f.read(4))))
                height_map_offset = int.from_bytes(f.read(4), "little")
                print('Height map offset: ' + str(height_map_offset))
                map_type_offset = int.from_bytes(f.read(4), "little")
                print('Map type offset: ' + str(map_type_offset))
                print('Tile index offset: ' + str(int.from_bytes(f.read(4), "little")))
                mini_map_offset = int.from_bytes(f.read(4), "little")
                print('Mini map offset: ' + str(mini_map_offset))
                metal_map_offset = int.from_bytes(f.read(4), "little")
                print('Metal map offset: ' + str(metal_map_offset))
                print('Feature map offset: ' + str(int.from_bytes(f.read(4), "little")))
                extra_header_count = int.from_bytes(f.read(4), "little")
                print('Extra header count: ' + str(extra_header_count))
                print('Parsing extra headers...')
                for i in tqdm(range(0, extra_header_count)):
                    extra_header_size = int.from_bytes(f.read(4), "little")
                    extra_header_type = int.from_bytes(f.read(4), "little")
                    extra_header_data = f.read(extra_header_size)
                print('Reading height map...')
                area = (width+1)*(length+1)
                for i in tqdm(range(0, int(area)) ):
                    f.read(2)
                print('Reading type map...')
                half_area = int((width/2.0)*(length/2.0) )
                for i in tqdm(range(0, half_area)):
                    f.read(1)

                # Hack to get the proper minimap
                while(f.tell() < mini_map_offset):
                    f.read(1)
                print('Reading mini map...')
                with open(OUTPUT_DIRECTORY + file[0:-4] + '_minimap.dds','wb') as dds_texture:
                    dds_texture.write(DDS_HEADER_1024 + f.read(699048))
                f.read(4)
                f.read(4)
                print('Number of tiles in this file : ' + str(int.from_bytes(f.read(4), "little")))
                print('The filename of the smt. : ' + str(f.read(len(file))))
                print('Reading tile index...')
                tile_count = int((width / 4.0) * (length / 4.0))
                for i in tqdm(range(0, tile_count)):
                    f.read(4)
                # print('Reading metal mini map...')
                # f.seek(metal_map_offset)
                # with open(OUTPUT_DIRECTORY + file[0:-4] + '_metal_minimap.dds','wb') as dds_texture:
                #     dds_texture.write(DDS_HEADER_1024 + f.read(int((width / 2) * (length / 2))))

convert_maps()