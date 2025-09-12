#Problema #3 // utiliando el metodo por Automatas Finitos Deterministas (AFD)
#se desarrollo basandonos en la descripcion del documento presentado para seguir la logica 
#y buscar brindar el desarrollo del ejercicio

#                                \\\  Elaborado por Nicolas Ballesteros ///


def verificar_cadena(cadena):
    # Contadores
    num_0 = cadena.count("0")
    num_1 = cadena.count("1")

    # Caso 1: No hay ningún 1
    if num_1 == 0:
        if num_0 % 2 == 0:
            return True, "✅ Aceptada: No tiene '1' y contiene un número par de '0'."
        else:
            return False, "❌ Rechazada: No tiene '1', pero el número de '0' es impar."

    # Caso 2: Número par de '1's mayor que 0
    if num_1 % 2 == 0 and num_1 > 0:
        if num_0 % 2 == 1:
            return True, "✅ Aceptada: Tiene un número par de '1' y termina con un número impar de '0'."
        else:
            return False, "❌ Rechazada: Tiene un número par de '1', pero el número de '0' es par."

    # Caso 3: Número impar de '1's
    if num_1 % 2 == 1:
        if num_0 % 2 == 0:
            return True, "✅ Aceptada: Tiene un número impar de '1' y termina con un número par de '0'."
        else:
            return False, "❌ Rechazada: Tiene un número impar de '1', pero el número de '0' es impar."

    return False, "❌ Rechazada: No cumple con ninguna condición."


def simular_automata(cadena):
    print("\n🔎 Proceso del autómata:")
    estado = "q0"  # estado inicial
    contador_0, contador_1 = 0, 0

    for i, simbolo in enumerate(cadena, start=1):
        if simbolo == "0":
            contador_0 += 1
        elif simbolo == "1":
            contador_1 += 1

        # Mostrar estado actual
        print(f" Paso {i}: leído '{simbolo}' → total 0s = {contador_0}, total 1s = {contador_1}")

    return verificar_cadena(cadena)


def main():
    print("=== Autómata Finito para el Problema 3 ===")
    cadena = input("Ingrese la cadena (alfabeto {0,1}): ").strip()

    # Validar que solo tenga 0 y 1
    if not set(cadena).issubset({"0", "1"}):
        print("⚠️ Error: La cadena solo debe contener '0' y '1'.")
        return

    aceptada, mensaje = simular_automata(cadena)
    print("\n📌 Resultado final:", mensaje)


if __name__ == "__main__":
    main()


