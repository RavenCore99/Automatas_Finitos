"""
Finite Automata Implementation - Problem 4
Languages: L1 = {(01)^n | n >= 0}, L2 = {(10)^n | n >= 0}, L3 = L1 ∪ L2

Author: [Your Name]
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
            tuple: (bool, str) - (is_accepted, final_state)
        """
        current_state = self.initial_state
        
        # Process each symbol in the input string
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False, "Invalid symbol"
            
            if current_state in self.transitions and symbol in self.transitions[current_state]:
                current_state = self.transitions[current_state][symbol]
            else:
                return False, "No transition defined"
        
        # Check if final state is accepting
        is_accepted = current_state in self.accepting_states
        return is_accepted, current_state
    
    def is_accepted(self, input_string):
        """
        Check if a string is accepted by the automaton
        
        Args:
            input_string (str): Input string to check
            
        Returns:
            bool: True if string is accepted, False otherwise
        """
        accepted, _ = self.process_string(input_string)
        return accepted
    
    def print_transition_table(self):
        """
        Print the transition table in a formatted way
        """
        print("Estado\t", end="")
        for symbol in sorted(self.alphabet):
            print(f"{symbol}\t", end="")
        print()
        
        for state in sorted(self.states):
            print(f"{state}\t", end="")
            for symbol in sorted(self.alphabet):
                if state in self.transitions and symbol in self.transitions[state]:
                    print(f"{self.transitions[state][symbol]}\t", end="")
                else:
                    print("----\t", end="")
            print()


class L1_Automaton(FiniteAutomaton):
    """
    Automaton for L1 = {(01)^n | n >= 0}
    Accepts repetitions of "01" pattern (including empty string)
    """
    
    def __init__(self):
        # Define automaton components
        states = {'q0', 'q1', 'q2'}
        alphabet = {'0', '1'}
        transitions = {
            'q0': {'0': 'q1', '1': 'q2'},  # From q0: 0→q1, 1→q2(trap)
            'q1': {'0': 'q2', '1': 'q0'},  # From q1: 0→q2(trap), 1→q0
            'q2': {'0': 'q2', '1': 'q2'}   # From q2: trap state (0,1→q2)
        }
        initial_state = 'q0'
        accepting_states = {'q0'}  # Only q0 is accepting
        
        super().__init__(states, alphabet, transitions, initial_state, accepting_states)


class L2_Automaton(FiniteAutomaton):
    """
    Automaton for L2 = {(10)^n | n >= 0}
    Accepts repetitions of "10" pattern (including empty string)
    """
    
    def __init__(self):
        # Define automaton components
        states = {'p0', 'p1', 'p2'}
        alphabet = {'0', '1'}
        transitions = {
            'p0': {'0': 'p2', '1': 'p1'},  # From p0: 0→p2(trap), 1→p1
            'p1': {'0': 'p0', '1': 'p2'},  # From p1: 0→p0, 1→p2(trap)
            'p2': {'0': 'p2', '1': 'p2'}   # From p2: trap state (0,1→p2)
        }
        initial_state = 'p0'
        accepting_states = {'p0'}  # Only p0 is accepting
        
        super().__init__(states, alphabet, transitions, initial_state, accepting_states)


class L3_Automaton(FiniteAutomaton):
    """
    Automaton for L3 = L1 ∪ L2
    Accepts strings that belong to L1 OR L2
    """
    
    def __init__(self):
        # Define automaton components
        states = {'r0', 'r1', 'r2', 'r3'}
        alphabet = {'0', '1'}
        transitions = {
            'r0': {'0': 'r1', '1': 'r2'},  # From r0: 0→r1, 1→r2
            'r1': {'0': 'r3', '1': 'r0'},  # From r1: 0→r3(trap), 1→r0
            'r2': {'0': 'r0', '1': 'r3'},  # From r2: 0→r0, 1→r3(trap)
            'r3': {'0': 'r3', '1': 'r3'}   # From r3: trap state (0,1→r3)
        }
        initial_state = 'r0'
        accepting_states = {'r0'}  # Only r0 is accepting
        
        super().__init__(states, alphabet, transitions, initial_state, accepting_states)


