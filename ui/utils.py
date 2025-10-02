import pygame

def render_text_with_outline(text, font, text_color=(255,255,255), outline_color=(0,0,0)):
    # Render main text
    text_surf = font.render(text, True, text_color)
    outline_surf = font.render(text, True, outline_color)

    # Create a surface large enough for outline
    w, h = text_surf.get_size()
    surface = pygame.Surface((w+2, h+2), pygame.SRCALPHA)

    # Draw outline by blitting the black text slightly offset in 8 directions
    offsets = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    for ox, oy in offsets:
        surface.blit(outline_surf, (ox+1, oy+1))

    # Draw white text on top
    surface.blit(text_surf, (1,1))

    return surface