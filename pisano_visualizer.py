# -----------------------------------------------------------
# Pisano Visualizer
# -----------------------------------------------------------
# pisano_visualizer.py
#
# Interactive visualization of Pisano periods as a bargraph
# Shows one complete period of a modulus 
# Saves the result as image, textfile and Lilypond score
# Coded in November 2025
#
# Author: Arthur Stammet
# -----------------------------------------------------------


import pygame, math, os

# --- Config ---
INIT_WIDTH = 1000
HEIGHT = 400
MARGIN = 100
GRAPH_WIDTH = 800

pygame.init()

# --- Setup main window ---
screen = pygame.display.set_mode((INIT_WIDTH, HEIGHT))
pygame.display.set_caption("Pisano Visualizer")

# --- Info window state ---
info_visible = True
info_surface = pygame.Surface((500, 300))  # size of info box

# --- Setup fonts ---
font = pygame.font.SysFont(None, 30)
info_font = pygame.font.SysFont(None, 22)

# --- Ensure folders exist ---
os.makedirs("Images", exist_ok=True)
os.makedirs("Scores", exist_ok=True)
os.makedirs("Textfiles", exist_ok=True)

# --- Core math ---
def pisano_list(m, cap=100000):
    seq = []
    a, b = 1, 0
    for _ in range(1, cap + 1):
        a, b = b, (a + b) % m
        seq.append(b)
        if a == 1 and b == 0:
            break
    return seq

def pisano_mirror(m):
    a, b, c = 0, 1, 2
    mirror = 0
    mirror_seq = [1, m - 1, 0]
    ex_seq = [m - 1, 1, 0]
    while c <= 100000:
        d = (a + b) % m
        end_seq = [a, b, d]
        a, b, c = b, d, c + 1
        if end_seq == mirror_seq:
            mirror += 1
        if end_seq == ex_seq:
            break
    return mirror

def pisano_length(m):
    psl = [1]
    a,b,c = 0,1,2
    end_seq = [1,1,2]
    ex_seq = [m-1, 1, 0]
    while c <= 100000:
        d = (a+b) % m
        end_seq = [a,b,d]
        a,b,c = b,d,c+1
        psl.append(d)
        if end_seq == ex_seq:
            break
    return c-1

def pisano_sections(m):
    psl = [1]
    a,b,c = 0,1,2
    z = 0
    end_seq = [1,1,2]
    ex_seq = [m-1, 1, 0]
    while c <= 100000:
        d = (a+b) % m
        if d == 0:
            z = z+1
        end_seq = [a,b,d]
        a,b,c = b,d,c+1
        psl.append(d)
        if end_seq == ex_seq:
            break
    return z

# --- Create title ---
def title_text(m):
    # Simple, clean title
    return f"Pisano {m}"

def subtitle_text(m):
    length = pisano_length(m)
    sect = pisano_sections(m)
    st = f"Fibonacci 1-{length} mod {m}"
    st += f" ({sect}*{int(length/sect)}"
    if pisano_mirror(m) > 0:
        st += " notes with mirrored 2nd half)"
    else:
        st += " notes)"
    return st

