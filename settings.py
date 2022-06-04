# Setup do mapa

level_map = [

'                                                ',
'                                                ',
'                                                ',
'                                        XXXXXXXX',
'      T C   XEEX                     XO     FFFF',
'AM     XXXXXFXXF        X           XFXX    FFFF',
'XXXX   FFFFFFFFFEE  C  XF           FFFFEEEEFFFF',
'FFFF   FFFFFFFFFXXXXXXXFF  XXXXXXXXXFFFFFFFFFFFF'
]

tile_size = 64                                # Tamanho do tile (Bloco de chão)
screen_width = 1024                           # Largura do tile  (20 tiles)
screen_height = len(level_map) * tile_size                           # Altura do tile (11 tiles)

#print(screen_height)
#print(len(level_map[0])*tile_size)
