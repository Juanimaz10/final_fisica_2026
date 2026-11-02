import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Particula:
    def __init__(self, m, r, r0, v0):
        self.m = m            
        self.r = r            
        self.pos = np.array(r0, dtype=float)  
        self.vel = np.array(v0, dtype=float)  

    def energia_cinetica(self):
        return 0.5 * self.m * np.linalg.norm(self.vel)**2

    def momento_lineal(self):
        return self.m * self.vel

class SistemaColision:
    def __init__(self, p1, p2, e=1.0):
        self.p1 = p1
        self.p2 = p2
        self.e = e  

    def colision(self):
        pos_diff = self.p1.pos - self.p2.pos
        vel_diff = self.p1.vel - self.p2.vel
        dist = np.linalg.norm(pos_diff)
        
        if dist <= (self.p1.r + self.p2.r) and np.dot(vel_diff, pos_diff) < 0:
            n = pos_diff / dist  
            v_rel_n = np.dot(vel_diff, n)
            
            j = -(1 + self.e) * v_rel_n / ((1/self.p1.m) + (1/self.p2.m))
            
            self.p1.vel = self.p1.vel + (j / self.p1.m) * n
            self.p2.vel = self.p2.vel - (j / self.p2.m) * n

    def paso_euler(self, dt):
        self.p1.pos += self.p1.vel * dt
        self.p2.pos += self.p2.vel * dt
        self.colision()


def ejecutar_simulacion(m1, r1, x1, y1, vx1, vy1, m2, r2, x2, y2, vx2, vy2, e, pasos, dt, titulo):
    # Inicialización de partículas y sistema
    particula_1 = Particula(m=m1, r=r1, r0=[x1, y1], v0=[vx1, vy1])
    particula_2 = Particula(m=m2, r=r2, r0=[x2, y2], v0=[vx2, vy2])
    sistema = SistemaColision(particula_1, particula_2, e=e) 

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

    print("\n" + "="*50)
    print("              RESULTADOS DE LA SIMULACIÓN              ")
    print("="*50)
    print(f"Momento Lineal Total Inicial: {P_inicial} | Final: {P_final}")
    print(f"Energía Cinética Total Inicial: {E_inicial:.2f} J | Final: {E_final:.2f} J")

    # Configuración de la animación
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_aspect('equal')
    ax.set_title(titulo)
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


# --- BUCLE PRINCIPAL DEL MENÚ (WHILE TRUE) ---
while True:
    print("\n" + "="*50)
    print("             MENÚ PRINCIPAL - COLISIÓN 2D              ")
    print("="*50)
    print("1. Ejecutar simulación con valores por defecto")
    print("2. Modificar variables por consola y ejecutar simulación")
    print("3. Salir / Cortar la simulación")
    
    opcion = input("Selecciona una opción (1, 2 o 3): ").strip()

    if opcion == '1':
        print("\nEjecutando simulación con valores por defecto...")
        ejecutar_simulacion(
            m1=2.0, r1=0.5, x1=-5.0, y1=1.0, vx1=3.0, vy1=-0.5,
            m2=3.0, r2=0.5, x2=5.0, y2=-0.5, vx2=-2.0, vy2=0.5,
            e=1.0, pasos=200, dt=0.02,
            titulo="Simulación de Colisión 2D (Por Defecto)"
        )

    elif opcion == '2':
        print("\n" + "="*50)
        print("         MODIFICACIÓN DE VARIABLES POR CONSOLA         ")
        print("="*50)
        print("Presiona ENTER sin escribir nada para conservar el valor entre corchetes [].\n")
        try:
            # Partícula 1
            print("--- Partícula 1 ---")
            m1 = float(input("Masa [2.0]: ") or 2.0)
            r1 = float(input("Radio [0.5]: ") or 0.5)
            x1 = float(input("Posición X inicial [-5.0]: ") or -5.0)
            y1 = float(input("Posición Y inicial [1.0]: ") or 1.0)
            vx1 = float(input("Velocidad X inicial [3.0]: ") or 3.0)
            vy1 = float(input("Velocidad Y inicial [-0.5]: ") or -0.5)

            # Partícula 2
            print("\n--- Partícula 2 ---")
            m2 = float(input("Masa [3.0]: ") or 3.0)
            r2 = float(input("Radio [0.5]: ") or 0.5)
            x2 = float(input("Posición X inicial [5.0]: ") or 5.0)
            y2 = float(input("Posición Y inicial [-0.5]: ") or -0.5)
            vx2 = float(input("Velocidad X inicial [-2.0]: ") or -2.0)
            vy2 = float(input("Velocidad Y inicial [0.5]: ") or 0.5)

            # Parámetros generales
            print("\n--- Parámetros Generales ---")
            e = float(input("Coeficiente de restitución 'e' (0 a 1) [1.0]: ") or 1.0)
            pasos = int(input("Número de pasos de simulación [200]: ") or 200)
            dt = float(input("Paso de tiempo dt [0.02]: ") or 0.02)

        except ValueError:
            print("\n[Aviso] Se detectó un valor inválido. Se regresará al menú principal.")
            continue

        ejecutar_simulacion(
            m1, r1, x1, y1, vx1, vy1,
            m2, r2, x2, y2, vx2, vy2,
            e, pasos, dt,
            titulo="Simulación de Colisión 2D (Personalizada)"
        )

    elif opcion == '3':
        print("\nSaliendo de la simulación. ¡Hasta luego!")
        break

    else:
        print("\n[Aviso] Opción no válida. Por favor, ingresa 1, 2 o 3.")