# Setup do mapa
level_map = [
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                    XXXX',
'        C   XEEX                 X     X',
' M E   XXXXXXXXX        X       XXXX   X',
'XXXX   XXXXXXXXX       XX       XXXX   X',
'XXXXXXXXXXXXXXXX  XXXXXXX  XXXXXXXXXXXXX'
]

tile_size = 64                                # Tamanho do tile (Bloco de chão)
screen_width = 768                            # Largura do tile  (20 tiles)
screen_height = len(level_map) * tile_size                           # Altura do tile (11 tiles)

print(screen_height)