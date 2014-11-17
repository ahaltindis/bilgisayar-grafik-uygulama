import pyglet
import math

from pyglet.gl import *
from pyglet.window import mouse
 
win = pyglet.window.Window()

tiklama = 0
ucgen_cizim = False
ucgen = [[0,0],[0,0],[0,0]]
cevrilmis_ucgen_cizim = False
cevrilmis_ucgen = [[0,0],[0,0],[0,0]]
ref_nokta = [0,0]
ref_nokta_cizim = False
donme_acisi = 0
donme_acisi_oku = False
sifirla = False

print "Ucgen icin uc noktaya tikla:"

def matris_carp(m1,m2):
    # Verilen iki matrisin carpimini hesaplar ve sonuc matrisi donderir.
    return [[(m1[0][0]*m2[0][0] + m1[0][1]*m2[1][0] + m1[0][2]*m2[2][0]), 
            (m1[0][0]*m2[0][1] + m1[0][1]*m2[1][1] + m1[0][2]*m2[2][1]), 
            (m1[0][0]*m2[0][2] + m1[0][1]*m2[1][2] + m1[0][2]*m2[2][2])],
        [(m1[1][0]*m2[0][0] + m1[1][1]*m2[1][0] + m1[1][2]*m2[2][0]), 
            (m1[1][0]*m2[0][1] + m1[1][1]*m2[1][1] + m1[1][2]*m2[2][1]), 
            (m1[1][0]*m2[0][2] + m1[1][1]*m2[1][2] + m1[1][2]*m2[2][2])],
        [(m1[2][0]*m2[0][0] + m1[2][1]*m2[1][0] + m1[2][2]*m2[2][0]), 
            (m1[2][0]*m2[0][1] + m1[2][1]*m2[1][1] + m1[2][2]*m2[2][1]), 
            (m1[2][0]*m2[0][2] + m1[2][1]*m2[1][2] + m1[2][2]*m2[2][2])]]

def ucgen_hesapla():
    global cevrilmis_ucgen
    global cevrilmis_ucgen_cizim
    global donme_acisi
    global ucgen
    global ref_nokta
    global sifirla
    
    # Verilen ucgenin 3 degerli hale cevrilmis matrisi
    u_matris = [[ucgen[0][0], ucgen[0][1], 1],[ucgen[1][0], ucgen[1][1], 1],[ucgen[2][0], ucgen[2][1], 1]]
    
    # Ucgeni orjine oteleyen transform matrisi
    t1_matris = [[1, 0, 0],[0, 1, 0],[-ref_nokta[0], -ref_nokta[1], 1]]
    
    # Orjin etrafinda verilen derece kadar saatin ters yonunde ceviren transform matrisi
    r_matris = [[0, 0, 0],[0, 0, 0],[0, 0, 1]]
    r_matris[0][0] = math.cos(math.radians(float(donme_acisi)))
    r_matris[0][1] = math.sin(math.radians(float(donme_acisi)))
    r_matris[1][0] = -math.sin(math.radians(float(donme_acisi)))
    r_matris[1][1] = math.cos(math.radians(float(donme_acisi)))
    
    # Cevrilen ucgeni eski yerine oteleyen transform matiris
    t2_matris = [[1, 0, 0],[0, 1, 0],[ref_nokta[0], ref_nokta[1], 1]]
    
    # Ucgene tum transform matrislerini uygula
    sonuc_matris = matris_carp(matris_carp(u_matris,t1_matris),matris_carp(r_matris,t2_matris))
    
    # Cevrilen ucgeni ekrana bastiralacak formata cevir
    cevrilmis_ucgen[0][0] = int(sonuc_matris[0][0])
    cevrilmis_ucgen[0][1] = int(sonuc_matris[0][1])
    cevrilmis_ucgen[1][0] = int(sonuc_matris[1][0])
    cevrilmis_ucgen[1][1] = int(sonuc_matris[1][1])
    cevrilmis_ucgen[2][0] = int(sonuc_matris[2][0])
    cevrilmis_ucgen[2][1] = int(sonuc_matris[2][1])
    
    cevrilmis_ucgen_cizim = True
    print "Ucgen ({},{}) referans noktasina gore {} derece donderildi".format(ref_nokta[0], ref_nokta[1], donme_acisi)
    print "Yeniden baslamak icin sahneye tiklayin"
    sifirla = True

@win.event
def on_draw(): 	
    glClear(GL_COLOR_BUFFER_BIT)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)   

    if ucgen_cizim:	
        pyglet.graphics.draw(3, pyglet.gl.GL_TRIANGLES, 
        ('v2i', (
        ucgen[0][0], ucgen[0][1], 
        ucgen[1][0], ucgen[1][1],
        ucgen[2][0], ucgen[2][1])))
    
    if ref_nokta_cizim:
        pyglet.graphics.draw(1, pyglet.gl.GL_POINTS, ('v2i', (ref_nokta[0], ref_nokta[1])))
    
    if cevrilmis_ucgen_cizim:
        pyglet.graphics.draw(3, pyglet.gl.GL_TRIANGLES, 
        ('v2i', (
        cevrilmis_ucgen[0][0], cevrilmis_ucgen[0][1], 
        cevrilmis_ucgen[1][0], cevrilmis_ucgen[1][1],
        cevrilmis_ucgen[2][0], cevrilmis_ucgen[2][1])))

@win.event
def on_mouse_press(x, y, button, modifiers):
    global ucgen_cizim
    global tiklama
    global ucgen
    global ref_nokta
    global ref_nokta_cizim
    global donme_acisi
    global donme_acisi_oku
    global sifirla
    global cevrilmis_ucgen_cizim
    
    if not ucgen_cizim:		
        if button == mouse.LEFT:
            ucgen[tiklama] = [x,y]			
            print "Ucgen Kose{}: ({},{})".format(tiklama,ucgen[tiklama][0],ucgen[tiklama][1])
            tiklama = tiklama + 1
            if tiklama == 3:
                ucgen_cizim = True	
                print "Referans noktasi icin bir noktaya tiklayin:"
    
    elif not ref_nokta_cizim:
        if button == mouse.LEFT:
            ref_nokta = [x,y]
            print "Referans Nokta: [{},{}]".format(ref_nokta[0],ref_nokta[1])
            ref_nokta_cizim = True
            donme_acisi = raw_input("Donme Acisini Girin: ")
            donme_acisi_oku = True
            ucgen_hesapla()
        
    elif sifirla:
        ucgen_cizim = False
        tiklama = 0
        cevrilmis_ucgen_cizim = False
        ref_nokta_cizim = False
        donme_acisi_oku = False
        sifirla = False
        print "Ucgen icin uc noktaya tikla:"

pyglet.app.run()
