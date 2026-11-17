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

def ejecutar_simulacion(m1, r1, x1, y1, vx1, vy1, m2, r2, x2, y2, vx2, vy2, e, pasos, dt, titulo, mostrar_datos_en_pantalla=False):
    particula_1 = Particula(m=m1, r=r1, r0=[x1, y1], v0=[vx1, vy1])
    particula_2 = Particula(m=m2, r=r2, r0=[x2, y2], v0=[vx2, vy2])
    sistema = SistemaColision(particula_1, particula_2, e=e) 

    historial_p1 = []
    historial_p2 = []
    historial_v1 = [] 
    historial_v2 = [] 

    P_inicial = particula_1.momento_lineal() + particula_2.momento_lineal()
    E_inicial = particula_1.energia_cinetica() + particula_2.energia_cinetica()

    for _ in range(pasos):
        historial_p1.append(particula_1.pos.copy())
        historial_p2.append(particula_2.pos.copy())
        historial_v1.append(particula_1.vel.copy())
        historial_v2.append(particula_2.vel.copy())
        sistema.paso_euler(dt)

    historial_p1 = np.array(historial_p1)
    historial_p2 = np.array(historial_p2)
    historial_v1 = np.array(historial_v1)
    historial_v2 = np.array(historial_v2)

    P_final = particula_1.momento_lineal() + particula_2.momento_lineal()
    E_final = particula_1.energia_cinetica() + particula_2.energia_cinetica()

    print("\n" + "="*50)
    print("              RESULTADOS DE LA SIMULACIÓN              ")
    print("="*50)
    print(f"Momento Lineal Total Inicial: {P_inicial} | Final: {P_final}")
    print(f"Energía Cinética Total Inicial: {E_inicial:.2f} J | Final: {E_final:.2f} J")

    fig, ax = plt.subplots(figsize=(8, 8)) 
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_aspect('equal')
    ax.set_title(titulo)
    ax.grid(True)

    cuerpo1 = plt.Circle(historial_p1[0], particula_1.r, color='blue', label='P1')
    cuerpo2 = plt.Circle(historial_p2[0], particula_2.r, color='red', label='P2')
    ax.add_patch(cuerpo1)
    ax.add_patch(cuerpo2)
    ax.legend(loc="upper right")

    texto_info = ax.text(0.02, 0.98, '', transform=ax.transAxes, verticalalignment='top', 
                         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8), fontsize=9)

    def animar(i):
        cuerpo1.set_center(historial_p1[i])
        cuerpo2.set_center(historial_p2[i])
        
        if mostrar_datos_en_pantalla:
            tiempo_actual = i * dt
            info = f"Tiempo: {tiempo_actual:.2f} s\n"
            info += f"P1 - Pos: ({historial_p1[i][0]:.1f}, {historial_p1[i][1]:.1f}) | Vel: ({historial_v1[i][0]:.1f}, {historial_v1[i][1]:.1f})\n"
            info += f"P2 - Pos: ({historial_p2[i][0]:.1f}, {historial_p2[i][1]:.1f}) | Vel: ({historial_v2[i][0]:.1f}, {historial_v2[i][1]:.1f})"
            texto_info.set_text(info)
            return cuerpo1, cuerpo2, texto_info
            
        return cuerpo1, cuerpo2

    ani = animation.FuncAnimation(fig, animar, frames=pasos, interval=20, blit=False)
    plt.show()

def pedir_valor(mensaje, por_defecto, min_val, max_val, tipo=float):
    prompt = f"{mensaje} ({min_val} a {max_val}): "
    while True:
        entrada = input(prompt).strip()
        if not entrada:
            return por_defecto
        try:
            valor = tipo(entrada)
            if min_val <= valor <= max_val:
                return valor
            else:
                print(f"  [Error] El valor debe estar entre {min_val} y {max_val}.")
        except ValueError:
            print("  [Error] Por favor ingresa un número válido.")


registro_simulaciones = []  

