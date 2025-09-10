import tkinter as tk
from tkinter import simpledialog, scrolledtext

# Mapa Morse
MORSE_CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..',
    '0': '-----', '1': '.----','2': '..---','3': '...--',
    '4': '....-','5': '.....','6': '-....','7': '--...',
    '8': '---..','9': '----.'
}

def generar_codigo(palabra):
    palabra = palabra.upper()
    codigo = """const int led = 13; // LED
const int dot = 250; // duración de un punto en ms

void setup() { pinMode(led, OUTPUT); }
void blinkDot() { digitalWrite(led, HIGH); delay(dot); digitalWrite(led, LOW); delay(dot); }
void blinkDash() { digitalWrite(led, HIGH); delay(dot*3); digitalWrite(led, LOW); delay(dot); }

void loop() {
"""
    for i, letra in enumerate(palabra):
        if letra == ' ':
            codigo += "  delay(dot*7); // espacio entre palabras\n"
            continue
        if letra not in MORSE_CODE:
            continue
        for simbolo in MORSE_CODE[letra]:
            codigo += "  blinkDot();\n" if simbolo == '.' else "  blinkDash();\n"
        if i < len(palabra)-1:
            codigo += "  delay(dot*3); // espacio entre letras\n"
    codigo += "  while(1); // detener loop\n}"
    return codigo

# Función para copiar al portapapeles
def copiar_al_portapapeles(texto, root):
    root.clipboard_clear()
    root.clipboard_append(texto)
    root.update()  # actualizar portapapeles

# Interfaz Tkinter
root = tk.Tk()
root.withdraw()  # ocultar ventana principal

# Popup para ingresar palabra
palabra = simpledialog.askstring("Entrada", "Escribe la palabra para convertir a Morse:")

if palabra:
    codigo_final = generar_codigo(palabra)

    # Crear ventana para mostrar código y botón copiar
    ventana = tk.Toplevel()
    ventana.title("Código Arduino")

    st = scrolledtext.ScrolledText(ventana, width=80, height=25)
    st.pack(padx=10, pady=10)
    st.insert(tk.END, codigo_final)
    st.config(state=tk.DISABLED)  # evitar edición

    boton_copiar = tk.Button(ventana, text="Copiar al portapapeles",
                             command=lambda: copiar_al_portapapeles(codigo_final, ventana))
    boton_copiar.pack(pady=5)

    ventana.mainloop()