# --- Drawing ---
def draw_pisano(m):
    global screen
    seq = pisano_list(m)
    n = len(seq)
    if n == 0:
        screen.fill((255,255,255))
        return

    max_val = max(seq) if seq else 1
    spacing = 0 if n > 69 else 1
    raw_width = GRAPH_WIDTH / n - spacing
    bar_width = max(1, math.ceil(raw_width))

    # Compute actual graph width from number of bars
    graph_width = n * (bar_width + spacing) - spacing

    # Window width = graph width + 100 pixels margin
    new_width = max(INIT_WIDTH, graph_width + 100)
    if screen.get_width() != new_width or screen.get_height() != HEIGHT:
        screen = pygame.display.set_mode((new_width, HEIGHT))

    screen.fill((255, 255, 255))

     # Define fonts once at the top
    title_font = pygame.font.SysFont(None, 36, bold=False)     # bigger for title
    subtitle_font = pygame.font.SysFont(None, 24, bold=False)  # smaller for subtitle

    # --- In draw_pisano ---
    # Title centered
    title = title_text(m)
    text = title_font.render(title, True, (0, 0, 0))
    text_rect = text.get_rect(center=(new_width // 2, 32))
    screen.blit(text, text_rect)

    # Subtitle just below, smaller and grey
    subtitle = subtitle_text(m)
    subtext = subtitle_font.render(subtitle, True, (100, 100, 100))
    subtext_rect = subtext.get_rect(center=(new_width // 2, 55))
    screen.blit(subtext, subtext_rect)

    # Center graph horizontally
    start_x = (new_width - graph_width) // 2
    graph_height = HEIGHT - 2 * MARGIN + 70

    section = 0
    mirror_flag = pisano_mirror(m)
    mid = n // 2 if (mirror_flag >= 1 and n % 2 == 0) else None

    for i, val in enumerate(seq):
        if val == 0:
            section += 1
        h = 3 if val == 0 else int((val / max_val) * graph_height)
        x = start_x + i * (bar_width + spacing)
        y = HEIGHT + 60- MARGIN - h

        color = (150, 150, 150) if section % 2 == 0 else (100, 100, 100)
        if val == 0:
            color = (0, 0, 0)
        if mid is not None and i >= mid and val != 0:
            r, g, b = color
            color = (r, g, min(255, int(b + 0.2 * 255)))

        pygame.draw.rect(screen, color, (x, y, bar_width, h))
        pygame.display.flip()


# --- Lilypond score generator ---

# create a list with Notenames in LilyPond format (4 octaves)
notes = [
"c,,,","cis,,,","d,,,","dis,,,","e,,,","f,,,","fis,,,","g,,,","gis,,,","a,,,","ais,,,","b,,,",                          # 0 - 11
"c,,","cis,,","d,,","dis,,","e,,","f,,","fis,,","g,,","gis,,","a,,","ais,,","b,,",                                      # 12 - 23
"c,","cis,","d,","dis,","e,","f,","fis,","g,","gis,","a,","ais,","b,",                                                  # 24 - 35
"c","cis","d","dis","e","f","fis","g","gis","a","ais","b",                                                              # 36 - 47
"c'","cis'","d'","dis'","e'","f'","fis'","g'","gis'","a'","ais'","b'",                                                  # 48 - 59
"c''","cis''","d''","dis''","e''","f''","fis''","g''","gis''","a''","ais''","b''",                                      # 60 - 71
"c'''","cis'''","d'''","dis'''","e'''","f'''","fis'''","g'''","gis'''","a'''","ais'''","b'''",                          # 72 - 83
"c''''","cis''''","d''''","dis''''","e''''","f''''","fis''''","g''''","gis''''","a''''","ais''''","b''''",              # 84 - 95
"c'''''","cis'''''","d'''''","dis'''''","e'''''","f'''''","fis'''''","g'''''","gis'''''","a'''''","ais'''''","b'''''",  # 96 - 107
"c''''''"                                                                                                               # 108
]

def signature(length,counter):
    # find out the time signature fitting with the length of the loop
    # longest mesure we want to use is counter/4

    # initialize a float and an integer value for comparison
    mf = 0.
    mi = 0
    tsig = ""

    while counter > 1:
        mf = length/counter
        mi = int(length/counter)

        if mf == mi:
            return counter        # number of notes per mesure
            break
        counter = counter-1

def transposition(m):
    if m < 25:
        t = 48
    if m > 24 and m < 49:
        t = 36
    if m > 48 and m < 61:
        t = 24
    if m > 60:
        t = 12
    return t

def clef(note):
    clef_name = ""
    if note > 73:
        clef_name = "treble^8"
    if note > 47 and note <= 73:
        clef_name = "treble"
    if note > 23 and note <= 47:
        clef_name = "bass"
    if note > 11 and note <= 23:
        clef_name = "bass_8"
    if note <= 11:
        clef_name = "bass_15"
    return clef_name

def pisano_score(m, file, ocr):
    # analyse series in order to obtain all data to be used for the score

    # initialize variables
    length = pisano_length(m)
    a,b,c = 0,1,2
    z = 1
    end_seq = [1,1,2]
    ex_seq = [m-1, 1, 0]
    new_sect = 0
    d_old = 1
    old_clef = " "
    barcounter = 1

    pf = open(file,'w')

    # page settings
    pf.write('''\\paper {'''+"\r")
    pf.write('''  top-margin = 15'''+"\r")
    pf.write('''  left-margin = 15'''+"\r")
    pf.write('''  right-margin = 15'''+"\r")
    pf.write('''  indent = 0'''+"\r")
    pf.write('''  }'''+"\r")
    pf.write('''\\version "2.18.2-1"'''+"\r")

    # create LilyPond header
    pf.write('''\\header{'''+"\r")
    pf.write('''   title = "Pisano Melody '''+str(m)+'''"'''+"\r")
    subtit = '''   subtitle = "Fibonacci 1-'''+str(length)+" mod "+str(m)
    subtit = subtit + ''' ( ''' + str(z)+" * "+str(int(length/z))
    if pisano_mirror(m) > 0:
        subtit = subtit + ''' notes with mirrored 2nd half )"'''
    else:
        subtit = subtit + ''' notes )"'''
    pf.write(subtit+"\r")
    pf.write('''   poet = "Coded in Python"'''+"\r")
    pf.write('''   composer = "Arthur Stammet"'''+"\r")
    pf.write('''   opus = "2019"'''+"\r")
    pf.write('''   }'''+"\r")
    pf.write('''{'''+"\r")
    # write time signature, bars and notes with supplementary informations
    # tsig = signature(length,7)
    pf.write('''\\time '''+str(signature(length,7))+'''/4 \r''')
    pf.write('''\\bar ".|:"'''+"\r")

    bt = b+transposition(m)
    if clef(bt) != old_clef:
        pf.write('''\\clef "'''+clef(bt)+'''" ''')
        old_clef = clef(bt)
        pf.write(str(notes[bt]))
        if ocr == 0:
            pf.write('''-1'''+"\r")
            pf.write('''^"Section 1"''')
        pf.write("\r")
    while c <= length:
        d = (a+b) % m
        if d_old == 0:
            z = z+1
            new_sect = 1
        else:
            new_sect = 0
        pos = c
        a,b,c = b,d,c+1
        bt = b+transposition(m)
        if clef(bt) != old_clef:
            pf.write('''\\clef "'''+clef(bt)+'''" ''')
            old_clef = clef(bt)
        pf.write(str(notes[bt]))
        if ocr == 0:
            pf.write('''-'''+str(pos))
        pf.write(" \r")
        if ocr == 0:
            if new_sect == 1:
                pf.write('''^"Section '''+str(z)+'''" \r''')
                if pos-1 == length/2:
                    if pisano_mirror(m) > 0:
                        pf.write('''^"Begin of mirror"'''+"\r")

        barcounter = barcounter+1
        d_old = d
        if barcounter % signature(length,7) == 0:
                pf.write('''|'''+"\r")

    pf.write('''\\bar ":|."'''+"\r")
    pf.write('}')

    pf.close()

# --- Save functions ---
os.makedirs("Textfiles", exist_ok=True)
os.makedirs("Images", exist_ok=True)
os.makedirs("Scores", exist_ok=True)

def save_snapshot(m):
    # Scale the current screen surface by 3x
    scaled_surface = pygame.transform.scale(
        screen, (screen.get_width() * 3, screen.get_height() * 3))
    fname = os.path.join("Images", f"Pisano {m}.png")
    pygame.image.save(scaled_surface, fname)
    print(f"Saved image (3x bigger): {fname}")

def save_score(m):
    fname = os.path.join("Scores", f"Pisano Melody {m}.ly")
    pisano_score(m, fname, 1)
    print(f"Saved score: {fname}")

def save_text(m):
    seq = pisano_list(m)
    length = len(seq)
    titleline = title_text(m)
    subtitleline = subtitle_text(m)
    fname = os.path.join("Textfiles", f"Pisano {m}.txt")
    with open(fname, "w") as f:
        # Title lines (lines 1-2)
        f.write(f"{titleline}\n")
        f.write(f"{subtitleline}\n")

        # Number of steps (line 3)
        f.write(f"{length}\n")

        # Sequence values, one per line (lines 4-...)
        for val in seq:
            f.write(f"{val}\n")
    print(f"Saved text file: {fname}")


# --- Main loop ---
def main():
    m = 13
    draw_pisano(m)
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_RIGHT:
                    m += 1; draw_pisano(m)
                elif event.key == pygame.K_LEFT:
                    m = max(3, m - 1); draw_pisano(m)
                elif event.key == pygame.K_UP:
                    m += 10; draw_pisano(m)
                elif event.key == pygame.K_DOWN:
                    m = max(3, m - 10); draw_pisano(m)
                elif event.key == pygame.K_t:
                    save_text(m)
                elif event.key == pygame.K_s:
                    save_snapshot(m)
                elif event.key == pygame.K_l:
                    if m < 98: save_score(m)
                elif event.key == pygame.K_1:
                    m = 10
                    draw_pisano(m)
                elif event.key == pygame.K_2:
                    m = 20
                    draw_pisano(m)
                elif event.key == pygame.K_3:
                    m = 30
                    draw_pisano(m)
                elif event.key == pygame.K_4:
                    m = 40
                    draw_pisano(m)
                elif event.key == pygame.K_5:
                    m = 50
                    draw_pisano(m)
                elif event.key == pygame.K_6:
                    m = 60
                    draw_pisano(m)
                elif event.key == pygame.K_7:
                    m = 70
                    draw_pisano(m)
                elif event.key == pygame.K_8:
                    m = 80
                    draw_pisano(m)
                elif event.key == pygame.K_9:
                    m = 90
                    draw_pisano(m)

            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    m += 1; draw_pisano(m)
                elif event.y < 0:
                    m = max(3, m - 1); draw_pisano(m)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left click
                    if m < 98: save_score(m)
                    save_snapshot(m)
                    save_text(m)

        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
