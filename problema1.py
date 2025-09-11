class AFD:
    def __init__(self):
        # Estados
        self.states = {"q0", "q1", "q2", "q3"}
        self.initial_state = "q0"
        self.accepting_states = {"q2", "q3"}  

        # Transiciones (deterministas)
        self.transitions = {
            "q0": {"0": "q1", "1": "q3"},
            "q1": {"1": "q2"},          
            "q2": {"1": "q2", "0": "q1"},  
            "q3": {"0": "q2", "1": "q3"}   
        }

    def process(self, string):
        state = self.initial_state
        recorrido = [state]  
        explicacion = []  # paso a paso

        for i, symbol in enumerate(string, 1):
            if symbol not in {"0", "1"}:
                explicacion.append(f"⚠️ Símbolo '{symbol}' inválido (no pertenece al alfabeto {{0,1}}).")
                return False, recorrido, explicacion  

            if symbol in self.transitions[state]:
                next_state = self.transitions[state][symbol]
                explicacion.append(f"Paso {i}: desde {state} con '{symbol}' → {next_state}")
                state = next_state
                recorrido.append(state)
            else:
                explicacion.append(f"Paso {i}: desde {state} con '{symbol}' → ❌ transición no definida.")
                return False, recorrido, explicacion  

        aceptado = state in self.accepting_states
        if aceptado:
            explicacion.append(f"✔️ Cadena terminada en estado de aceptación: {state}.")
        else:
            explicacion.append(f"❌ Cadena terminada en estado no aceptado: {state}.")
        return aceptado, recorrido, explicacion


# ----------------- PROGRAMA PRINCIPAL -----------------
if __name__ == "__main__":
    afd = AFD()

    print("\n=== AUTÓMATA FINITO DETERMINISTA ===")
    print("Alfabeto: Σ = {0, 1}")
    print("Lenguaje aceptado: ((01 + 10)(11)*0)* (01 + 10)(11)*")
    print("Descripción:")
    print(" - El autómata acepta cadenas que contienen subcadenas '01' o '10',")
    print("   seguidas de repeticiones de '11', y opcionalmente con '0' intercalado.\n")

    while True:
        cadena = input("Digite una cadena con 0s y 1s (o 'salir' para terminar): ").strip()
        if cadena.lower() == "salir":
            print("Programa finalizado.")
            break

        aceptado, recorrido, explicacion = afd.process(cadena)

        print("\n=== RESULTADO ===")
        print(f"Cadena ingresada: {cadena}")
        print("Recorrido de estados:", " -> ".join(recorrido))
        print("\n--- Proceso paso a paso ---")
        for paso in explicacion:
            print(paso)

        if aceptado:
            print(f"\n✅ La cadena '{cadena}' ES ACEPTADA en el lenguaje.\n")
        else:
            print(f"\n❌ La cadena '{cadena}' NO es aceptada en el lenguaje.\n")