while True:
    print("\n" + "="*50)
    print("             MENÚ PRINCIPAL - COLISIÓN 2D              ")
    print("="*50)
    print("1. Ejecutar simulación con valores por defecto (Ver datos)")
    print("2. Modificar variables por consola y ejecutar simulación")
    print("3. Mostrar fórmulas físicas utilizadas")
    print("4. Mostrar historial de simulaciones realizadas en esta sesión")
    print("5. Salir / Cortar la simulación")
    
    opcion = input("Selecciona una opción (1 al 5): ").strip()

    if opcion == '1':
        print("\nEjecutando simulación con valores por defecto...")
        
        registro_simulaciones.append({
            "Tipo": "Por Defecto",
            "P1": {"m": 2.0, "r": 0.5, "Pos Inicial": (-5.0, 1.0), "Vel Inicial": (3.0, -0.5)},
            "P2": {"m": 3.0, "r": 0.5, "Pos Inicial": (5.0, -0.5), "Vel Inicial": (-2.0, 0.5)},
            "Sistema": {"e": 1.0, "Pasos": 200, "dt": 0.02}
        })

        ejecutar_simulacion(
            m1=2.0, r1=0.5, x1=-5.0, y1=1.0, vx1=3.0, vy1=-0.5,
            m2=3.0, r2=0.5, x2=5.0, y2=-0.5, vx2=-2.0, vy2=0.5,
            e=1.0, pasos=200, dt=0.02,
            titulo="Simulación de Colisión 2D (Por Defecto)",
            mostrar_datos_en_pantalla=True
        )

    elif opcion == '2':
        print("\n" + "="*50)
        print("         MODIFICACIÓN DE VARIABLES POR CONSOLA         ")
        print("="*50)
        print("Presiona ENTER sin escribir nada para utilizar el valor por defecto.\n")
        
        print("--- Partícula 1 ---")
        m1 = pedir_valor("Masa", 2.0, 0.1, 50.0)
        # Cálculo automático del radio asumiendo densidad uniforme en 2D (r proporcional a la raíz de la masa)
        r1 = float(np.sqrt(m1) * 0.353) 
        print(f"  [>] Radio calculado automáticamente: {r1:.2f} m")
        
        x1 = pedir_valor("Posición X inicial", -5.0, -9.0, 9.0)
        y1 = pedir_valor("Posición Y inicial", 1.0, -9.0, 9.0)
        vx1 = pedir_valor("Velocidad X inicial", 3.0, -15.0, 15.0)
        vy1 = pedir_valor("Velocidad Y inicial", -0.5, -15.0, 15.0)

        print("\n--- Partícula 2 ---")
        m2 = pedir_valor("Masa", 3.0, 0.1, 50.0)
        # Cálculo automático del radio para la partícula 2
        r2 = float(np.sqrt(m2) * 0.353)
        print(f"  [>] Radio calculado automáticamente: {r2:.2f} m")
        
        x2 = pedir_valor("Posición X inicial", 5.0, -9.0, 9.0)
        y2 = pedir_valor("Posición Y inicial", -0.5, -9.0, 9.0)
        vx2 = pedir_valor("Velocidad X inicial", -2.0, -15.0, 15.0)
        vy2 = pedir_valor("Velocidad Y inicial", 0.5, -15.0, 15.0)

        print("\n--- Parámetros Generales ---")
        e = pedir_valor("Coeficiente de restitución 'e'", 1.0, 0.0, 1.0)
        pasos = pedir_valor("Número de pasos de simulación", 200, 50, 1000, tipo=int)
        dt = pedir_valor("Paso de tiempo dt", 0.02, 0.001, 0.5)

        registro_simulaciones.append({
            "Tipo": "Personalizada",
            "P1": {"m": m1, "r": r1, "Pos Inicial": (x1, y1), "Vel Inicial": (vx1, vy1)},
            "P2": {"m": m2, "r": r2, "Pos Inicial": (x2, y2), "Vel Inicial": (vx2, vy2)},
            "Sistema": {"e": e, "Pasos": pasos, "dt": dt}
        })

        ejecutar_simulacion(
            m1, r1, x1, y1, vx1, vy1,
            m2, r2, x2, y2, vx2, vy2,
            e, pasos, dt,
            titulo="Simulación de Colisión 2D (Personalizada)",
            mostrar_datos_en_pantalla=True
        )

    elif opcion == '3':
        print("\n" + "="*70)
        print("           FÓRMULAS FÍSICAS UTILIZADAS Y SUS UNIDADES           ")
        print("="*70)
        
        print("1. Energía Cinética (Translacional):")
        print("   Fórmula:   Ec = 0.5 * m * ||v||^2")
        print("   Variables: m = Masa [kg], v = Velocidad [m/s]")
        print("   Resultado: Ec = Energía [Joules (J) o kg·m²/s²]")
        
        print("\n2. Momento Lineal:")
        print("   Fórmula:   P = m * v")
        print("   Variables: m = Masa [kg], v = Velocidad [m/s]")
        print("   Resultado: P = Momento Lineal [kg·m/s]")
        
        print("\n3. Cinemática - Integración de Euler:")
        print("   Fórmula:   Pos_nueva = Pos_actual + v * dt")
        print("   Variables: Pos = Posición [m], v = Velocidad [m/s], dt = Paso de tiempo [s]")
        print("   Resultado: Pos_nueva = Posición actualizada [m]")
        
        print("\n4. Resolución de Colisión (Impulso J):")
        print("   - Distancia entre centros:")
        print("     Fórmula:   d = ||Pos1 - Pos2||")
        print("     Variables: Pos1, Pos2 = Posiciones [m]")
        print("     Resultado: d = Distancia [m]")
        
        print("\n   - Vector Normal (dirección del choque):")
        print("     Fórmula:   n = (Pos1 - Pos2) / d")
        print("     Resultado: n = Vector direccional unitario [Adimensional]")
        
        print("\n   - Magnitud del Impulso:")
        print("     Fórmula:   J = -(1 + e) * (v_rel * n) / (1/m1 + 1/m2)")
        print("     Variables: e = Coef. de restitución [Adimensional], v_rel = Vel. relativa [m/s]")
        print("                m1, m2 = Masas [kg]")
        print("     Resultado: J = Impulso [N·s o kg·m/s]")
        
        print("\n   - Nuevas Velocidades tras el choque:")
        print("     Fórmula:   v1_nueva = v1 + (J / m1) * n")
        print("                v2_nueva = v2 - (J / m2) * n")
        print("     Variables: J = Impulso [kg·m/s], m = Masa [kg], n = Vector [Adim.]")
        print("     Resultado: v_nueva = Velocidad actualizada [m/s]")
        print("="*70)

    elif opcion == '4':
        print("\n" + "="*50)
        print("            HISTORIAL DE DATOS DE LA SESIÓN            ")
        print("="*50)
        if len(registro_simulaciones) == 0:
            print("Aún no se ha ejecutado ninguna simulación en esta sesión.")
        else:
            for idx, sim in enumerate(registro_simulaciones, 1):
                print(f"--- Simulación #{idx} ({sim['Tipo']}) ---")
                print(f"P1: Masa={sim['P1']['m']}, Radio={sim['P1']['r']}, "
                      f"Pos0={sim['P1']['Pos Inicial']}, Vel0={sim['P1']['Vel Inicial']}")
                print(f"P2: Masa={sim['P2']['m']}, Radio={sim['P2']['r']}, "
                      f"Pos0={sim['P2']['Pos Inicial']}, Vel0={sim['P2']['Vel Inicial']}")
                print(f"Sistema: Coef Restit (e)={sim['Sistema']['e']}, "
                      f"Pasos={sim['Sistema']['Pasos']}, dt={sim['Sistema']['dt']}\n")
        print("="*50)

    elif opcion == '5':
                print("\nSaliendo de la simulación. ¡Hasta luego!")
                break

    else:
        print("\n[Aviso] Opción no válida. Por favor, ingresa un número del 1 al 5.")
