#Problema #2 // utiliando el metodo por Automatas Finitos Deterministas (AFD)
#se desarrollo basandonos en la descripcion del documento presentado para seguir la logica 
#y buscar brindar el desarrollo del ejercicio

#                                \\\  Elaborado por Nicolas Ballesteros ///

# se definieron variables para realizar las operaciones siguiendo la estructura logica del ejercicio

def afd_problema2(cadena):
    """
    AFD para el lenguaje:
    - Número de 'a' par.
    - No debe contener la subcadena 'bc'.
    """
# se sigue la descripcion a detalle de acuerdo al documento
    # Estados representados como tuplas: (paridad_a, ultimo_simbolo)
    # paridad_a: "par" o "impar"
    # ultimo_simbolo: "nulo", "a", "b", "c"
    # Estado de error: "trampa"

    estado = ("par", "nulo")  # Estado inicial
    recorrido = [estado]

    for simbolo in cadena:
        paridad, ultimo = estado

        # Si ya estamos en trampa, nos quedamos allí
        if estado == "trampa":
            recorrido.append("trampa")
            continue

        # Verificación del alfabeto
        if simbolo not in {"a", "b", "c"}:
            print(f"⚠️ Símbolo inválido '{simbolo}'. Solo se permiten caracteres {a, b, c}.")
            return False, recorrido

        # Actualizar paridad si el símbolo es 'a'
        if simbolo == "a":
            if paridad == "par":
                paridad = "impar"
            else:
                paridad = "par"

        # Verificar si se forma la subcadena "bc"
        if ultimo == "b" and simbolo == "c":
            estado = "trampa"
            recorrido.append(estado)
            continue

        # Actualizar el último símbolo
        estado = (paridad, simbolo)
        recorrido.append(estado)

    # Aceptación: estado no es trampa y paridad = par
    if estado != "trampa" and estado[0] == "par":
        return True, recorrido
    else:
        return False, recorrido


# Programa principal
if __name__ == "__main__":
    cadena = input("👉 Ingrese una cadena con caracteres del alfabeto {a, b, c} (ejemplo: aabac): ").strip()
    valido, recorrido = afd_problema2(cadena)

    print("\n=== Proceso del AFD ===")
    for i, estado in enumerate(recorrido):
        print(f" Paso {i}: {estado}")

    if valido:
        print("\n✅ La cadena es ACEPTADA por el lenguaje.")
    else:
        print("\n❌ La cadena NO es aceptada por el lenguaje.")
