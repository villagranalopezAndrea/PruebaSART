# Importamos las bibliotecas necesarias
from psychopy import visual, core, event, monitors  #Img,tempo,,,
import random           #Módulo para poder generar secuencias de forma aleatoria
import os               #Módulo del Sistema Operativo
import pyautogui        #Obtener resolución del monitor en donde se correrá
import time             #Para medir el tiempo total de la prueba (tomando en cuenta pausas)

# Crear directorio para guardar respuestas 
if not os.path.exists("datos"):
    os.makedirs("datos")

# Obtener la resolución en pixeles del monitor actual
screen_width, screen_height = pyautogui.size()

# Crear y configurar monitor
mon = monitors.Monitor('testMonitor')
mon.setWidth(35)  # ancho del monitor en cm
mon.setDistance(30)  # distancia de visualización en cm
mon.setSizePix([screen_width, screen_height])  # resolución de pantalla
mon.save()  # Guardar la configuración del monitor

# Configurar resolución, color y tamaño de la ventana
ventana = visual.Window([screen_width, screen_height], color="white", fullscr=True, monitor=mon)

# Cargar imágenes de números + máscaras (TODAS tienen que estar en la misma carpeta que el .py
# altura_estimulo_norm = 4.7 / (21.5625 / 2) = 0.436
height_stims = 0.436 / 0.72; #El font size sólo mide le 70% del total de espacio de altura.Calcular altura total

one_text = visual.TextStim(ventana, text="1", font="Arial", color="white", bold=True, height=.45) # Go 1
two_text = visual.TextStim(ventana, text="2", font="Arial", color="white", bold=True, height=.45) # Go 2
three_text = visual.TextStim(ventana, text="3", font="Arial", color="white", bold=True, height=.45) # Estímulo No-Go
four_text = visual.TextStim(ventana, text="4", font="Arial", color="white", bold=True, height=.45)  # Go 4
five_text = visual.TextStim(ventana, text="5", font="Arial", color="white", bold=True, height=.45) # Go 5
six_text = visual.TextStim(ventana, text="6", font="Arial", color="white", bold=True, height=.45) #  Go 6
seven_text = visual.TextStim(ventana, text="7", font="Arial", color="white", bold=True, height=.45) # Go 7
eight_text = visual.TextStim(ventana, text="8", font="Arial", color="white", bold=True, height=.45) # Go 8
nine_text = visual.TextStim(ventana, text="9", font="Arial", color="white", bold=True, height=.45) # Go 9

mas_text = visual.TextStim(ventana, text="+", font="Arial", color="white", height=.12)  #Estímulo de máscara

# Crear un diccionario para acceder a imgs por los números 1-9
stimsNum = {
    1: one_text,
    2: two_text,
    3: three_text,
    4: four_text,
    5: five_text,
    6: six_text,
    7: seven_text,
    8: eight_text,
    9: nine_text,
}

#Cargar textos de instrucciones de la prueba
instruction_text = visual.TextStim(ventana, text="Instrucciones", color="black", height=0.1, pos=(0, 0.6))#Altura[0-1] Posición [-1,1] [centro, arriba]
instruction_text2 = visual.TextStim(ventana, text="Presiona la tecla ESPACIO lo más rápido que puedas para todos los números excepto el 3", color="black", height=0.07, pos=(0, 0))
instruction_text3 = visual.TextStim(ventana, text="Presiona la tecla ENTER para iniciar la prueba de familiarización", color="black", height=0.05, pos=(0, -0.6))
# Crear espacio de texto ID participante y cargar línea ________
participant_text = visual.TextStim(ventana, text="Escribe tu inciales:", color="black", height=0.1, pos=(0, 0.2))
participant_subtext = visual.TextStim(ventana, text="Presiona la tecla ENTER al finalizar", color="black", height=0.05, pos=(0, -0.6))
id_box = visual.TextStim(ventana, text="", font="Arial", color="black", height=0.1, pos=(0, 0))
line_img = visual.ImageStim(ventana, image="linea.png", size=(0.9, 0.3))
line_img.pos = (0, -0.06)       # Establecer Posición de la línea donde escribir ID

#Duración de los estímulos (en seg)
t_num = 0.3 #300ms
t_masc = 0.8 #800ms
t_total_ensayo = t_num+t_masc #1100ms

# Cálculo de número de ensayos 
numsNo3 = [1, 2, 4, 5, 6, 7, 8, 9] #Digitos del 1-9 excepto el 3
sequence = []    #Lista para guardar la secuencia de números que se mostrarán en la prueba
sequence_Fam = [] #Lista fase de familiarización
t_total_prueba = 360 #6 minutos * 60 segundos
t_total_prueba_Fam = 77 #1.1 (tiempo ensayo) * 70 ensayos (60 a 80 ensayos)
porcentaje_Num3 = .13 #13 porciento

#Crear Fn para pausar la ejecución hasta que se presione la tecla ENTER o ESCAPE
def wait_enter_scape():
    event.waitKeys(keyList=['return','escape']) 
    if 'escape' in event.getKeys():
        ventana.close()
        core.quit()

