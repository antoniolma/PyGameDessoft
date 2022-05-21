# Setup do mapa
level_map = [
'                    ',
'                    ',
'                    ',
'                    ',
'                    ',
'                    ',
'                    ',
'                    ',
'                    ',
'   M                ',
'XXXXXXXXXXXXXXXXXXXX'
]

tile_size = 64                                # Tamanho do tile (Bloco de chão)
screen_width = 1280                           # Altura do tile  (20 tiles)
screen_height = len(level_map) * tile_size                           # Largura do tile (11 tiles)

print(screen_height)