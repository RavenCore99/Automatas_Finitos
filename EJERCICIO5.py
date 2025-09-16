"""
Finite Automata Implementation - Regular Expression Problem
Expression: (((0 + 10)(10)*(11 + 0)) + 11)(0 + 1)*

Autorr: [Your Name]
Date: [Current Date]
Course: Automata Theory
"""

class FiniteAutomaton:
    """
    Base class for Finite Automaton implementation
    """
    
    def __init__(self, states, alphabet, transitions, initial_state, accepting_states):
        """
        Initialize the finite automaton
        
        Args:
            states (set): Set of all states
            alphabet (set): Input alphabet
            transitions (dict): Transition function as nested dictionary
            initial_state (str): Initial state
            accepting_states (set): Set of accepting states
        """
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.accepting_states = accepting_states
    
    def process_string(self, input_string):
        """
        Process an input string through the automaton
        
        Args:
            input_string (str): Input string to process
            
        Returns:
            tuple: (bool, str, list) - (is_accepted, final_state, path)
        """
        current_state = self.initial_state
        path = [current_state]
        
        # Process each symbol in the input string
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False, "Invalid symbol", path
            
            if current_state in self.transitions and symbol in self.transitions[current_state]:
                current_state = self.transitions[current_state][symbol]
                path.append(current_state)
            else:
                path.append("∅")
                return False, "No transition defined", path
        
        # Check if final state is accepting
        is_accepted = current_state in self.accepting_states
        return is_accepted, current_state, path
    
    def is_accepted(self, input_string):
        """
        Check if a string is accepted by the automaton
        
        Args:
            input_string (str): Input string to check
            
        Returns:
            bool: True if string is accepted, False otherwise
        """
        accepted, _, _ = self.process_string(input_string)
        return accepted
    
    def print_transition_table(self):
        """
        Print the transition table in a formatted way
        """
        print("Estado\t", end="")
        for symbol in sorted(self.alphabet):
            print(f"{symbol}\t", end="")
        print()
        print("-" * 40)
        
        for state in sorted(self.states):
            marker = "→ " if state == self.initial_state else "  "
            marker += "* " if state in self.accepting_states else "  "
            print(f"{marker}{state}\t", end="")
            
            for symbol in sorted(self.alphabet):
                if state in self.transitions and symbol in self.transitions[state]:
                    print(f"{self.transitions[state][symbol]}\t", end="")
                else:
                    print("∅\t", end="")
            print()


class RegexAutomaton(FiniteAutomaton):
    """
    Automaton for the regular expression: (((0 + 10)(10)*(11 + 0)) + 11)(0 + 1)*
    
    This automaton accepts strings that:
    1. Start with pattern ((0 + 10)(10)*(11 + 0)) OR start with "11"
    2. Followed by any sequence of 0s and 1s: (0 + 1)*
    
    State meanings:
    - q0: Initial state, decides the path based on first symbol
    - q1: After reading "0", can accept directly or continue with "10" pattern
    - q2: After reading first "1", looking for second "1" to form "11"
    - q3: Processing "10" sequence, allows repetition
    - q4: After "11", can terminate or continue
    - q5: Intermediate state after "111"
    - q6: Final accepting state, accepts any continuation
    """
    
    def __init__(self):
        # Define automaton components
        states = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6'}
        alphabet = {'0', '1'}
        transitions = {
            'q0': {'0': 'q1', '1': 'q2'},  # Initial choice: 0→q1, 1→q2
            'q1': {'0': 'q6', '1': 'q3'},  # After "0": 0→accept, 1→process "10"
            'q2': {'1': 'q4'},             # After "1": need "1" for "11"
            'q3': {'0': 'q1'},             # In "10" pattern: 0→back to q1
            'q4': {'0': 'q6', '1': 'q5'},  # After "11": 0→accept, 1→continue
            'q5': {'0': 'q6', '1': 'q6'},  # Intermediate: any→accept
            'q6': {'0': 'q6', '1': 'q6'}   # Final: accept any continuation
        }
        initial_state = 'q0'
        accepting_states = {'q6'}
        
        super().__init__(states, alphabet, transitions, initial_state, accepting_states)


