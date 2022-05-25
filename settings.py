# Setup do mapa
level_map = [
'                    ',
'                    ',
'                    ',
'                    ',
'                    ',
'                    ',
'   C                ',
'   XXX     X        ',
'   M      X         ',
'         XX         ',
'XXXXXXXXXXXXXXXXXXXX'
]

tile_size = 64                                # Tamanho do tile (Bloco de chão)
screen_width = 768                           # Altura do tile  (20 tiles)
screen_height = len(level_map) * tile_size                           # Largura do tile (11 tiles)

print(screen_height)