def test_automaton(automaton, test_cases, language_name):
    """
    Test an automaton with a set of test cases
    
    Args:
        automaton: FiniteAutomaton instance to test
        test_cases (list): List of tuples (string, expected_result)
        language_name (str): Name of the language for display
    """
    print(f"\n=== Probando {language_name} ===")
    print("Tabla de Transiciones:")
    automaton.print_transition_table()
    print(f"\nEstado inicial: {automaton.initial_state}")
    print(f"Estados de aceptación: {automaton.accepting_states}")
    
    print(f"\nResultados de pruebas para {language_name}:")
    print("-" * 60)
    
    all_correct = True
    for test_string, expected in test_cases:
        result = automaton.is_accepted(test_string)
        status = "✓" if result == expected else "✗"
        display_string = f'"{test_string}"' if test_string != "" else "ε (vacía)"
        expected_text = "Aceptada" if expected else "Rechazada"
        result_text = "Aceptada" if result else "Rechazada"
        
        if result != expected:
            all_correct = False
        
        print(f"{status} Cadena: {display_string:<15} Esperado: {expected_text:<10} Obtenido: {result_text}")
    
    accuracy = "TODAS CORRECTAS" if all_correct else "HAY ERRORES"
    print(f"\nResultado general de las pruebas: {accuracy}")


def demonstrate_string_processing(automaton, test_string, language_name):
    """
    Demonstrate step-by-step processing of a string
    
    Args:
        automaton: FiniteAutomaton instance
        test_string (str): String to process
        language_name (str): Name of the language
    """
    print(f"\n=== Procesamiento paso a paso de '{test_string}' en {language_name} ===")
    
    current_state = automaton.initial_state
    print(f"Estado inicial: {current_state}")
    
    for i, symbol in enumerate(test_string):
        if current_state in automaton.transitions and symbol in automaton.transitions[current_state]:
            next_state = automaton.transitions[current_state][symbol]
            print(f"Paso {i+1}: Leer '{symbol}' → {current_state} → {next_state}")
            current_state = next_state
        else:
            print(f"Paso {i+1}: Leer '{symbol}' → No hay transición desde {current_state}")
            break
    
    is_accepted = current_state in automaton.accepting_states
    result = "ACEPTADA" if is_accepted else "RECHAZADA"
    print(f"Estado final: {current_state}")
    print(f"Resultado: La cadena es {result}")