def test_automaton(automaton, test_cases, expression):
    """
    Test an automaton with a set of test cases
    
    Args:
        automaton: FiniteAutomaton instance to test
        test_cases (list): List of tuples (string, expected_result)
        expression (str): Regular expression for display
    """
    print(f"\n{'='*80}")
    print(f"PROBANDO AUTÓMATA PARA: {expression}")
    print(f"{'='*80}")
    
    print("\n📊 TABLA DE TRANSICIONES:")
    automaton.print_transition_table()
    print(f"\nEstado inicial: {automaton.initial_state}")
    print(f"Estados de aceptación: {automaton.accepting_states}")
    
    print(f"\n🧪 RESULTADOS DE PRUEBAS:")
    print("-" * 80)
    print(f"{'Cadena':<15} {'Esperado':<10} {'Obtenido':<10} {'Estado'}")
    print("-" * 80)
    
    all_correct = True
    for test_string, expected in test_cases:
        result = automaton.is_accepted(test_string)
        _, final_state, _ = automaton.process_string(test_string)
        status = "✅" if result == expected else "❌"
        display_string = f'"{test_string}"' if test_string != "" else "ε"
        expected_text = "ACEPTA" if expected else "RECHAZA"
        result_text = "ACEPTA" if result else "RECHAZA"
        
        if result != expected:
            all_correct = False
        
        print(f"{display_string:<15} {expected_text:<10} {result_text:<10} {status}")
    
    accuracy = "🎉 TODAS CORRECTAS" if all_correct else "⚠️  HAY ERRORES"
    print("-" * 80)
    print(f"RESULTADO GENERAL: {accuracy}")
    
    return all_correct


def demonstrate_string_processing(automaton, test_string, show_details=True):
    """
    Demonstrate step-by-step processing of a string
    
    Args:
        automaton: FiniteAutomaton instance
        test_string (str): String to process
        show_details (bool): Whether to show detailed step-by-step processing
    """
    print(f"\n{'='*60}")
    print(f"PROCESAMIENTO PASO A PASO DE: '{test_string}'")
    print(f"{'='*60}")
    
    accepted, final_state, path = automaton.process_string(test_string)
    
    if show_details:
        current_state = automaton.initial_state
        print(f"Estado inicial: {current_state}")
        print("-" * 40)
        
        for i, symbol in enumerate(test_string):
            if i + 1 < len(path):
                next_state = path[i + 1]
                print(f"Paso {i+1:2d}: Leer '{symbol}' → {current_state} → {next_state}")
                current_state = next_state
                
                # Check if we hit a trap state
                if next_state == "∅":
                    print(f"         ⚠️  No hay transición definida desde {path[i]} con '{symbol}'")
                    break
            else:
                print(f"Paso {i+1:2d}: Error en el procesamiento")
                break
        
        print("-" * 40)
    
    is_accepted = final_state in automaton.accepting_states if final_state != "∅" else False
    result_icon = "✅" if is_accepted else "❌"
    result_text = "ACEPTADA" if is_accepted else "RECHAZADA"
    
    print(f"Estado final: {final_state}")
    print(f"Camino completo: {' → '.join(path)}")
    print(f"Resultado: {result_icon} La cadena es {result_text}")
    
    return is_accepted


def analyze_regex_components():
    """
    Analyze the components of the regular expression
    """
    print(f"\n{'='*80}")
    print("ANÁLISIS DE LA EXPRESIÓN REGULAR")
    print(f"{'='*80}")
    print("Expresión: (((0 + 10)(10)*(11 + 0)) + 11)(0 + 1)*")
    print()
    print("🔍 DESCOMPOSICIÓN:")
    print("   1. ((0 + 10)(10)*(11 + 0)) - Primera alternativa principal")
    print("      • (0 + 10) - Comienza con '0' o '10'")
    print("      • (10)* - Seguido de cero o más repeticiones de '10'")
    print("      • (11 + 0) - Termina con '11' o '0'")
    print()
    print("   2. 11 - Segunda alternativa principal")
    print("      • Simplemente la cadena '11'")
    print()
    print("   3. (0 + 1)* - Sufijo opcional")
    print("      • Cualquier secuencia de 0s y 1s (incluyendo vacía)")
    print()
    print("🎯 EJEMPLOS DE PATRONES ACEPTADOS:")
    print("   • '00...' - Empieza con '0', termina con '0', seguido de cualquier cosa")
    print("   • '011...' - Empieza con '0', termina con '11', seguido de cualquier cosa")
    print("   • '1011...' - Empieza con '10', termina con '11', seguido de cualquier cosa")
    print("   • '11...' - Directamente '11' seguido de cualquier cosa")