def calculate_trials(t_total_prueba, t_total_ensayo, porcentaje_Num3, numsNo3, sequence):
    num_ensayos = round(t_total_prueba / t_total_ensayo) #327

    reps_num3 = round(num_ensayos * porcentaje_Num3) #Repeticiones num3 para ser el 13% de los ensayos = 43
    num_ensayos_restantes = num_ensayos - reps_num3  # 287 (1, 2, 4, 5, 6, 7, 8, 9)

    reps_numNo3 = round(num_ensayos_restantes / len(numsNo3)) #287 / 8 = 36

    vnum3 = [3]*reps_num3 #43 ensayos del #3
    sequence.extend(vnum3) #Agregar los 43 número
    return reps_numNo3, reps_num3, sequence

# Usar la función para calcular el número de ensayos para la prueba y la fase de familiarización
reps_numNo3, reps_num3, sequence = calculate_trials(t_total_prueba, t_total_ensayo, porcentaje_Num3, numsNo3, sequence)
reps_numNo3_Fam, reps_num3_Fam, sequence_Fam = calculate_trials(t_total_prueba_Fam, t_total_ensayo, porcentaje_Num3, numsNo3, sequence_Fam)

# Función para generar la secuencia de la prueba (324 ensayos) -> 6 minutos
def generate_trial_sequence(numsNo3, reps_numNo3, sequence):
    for n in numsNo3: 
        sequence.extend([n]*reps_numNo3) #Genera una lista con todas los dígitos 1-9
    random.shuffle(sequence) #Aleatoriza todos los 324 números generados
    return sequence

# Esperar a que el usuario ingrese su nombre
participant = ""
while participant == "":
    participant_text.draw() #Mostrar la instrucción de ingresar ID
    participant_subtext.draw() #Mostrar la instrucción para seguir con la prueba
    id_box.draw()           #Mostrar espacio para ingresar ID
    line_img.draw()         #Mostrar línea donde escribir
    ventana.flip()          #Actualiza la ventana mostrando todo lo dibujado desde el último flip
    
    keys = event.getKeys() # Capturar teclas presionadas (para el ID)
    
    # Procesar la entrada
    for key in keys:
        match key:
            case 'return': # Confirmar ID completo (con tecla de enter)
                participant = id_box.text
            case 'escape': # Salir si se presiona ESC
                ventana.close()
                core.quit()
            case 'backspace': # Borrar un carácter (por si se equivoca)
                id_box.text = id_box.text[:-1]
            case _: # Agregar la tecla presionada al ID
                id_box.text += key.upper()    #upper para hacerlas mayúsculas
    
    # Volver a dibujar el texto con el ID actualizado
    participant_text.draw()
    participant_subtext.draw()
    id_box.draw()
    line_img.draw()
    ventana.flip()

# Instrucciones iniciales
instruction_text.draw()
instruction_text2.draw()
instruction_text3.draw()          # Dibujar las instrucciones
ventana.flip()                    # Mostrar instrucciones anteriores
wait_enter_scape()                # Esperar a que el usuario presione ENTER o ESCAPE para continuar

start_t = time.time()  #Obtener hora de la computadora
start_clock_hour = time.strftime("%H:%M:%S")#Mostrarlo en formato 24hrs/min/seg

# Variables de prueba puntuación y respuestas
sequence = generate_trial_sequence(numsNo3, reps_numNo3, sequence) #Generar Lista de 331 números
total_trials = len(sequence)         #Num de Ensayos 331
sequence_Fam = generate_trial_sequence(numsNo3, reps_numNo3_Fam, sequence_Fam) #Generar Lista de 73 números
total_trials_Fam = len(sequence_Fam) #Num de Ensayos 73

