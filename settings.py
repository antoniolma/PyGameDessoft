# Setup do mapa

level_map = [

'                                                ',
'                                                ',
'                                                ',
'                                        XXXXXXXX',
'        C   XEEX                     X      XXXX',
' M E   XXXXXXXXX        X           XXXX    XXXX',
'XXXX   XXXXXXXXXEE  C  XX           XXXX EEEXXXX',
'XXXX   XXXXXXXXXXXXXXXXXX  XXXXXXXXXXXXXXXXXXXXX'
]

tile_size = 64                                # Tamanho do tile (Bloco de chão)
screen_width = 768                            # Largura do tile  (20 tiles)
screen_height = len(level_map) * tile_size                           # Altura do tile (11 tiles)

print(screen_height)
print(len(level_map[0])*tile_size)