def main():
    """
    Main function to test the regex automaton
    """
    print("🤖 IMPLEMENTACIÓN DE AUTÓMATA FINITO DETERMINISTA")
    print("📚 Curso: Lenguajes y Autómatas")
    print("📋 Ejercicio: Construcción de AFD desde Expresión Regular")
    print(f"{'='*80}")
    
    # Analyze the regular expression components
    analyze_regex_components()
    
    # Create automaton instance
    regex_automaton = RegexAutomaton()
    
    # Comprehensive test cases
    test_cases = [
        # Basic acceptance cases
        ("00", True),          # (0)(0) pattern
        ("011", True),         # (0)(11) pattern  
        ("110", True),         # (11)(0) pattern
        ("111", True),         # (11)(1) pattern
        ("1111", True),        # (11)(11) pattern
        
        # Pattern with repetitions
        ("10100", True),       # (10)(10)(0) pattern
        ("101011", True),      # (10)(10)(11) pattern
        ("10101010110", True), # Complex valid pattern
        
        # Empty and single characters
        ("", False),           # Empty string
        ("0", False),          # Single '0' - incomplete
        ("1", False),          # Single '1' - incomplete
        
        # Invalid patterns
        ("01", False),         # Starts with '0' but ends with '1' (invalid)
        ("10", False),         # Just '10' without proper ending
        ("101", False),        # '10' + '1' (invalid ending)
        ("1001", False),       # Invalid pattern
        ("0110", False),       # Invalid pattern
        ("010", False),        # Invalid pattern
        
        # Edge cases
        ("000", True),         # (0)(0)(0) - valid continuation
        ("1100", True),        # (11)(00) - valid continuation
        ("11010101", True),    # (11) + continuation
        ("001010", True),      # (00) + continuation
        
        # Complex valid cases
        ("10101100101", True), # Complex valid pattern
        ("1110101010", True),  # (111) + continuation
        ("000111000", True),   # (00) + continuation
        
        # Complex invalid cases
        ("101010", False),     # Ends in incomplete state
        ("010101", False),     # Invalid pattern
        ("100110", False),     # Invalid transition
    ]
    
    # Test the automaton
    all_tests_passed = test_automaton(regex_automaton, test_cases, 
                                     "(((0 + 10)(10)*(11 + 0)) + 11)(0 + 1)*")
    
    # Demonstrate step-by-step processing for key examples
    print(f"\n{'='*80}")
    print("DEMOSTRACIONES DETALLADAS")
    print(f"{'='*80}")
    
    demo_strings = ["00", "110", "1111", "10100", "01", "101010"]
    for demo_string in demo_strings:
        demonstrate_string_processing(regex_automaton, demo_string, show_details=True)
    
    # Interactive testing section
    print(f"\n{'='*80}")
    print("🎮 MODO INTERACTIVO - PRUEBA TUS PROPIAS CADENAS")
    print(f"{'='*80}")
    
    while True:
        try:
            print(f"\nExpresión regular: (((0 + 10)(10)*(11 + 0)) + 11)(0 + 1)*")
            print("Ingresa una cadena para probar (solo 0s y 1s), o 'quit' para salir:")
            
            user_input = input("► Cadena: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'salir', 'q']:
                print("👋 ¡Hasta luego!")
                break
            
            # Validate input
            if not all(c in "01" for c in user_input):
                print("⚠️  Entrada inválida! Usa solo 0s y 1s.")
                continue
            
            # Process the string
            print(f"\n{'🔍 ANÁLISIS':<20}")
            print("-" * 40)
            
            result = demonstrate_string_processing(regex_automaton, user_input, show_details=False)
            
            # Additional analysis
            accepted, final_state, path = regex_automaton.process_string(user_input)
            
            print(f"\n📊 RESUMEN:")
            display_string = f'"{user_input}"' if user_input else "ε (cadena vacía)"
            status_icon = "✅" if result else "❌"
            status_text = "PERTENECE" if result else "NO PERTENECE"
            
            print(f"   Cadena analizada: {display_string}")
            print(f"   Resultado: {status_icon} {status_text} al lenguaje")
            print(f"   Camino de estados: {' → '.join(path)}")
            
            if result:
                print(f"   🎉 La cadena es aceptada por el autómata")
            else:
                print(f"   ⛔ La cadena es rechazada por el autómata")
                
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Final summary
    print(f"\n{'='*80}")
    print("📈 RESUMEN FINAL")
    print(f"{'='*80}")
    print(f"🔬 Total de pruebas realizadas: {len(test_cases)}")
    print(f"✅ Pruebas exitosas: {'Todas' if all_tests_passed else 'Algunas fallaron'}")
    print(f"🤖 El autómata está {'✅ FUNCIONANDO CORRECTAMENTE' if all_tests_passed else '❌ CON ERRORES'}")
    print(f"📝 Expresión regular implementada: (((0 + 10)(10)*(11 + 0)) + 11)(0 + 1)*")
    print(f"🎯 Estados del autómata: 7 estados (q0 a q6)")
    print(f"🔤 Alfabeto: {{0, 1}}")
    print(f"✨ Estado final: {{q6}}")


if __name__ == "__main__":
    main()