def run_trials(sequence, reps_num3):
    responses = []       #1 si presionó, 0 si no
    reaction_times = []  #RT en seg
    good_Hits = []       #Aciertos (if num = 3, res=0) else res=1 (True/False)

    # Definir el temporizador
    clock = core.Clock()

    # Comienza la prueba
    ventana.color = "gray"
    ventana.flip()          # actualiza el fondo 
    escapePushed = False #variable para salir del for
    for trial_number, number in enumerate(sequence): #regresa [#trial,dígito]
        stimulus = stimsNum[number]
        stimulus.draw()
        ventana.flip()
        clock.reset()   # Iniciar temporizador para el RT ( o hasta que responda)
        
        #Incializar valores de variables
        response = 0  # No respuesta
        rt = None  # Tiempo de reacción
        
        # Esperar una respuesta durante el tiempo def para el dígito t_num(300ms)
        #Con waitkeys por defecto, la 1er tecla termina la espera. Devuelve 0 o 1 tupla
        while clock.getTime() < t_num:
            keys = event.getKeys(keyList=["space", "escape"], timeStamped=clock)
            if keys:
                match keys[0][0]:
                    case 'escape':
                        escapePushed = True
                        break
                    case 'space':
                        response = 1 # Presionó la tecla
                        rt = keys[0][1]  # Se accede al 2ndo elemento de la tupla para
                                    # Guardar el Tiempo de reacción [nombre de la tecla,rt]
        if escapePushed:
            break
        
        #Mostrar máscara
        mas_text.draw()
        ventana.flip()
        
        #Guardar tiempo justo cuando se muestra máscara
        t_masc_Drew = clock.getTime()
        t_masc_Fin = t_masc_Drew + t_masc #Desde que se dibuja + 800ms
        
        while clock.getTime() < t_masc_Fin:
            keys2 = event.getKeys(keyList=["space", "escape"], timeStamped=clock)
            if keys2:
                match keys2[0][0]:
                    case 'escape':
                        escapePushed = True
                        break
                    case 'space':
                        response = 1 # Presionó la tecla
                        rt = keys2[0][1]  # Se accede al 2ndo elemento de la tupla para
        if escapePushed:
            break
        
        # Determinar las respuestas correctas
        if number == 3: #Estímulo No-Go
            correct = (response == 0)
        else:           #Estímulos Go
            correct = (response == 1)
        
        # Almacenar las respuestas
        good_Hits.append(correct)
        responses.append(response)
        reaction_times.append(rt)
        
    # Guardar los resultados en un archivo de texto
    # Configurar el nombre del archivo de salida
    output_file = f"datos/{participant}_resultados.txt"
    #Revisar si el archivo ya existe para evitar sobreescribirlo
    existing_file = os.path.isfile(output_file)
    with open(output_file, "a", encoding="utf-8-sig") as f:
        if not existing_file:  #Sólo entonces escribir los encabezados
            f.write("Prueba de Familiarización\nTrial\tDígito\tKeyRes\tRT\tCorrecto(1=Sí)\n")  # Escribimos los encabezados
        else:
            f.write("\nPrueba principal\n")
        # Guardamos cada uno de los ensayos con las respuestas y tiempos de reacción
        for i in range(len(good_Hits)):
            rt_str = f"{reaction_times[i]:.3f}" if reaction_times[i] is not None else "None"
            f.write(f"{i+1}\t{sequence[i]}\t{responses[i]}\t{rt_str}\t{int(good_Hits[i])}\n")
    
    # Mostrar el resultado   
    total_Hits = sum(good_Hits)
    t_total_prueba_Real = (len(sequence)*t_total_ensayo)/60 #331*1.1 / 60seg = 6.07 minutos
    porcentaje_Real_Num3 = (reps_num3 / len(sequence))*100 #43/331*100 = 12.99%
    return total_Hits, porcentaje_Real_Num3, t_total_prueba_Real, output_file

#Ejecutar la fase de familiarización      
total_Hits_Fam, porcentaje_Real_Num3_Fam, t_total_prueba_Real, output_file_Fam = run_trials(sequence_Fam, reps_num3_Fam) #Regresar todos lo valores para desempaquetar el vector
t_Fam = round(t_total_prueba_Real,2)
#Mostrar mensaje de transición a la prueba principal
ventana.color = "white" 
ventana.flip()          # actualiza el fondo
trans_text = visual.TextStim(ventana, text=f"Fin de la prueba de familiarización", color="black", height=0.1,)
trans_text2 = visual.TextStim(ventana, text="Presiona la tecla ENTER para iniciar la prueba principal", color="black", height=0.05, pos=(0, -0.6))
trans_text.draw()
trans_text2.draw()
ventana.flip()    
wait_enter_scape()    

# Ejecutar la prueba SART
total_Hits, porcentaje_Real_Num3, t_total_prueba_Real, output_file = run_trials(sequence, reps_num3)

final_t = time.time()  #Obtener hora de la computadora
final_clock_hour = time.strftime("%H:%M:%S") #Cambiar formato
tt_execution = (final_t - start_t) / 60 #Tiempo total en minutos

t_total_prueba_Real = round(t_total_prueba_Real,2)
#Mostrar resultados prueba
ventana.color = "white" 
ventana.flip()          # actualiza el fondo
final_text = visual.TextStim(ventana, text=f"Fin de la prueba :)", color="black", height=0.1,)
final_text2 = visual.TextStim(ventana, text=f"Aciertos: {total_Hits} de {total_trials}", color="black", height=0.05, pos=(0,0.6))
final_text3 = visual.TextStim(ventana, text=f"Presiona la tecla ENTER para terminar el experimento", color="black", height=0.05, pos=(0,-0.6))
final_text.draw()
final_text2.draw()
final_text3.draw()
ventana.flip()

output_file = f"datos/{participant}_resultados.txt"
with open(output_file, "a", encoding="utf-8-sig") as f:
    f.write(f"\nResumen\n")
    f.write(f"Porcentaje de visualización #3:  {round(porcentaje_Real_Num3_Fam,2)} y {round(porcentaje_Real_Num3,2)}%\n")
    f.write(f"Hora de inicio y fin:  {start_clock_hour} ->  {final_clock_hour}\n")
    f.write(f"Tiempo total ensayos: {t_Fam} + {t_total_prueba_Real} = {t_Fam + t_total_prueba_Real}min\n")
    f.write(f"Tiempo total de la sesión: {round(tt_execution, 2)} min")

wait_enter_scape()
ventana.close() #Cerrar ventana
core.quit() #Cerrar programa