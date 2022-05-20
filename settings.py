# Setup do mapa
level_map = [
'                                                            ',
'                                                            ',
'                                                            ',
'                                                            ',
'                                                            ',
'                                                            ',
'  M          XX                                             ',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
]

tile_size = 64                                # Tamanho do tile (Bloco de chão)
screen_width = 1200                           # Altura do tile
screen_height = len(level_map) * tile_size    # Largura do tile

print(screen_height)