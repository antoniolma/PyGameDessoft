# Setup do mapa
level_map = [

'                                                                                                                                                                      FFF           ',
'                                                                                                                     A                                     T     CT   FFF           ',
'                              T  CT   XXX                                                         TC    T           XXX                                     XXXXXX    FFF           ',
'                               XXX          XXXXX                 X                              XXXXXX                                             TV    T          FF            ',
'                X   X    XX                 FFFF    T     CTV    TF   X                   TV     T                      TV  T            T     CT                     FF          O ',
' M             XF   FX                     EFFF      XXXXXXX      F   F     X             X               X           X                  XXXXXXXEEEEXEEEE   x     X         X    XXX',
'XXXX  T  CT   XFF   FFX      CT     E     EXFFFA  EXXFFFFFFFXXEEEEFEEEFC    FX      TV   T                   E   XXX  EEEEE    T   CXXXXXFFFFFFFFFFFFFFFF              XXX       FFF',
'FFFF   XXX   XFFF   FFFXXXXXXX      X     XFFFFXXXXFFFFFFFFFFFFXXXFXXXFXXXXXFFXXXXXXX                        X   FFF  XXXXX     XXXXFFFFFFFFFFFFFFFFFFFFFXX      TV    T         FFF'
]

tile_size = 64                                # Tamanho do tile (Bloco de chão)
screen_width = 1024                           # Largura do tile  (20 tiles)
screen_height = len(level_map) * tile_size    # Altura do tile (11 tiles)

#print(screen_height)
#print(len(level_map[0])*tile_size)

# Score possível = 20000
