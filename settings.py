# Setup do mapa

level_map = [

'                                                                                                                                                                      ',
'                                                                                                                     A                                     TC     T   ',
'                              TC  T   XXX                                                         TC    T           XXX                                     XXXXXX    ',
'                               XXX           XXXX                 X                                XXXXX                                                              ',
'                X   X    XX                 XFFF    TC     TV    TF   X                   TV     T                     TV    T           TC     T    TV    T        O ',
' M             XF   FX                     EFFF      XXXXXXX      F   F     X             X               X           X                  XXXXXXXEEEEXEEEE          XXX',
'XXXX  T  CT   XFF   FFXC      T           EXFFFA  EXXFFFFFFFXXEEEEFEEEFC    FXC     TV   T                   E   XXX  EEEEE    TC   XXXXXFFFFFFFFFFFFFFFF          FFF',
'FFFF   XXX   XFFF   FFFXXXXXXX            XFFFFXXXXFFFFFFFFFFFFXXXFXXXFXXXXXFFXXXXXXX                        X   FFF  XXXXX     XXXXFFFFFFFFFFFFFFFFFFFFF          FFF'
]

tile_size = 64                                # Tamanho do tile (Bloco de chão)
screen_width = 1024                           # Largura do tile  (20 tiles)
screen_height = len(level_map) * tile_size    # Altura do tile (11 tiles)

print(screen_height)
print(len(level_map[0])*tile_size)
