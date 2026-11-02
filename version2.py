import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.integrate import solve_ivp

class Particula:
    """Clase que representa una partícula en 2D."""
    def __init__(self, m, r, r0, v0):
        self.m = m            # Masa
        self.r = r            # Radio
        self.pos = np.array(r0, dtype=float)  # Posición inicial [x, y]
        self.vel = np.array(v0, dtype=float)  # Velocidad inicial [vx, vy]

    def energia_cinetica(self):
        return 0.5 * self.m * np.linalg.norm(self.vel)**2

    def momento_lineal(self):
        return self.m * self.vel

class SistemaColision:
    """Clase que gestiona el sistema y la integración numérica (Método de Euler modificado / Eventos)."""
    def __init__(self, p1, p2, e=1.0):
        self.p1 = p1
        self.p2 = p2
        self.e = e  

    def colision(self):
        """Calcula las velocidades post-colisión en 2D."""
        pos_diff = self.p1.pos - self.p2.pos
        vel_diff = self.p1.vel - self.p2.vel
        dist = np.linalg.norm(pos_diff)
        
       
        if dist <= (self.p1.r + self.p2.r) and np.dot(vel_diff, pos_diff) < 0:
            n = pos_diff / dist  # Vector normal
            v_rel_n = np.dot(vel_diff, n)
            
           
            j = -(1 + self.e) * v_rel_n / ((1/self.p1.m) + (1/self.p2.m))
            
            
            self.p1.vel = self.p1.vel + (j / self.p1.m) * n
            self.p2.vel = self.p2.vel - (j / self.p2.m) * n

    def paso_euler(self, dt):
        """Integra las ecuaciones de movimiento usando el método de Euler."""
      
        self.p1.pos += self.p1.vel * dt
        self.p2.pos += self.p2.vel * dt
        self.colision()


particula_1 = Particula(m=2.0, r=0.5, r0=[-5.0, 1.0], v0=[3.0, -0.5])
particula_2 = Particula(m=3.0, r=0.5, r0=[5.0, -0.5], v0=[-2.0, 0.5])

sistema = SistemaColision(particula_1, particula_2, e=1.0) # Colisión elástica


dt = 0.02
pasos = 200
historial_p1 = []
historial_p2 = []


P_inicial = particula_1.momento_lineal() + particula_2.momento_lineal()
E_inicial = particula_1.energia_cinetica() + particula_2.energia_cinetica()

for _ in range(pasos):
    historial_p1.append(particula_1.pos.copy())
    historial_p2.append(particula_2.pos.copy())
    sistema.paso_euler(dt)

historial_p1 = np.array(historial_p1)
historial_p2 = np.array(historial_p2)


P_final = particula_1.momento_lineal() + particula_2.momento_lineal()
E_final = particula_1.energia_cinetica() + particula_2.energia_cinetica()

print(f"Momento Lineal Total Inicial: {P_inicial} | Final: {P_final}")
print(f"Energía Cinética Total Inicial: {E_inicial:.2f} J | Final: {E_final:.2f} J")


fig, ax = plt.subplots()
ax.set_xlim(-6, 6)
ax.set_ylim(-3, 3)
ax.set_aspect('equal')
ax.set_title("Simulación de Colisión 2D")
ax.grid(True)

cuerpo1 = plt.Circle(historial_p1[0], particula_1.r, color='blue', label='P1')
cuerpo2 = plt.Circle(historial_p2[0], particula_2.r, color='red', label='P2')
ax.add_patch(cuerpo1)
ax.add_patch(cuerpo2)
ax.legend()

def animar(i):
    cuerpo1.set_center(historial_p1[i])
    cuerpo2.set_center(historial_p2[i])
    return cuerpo1, cuerpo2

ani = animation.FuncAnimation(fig, animar, frames=pasos, interval=20, blit=False)
plt.show()

#TODO: ver variables y cambiarlos, en la ecuación, preguntar el porque de como modifica todo