def main():
    """
    Main function to test all automata
    """
    print("Implementación de Autómatas Finitos - Problema 4")
    print("=" * 70)
    print("Este programa simula tres autómatas finitos:")
    print("• L₁ = {(01)ⁿ | n ≥ 0} - Acepta repeticiones del patrón '01'")
    print("• L₂ = {(10)ⁿ | n ≥ 0} - Acepta repeticiones del patrón '10'") 
    print("• L₃ = L₁ ∪ L₂ - Acepta cadenas que pertenecen a L₁ O a L₂")
    print("=" * 70)
    
    # Create automaton instances
    l1_automaton = L1_Automaton()
    l2_automaton = L2_Automaton()
    l3_automaton = L3_Automaton()
    
    # Test cases for L1 = {(01)^n | n >= 0}
    l1_test_cases = [
        ("", True),        # Empty string (n=0)
        ("01", True),      # n=1
        ("0101", True),    # n=2
        ("010101", True),  # n=3
        ("0", False),      # Invalid
        ("1", False),      # Invalid
        ("10", False),     # Invalid
        ("00", False),     # Invalid
        ("11", False),     # Invalid
        ("001", False),    # Invalid
        ("110", False),    # Invalid
    ]
    
    # Test cases for L2 = {(10)^n | n >= 0}
    l2_test_cases = [
        ("", True),        # Empty string (n=0)
        ("10", True),      # n=1
        ("1010", True),    # n=2
        ("101010", True),  # n=3
        ("0", False),      # Invalid
        ("1", False),      # Invalid
        ("01", False),     # Invalid
        ("00", False),     # Invalid
        ("11", False),     # Invalid
        ("100", False),    # Invalid
        ("011", False),    # Invalid
    ]
    
    # Test cases for L3 = L1 ∪ L2
    l3_test_cases = [
        ("", True),        # Empty string
        ("01", True),      # From L1
        ("10", True),      # From L2
        ("0101", True),    # From L1
        ("1010", True),    # From L2
        ("010101", True),  # From L1
        ("101010", True),  # From L2
        ("0", False),      # Invalid
        ("1", False),      # Invalid
        ("00", False),     # Invalid
        ("11", False),     # Invalid
        ("0110", False),   # Invalid
        ("1001", False),   # Invalid
    ]
    
    # Test all automata
    test_automaton(l1_automaton, l1_test_cases, "L₁ = {(01)ⁿ | n ≥ 0}")
    test_automaton(l2_automaton, l2_test_cases, "L₂ = {(10)ⁿ | n ≥ 0}")
    test_automaton(l3_automaton, l3_test_cases, "L₃ = L₁ ∪ L₂")
    
    # Demonstrate step-by-step processing
    print("\n" + "=" * 70)
    print("DEMOSTRACIONES PASO A PASO")
    print("=" * 70)
    
    demonstrate_string_processing(l1_automaton, "0101", "L₁")
    demonstrate_string_processing(l2_automaton, "1010", "L₂")
    demonstrate_string_processing(l3_automaton, "01", "L₃")
    demonstrate_string_processing(l3_automaton, "10", "L₃")
    demonstrate_string_processing(l3_automaton, "0110", "L₃")
    
    # Interactive testing section
    print("\n" + "=" * 70)
    print("MODO INTERACTIVO")
    print("=" * 70)
    
    while True:
        try:
            print("\nElige el autómata a probar:")
            print("1. L₁ = {(01)ⁿ | n ≥ 0} - Patrones '01'")
            print("2. L₂ = {(10)ⁿ | n ≥ 0} - Patrones '10'")
            print("3. L₃ = L₁ ∪ L₂ - Unión de ambos lenguajes")
            print("4. Salir")
            
            choice = input("Ingresa tu opción (1-4): ").strip()
            
            if choice == "4":
                print("¡Hasta luego!")
                break
            elif choice in ["1", "2", "3"]:
                test_string = input("Ingresa la cadena a probar (solo 0s y 1s): ").strip()
                
                # Validate input
                if not all(c in "01" for c in test_string):
                    print("¡Entrada inválida! Usa solo 0s y 1s.")
                    continue
                
                if choice == "1":
                    result = l1_automaton.is_accepted(test_string)
                    lang = "L₁"
                    pattern = "repeticiones de '01'"
                elif choice == "2":
                    result = l2_automaton.is_accepted(test_string)
                    lang = "L₂"
                    pattern = "repeticiones de '10'"
                else:
                    result = l3_automaton.is_accepted(test_string)
                    lang = "L₃"
                    pattern = "patrones '01' o '10'"
                
                display_string = f'"{test_string}"' if test_string else "ε (cadena vacía)"
                status = "ACEPTADA" if result else "RECHAZADA"
                print(f"\n📊 RESULTADO:")
                print(f"   Cadena: {display_string}")
                print(f"   Lenguaje: {lang} ({pattern})")
                print(f"   Estado: {status}")
                
                if result:
                    print(f"   ✅ La cadena pertenece al lenguaje {lang}")
                else:
                    print(f"   ❌ La cadena NO pertenece al lenguaje {lang}")
            else:
                print("¡Opción inválida! Por favor ingresa 1-4.")
                
        except KeyboardInterrupt:
            print("\n¡Hasta luego!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()