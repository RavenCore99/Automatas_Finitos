"""
Pushdown Automaton Implementation - Context-Free Language Problem
Language: L = {a^i b^j c^k a^l | i,j > 0; k = j}

Author: [Your Name]
Date: [Current Date]
Course: Automata Theory - Universidad
"""

class PushdownAutomaton:
    """
    Base class for Pushdown Automaton implementation
    """
    
    def __init__(self, states, alphabet, stack_alphabet, transitions, initial_state, initial_stack, accepting_states):
        """
        Initialize the pushdown automaton
        
        Args:
            states (set): Set of all states
            alphabet (set): Input alphabet
            stack_alphabet (set): Stack alphabet
            transitions (dict): Transition function as nested dictionary
            initial_state (str): Initial state
            initial_stack (str): Initial stack symbol
            accepting_states (set): Set of accepting states
        """
        self.states = states
        self.alphabet = alphabet
        self.stack_alphabet = stack_alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.initial_stack = initial_stack
        self.accepting_states = accepting_states
    
    def process_string(self, input_string):
        """
        Process an input string through the pushdown automaton
        
        Args:
            input_string (str): Input string to process
            
        Returns:
            tuple: (bool, str, list, list) - (is_accepted, final_state, path, stack_trace)
        """
        current_state = self.initial_state
        stack = [self.initial_stack]
        path = [current_state]
        stack_trace = [stack.copy()]
        position = 0
        
        # Process each symbol in the input string
        while position <= len(input_string):
            if position == len(input_string):
                # Check epsilon transitions at end of input
                symbol = 'ε'
            else:
                symbol = input_string[position]
                if symbol not in self.alphabet:
                    return False, "Invalid symbol", path, stack_trace
            
            # Find valid transition
            transition_found = False
            
            if current_state in self.transitions:
                for (input_sym, stack_top), (next_state, stack_action) in self.transitions[current_state].items():
                    # Check if this transition applies
                    if ((symbol == input_sym or (symbol == 'ε' and input_sym == 'ε')) and
                        (stack_top == 'ε' or (len(stack) > 0 and stack[-1] == stack_top))):
                        
                        # Apply transition
                        current_state = next_state
                        
                        # Handle stack operations
                        if stack_top != 'ε' and len(stack) > 0:
                            stack.pop()  # Pop the matched symbol
                        
                        if stack_action != 'ε':
                            stack.append(stack_action)  # Push new symbol
                        
                        path.append(current_state)
                        stack_trace.append(stack.copy())
                        transition_found = True
                        
                        # Only advance position if we consumed an input symbol
                        if symbol != 'ε':
                            position += 1
                        break
            
            if not transition_found:
                if position < len(input_string):
                    path.append("∅")
                    return False, "No transition defined", path, stack_trace
                else:
                    break
        
        # Check if final state is accepting and stack only contains initial symbol
        is_accepted = (current_state in self.accepting_states and 
                      len(stack) == 1 and stack[0] == self.initial_stack)
        
        return is_accepted, current_state, path, stack_trace
    
    def is_accepted(self, input_string):
        """
        Check if a string is accepted by the automaton
        
        Args:
            input_string (str): Input string to check
            
        Returns:
            bool: True if string is accepted, False otherwise
        """
        accepted, _, _, _ = self.process_string(input_string)
        return accepted
    
    def print_transition_table(self):
        """
        Print the transition table in a formatted way
        """
        print("Estado\t", end="")
        for symbol in sorted(self.alphabet.union({'ε'})):
            print(f"{symbol}\t", end="")
        print()
        print("-" * 60)
        
        for state in sorted(self.states):
            marker = "→ " if state == self.initial_state else "  "
            marker += "* " if state in self.accepting_states else "  "
            print(f"{marker}{state}\t", end="")
            
            for symbol in sorted(self.alphabet.union({'ε'})):
                transitions_for_symbol = []
                if state in self.transitions:
                    for (input_sym, stack_top), (next_state, stack_action) in self.transitions[state].items():
                        if input_sym == symbol:
                            transition_str = f"{next_state}"
                            if stack_top != 'ε' or stack_action != 'ε':
                                transition_str += f" ({stack_top}/{stack_action})"
                            transitions_for_symbol.append(transition_str)
                
                if transitions_for_symbol:
                    print(f"{','.join(transitions_for_symbol)}\t", end="")
                else:
                    print("∅\t", end="")
            print()


class LanguageAutomaton(PushdownAutomaton):
    """
    Pushdown Automaton for the language: L = {a^i b^j c^k a^l | i,j > 0; k = j}
    
    This automaton accepts strings that:
    1. Start with at least one 'a' (i > 0)
    2. Continue with at least one 'b' (j > 0), pushing each 'b' to stack
    3. Have exactly j 'c's (k = j), popping one 'b' for each 'c'
    4. End with zero or more 'a's (l >= 0)
    5. Stack must be empty at the end (only initial symbol remains)
    
    State meanings:
    - q0: Initial state, waiting for first 'a'
    - q1: Processing initial 'a's (i > 0)
    - q2: Processing 'b's and pushing to stack (j > 0)
    - q3: Processing 'c's and popping from stack (k = j verification)
    - q4: Processing final 'a's (l >= 0)
    - qf: Final accepting state
    """
    
    def __init__(self):
        # Define automaton components
        states = {'q0', 'q1', 'q2', 'q3', 'q4', 'qf'}
        alphabet = {'a', 'b', 'c'}
        stack_alphabet = {'B', 'Z0'}
        
        # Transition function: state -> {(input, stack_top): (next_state, stack_action)}
        transitions = {
            'q0': {
                ('a', 'ε'): ('q1', 'ε')  # First 'a', no stack operation
            },
            'q1': {
                ('a', 'ε'): ('q1', 'ε'),  # More 'a's, stay in q1
                ('b', 'ε'): ('q2', 'B')   # First 'b', push B to stack
            },
            'q2': {
                ('b', 'ε'): ('q2', 'B'),  # More 'b's, push B to stack
                ('c', 'B'): ('q3', 'ε')   # First 'c', pop B from stack
            },
            'q3': {
                ('c', 'B'): ('q3', 'ε'),        # More 'c's, pop B from stack
                ('a', 'ε'): ('q4', 'ε'),        # First final 'a'
                ('ε', 'Z0'): ('qf', 'Z0')       # End of string, accept if only Z0 in stack
            },
            'q4': {
                ('a', 'ε'): ('q4', 'ε'),        # More final 'a's
                ('ε', 'Z0'): ('qf', 'Z0')       # End of string, accept if only Z0 in stack
            }
        }
        
        initial_state = 'q0'
        initial_stack = 'Z0'
        accepting_states = {'qf'}
        
        super().__init__(states, alphabet, stack_alphabet, transitions, 
                        initial_state, initial_stack, accepting_states)


def validate_string_pattern(input_string):
    """
    Validate string pattern manually to understand the language
    
    Args:
        input_string (str): String to validate
        
    Returns:
        dict: Analysis results
    """
    analysis = {
        'string': input_string,
        'i': 0, 'j': 0, 'k': 0, 'l': 0,
        'valid': True,
        'reason': '',
        'phases': []
    }
    
    pos = 0
    
    # Phase 1: Count initial a's (i > 0)
    start_pos = pos
    while pos < len(input_string) and input_string[pos] == 'a':
        analysis['i'] += 1
        pos += 1
    
    if analysis['i'] == 0:
        analysis['valid'] = False
        analysis['reason'] = "i debe ser > 0 (faltan 'a's iniciales)"
        return analysis
    
    analysis['phases'].append(f"Fase 1: {analysis['i']} 'a's iniciales (posiciones {start_pos}-{pos-1})")
    
    # Phase 2: Count b's (j > 0)
    start_pos = pos
    while pos < len(input_string) and input_string[pos] == 'b':
        analysis['j'] += 1
        pos += 1
    
    if analysis['j'] == 0:
        analysis['valid'] = False
        analysis['reason'] = "j debe ser > 0 (faltan 'b's)"
        return analysis
    
    analysis['phases'].append(f"Fase 2: {analysis['j']} 'b's (posiciones {start_pos}-{pos-1})")
    
    # Phase 3: Count c's (must equal j)
    start_pos = pos
    while pos < len(input_string) and input_string[pos] == 'c':
        analysis['k'] += 1
        pos += 1
    
    analysis['phases'].append(f"Fase 3: {analysis['k']} 'c's (posiciones {start_pos}-{pos-1})")
    
    if analysis['k'] != analysis['j']:
        analysis['valid'] = False
        analysis['reason'] = f"k={analysis['k']} ≠ j={analysis['j']} (debe cumplirse k=j)"
        return analysis
    
    # Phase 4: Count final a's (l >= 0)
    start_pos = pos
    while pos < len(input_string) and input_string[pos] == 'a':
        analysis['l'] += 1
        pos += 1
    
    if analysis['l'] > 0:
        analysis['phases'].append(f"Fase 4: {analysis['l']} 'a's finales (posiciones {start_pos}-{pos-1})")
    else:
        analysis['phases'].append("Fase 4: Sin 'a's finales")
    
    # Check if we consumed all characters
    if pos < len(input_string):
        analysis['valid'] = False
        analysis['reason'] = f"Caracteres inválidos: '{input_string[pos:]}'"
        return analysis
    
    analysis['reason'] = f"✅ Válido: i={analysis['i']}, j={analysis['j']}, k={analysis['k']}, l={analysis['l']}"
    return analysis


def test_automaton(automaton, test_cases, language_description):
    """
    Test an automaton with a set of test cases
    """
    print(f"\n{'='*80}")
    print(f"PROBANDO AUTÓMATA A PILA PARA: {language_description}")
    print(f"{'='*80}")
    
    print("\n📊 TABLA DE TRANSICIONES:")
    automaton.print_transition_table()
    print(f"\nEstado inicial: {automaton.initial_state}")
    print(f"Símbolo inicial de pila: {automaton.initial_stack}")
    print(f"Estados de aceptación: {automaton.accepting_states}")
    
    print(f"\n🧪 RESULTADOS DE PRUEBAS:")
    print("-" * 90)
    print(f"{'Cadena':<20} {'Esperado':<10} {'Obtenido':<10} {'Análisis Manual':<20} {'Estado'}")
    print("-" * 90)
    
    all_correct = True
    for test_string, expected in test_cases:
        result = automaton.is_accepted(test_string)
        manual_analysis = validate_string_pattern(test_string)
        manual_result = manual_analysis['valid']
        
        _, final_state, _, _ = automaton.process_string(test_string)
        status = "✅" if result == expected else "❌"
        consistency = "✅" if result == manual_result else "⚠️"
        
        display_string = f'"{test_string}"' if test_string != "" else "ε"
        expected_text = "ACEPTA" if expected else "RECHAZA"
        result_text = "ACEPTA" if result else "RECHAZA"
        manual_text = "VÁLIDO" if manual_result else "INVÁLIDO"
        
        if result != expected:
            all_correct = False
        
        print(f"{display_string:<20} {expected_text:<10} {result_text:<10} {manual_text:<20} {status} {consistency}")
    
    accuracy = "🎉 TODAS CORRECTAS" if all_correct else "⚠️  HAY ERRORES"
    print("-" * 90)
    print(f"RESULTADO GENERAL: {accuracy}")
    
    return all_correct


def demonstrate_string_processing(automaton, test_string, show_details=True):
    """
    Demonstrate step-by-step processing of a string
    """
    print(f"\n{'='*80}")
    print(f"PROCESAMIENTO PASO A PASO DE: '{test_string}'")
    print(f"{'='*80}")
    
    # First show manual analysis
    manual_analysis = validate_string_pattern(test_string)
    print("🔍 ANÁLISIS MANUAL:")
    print("-" * 40)
    for phase in manual_analysis['phases']:
        print(f"   {phase}")
    print(f"   Resultado: {manual_analysis['reason']}")
    
    # Now show automaton processing
    print(f"\n🤖 PROCESAMIENTO DEL AUTÓMATA:")
    print("-" * 40)
    
    accepted, final_state, path, stack_trace = automaton.process_string(test_string)
    
    if show_details and len(path) > 1:
        current_state = automaton.initial_state
        print(f"Estado inicial: {current_state}, Pila: {stack_trace[0]}")
        print("-" * 60)
        
        input_pos = 0
        for i in range(1, len(path)):
            if i < len(stack_trace):
                if path[i] == "∅":
                    symbol = test_string[input_pos] if input_pos < len(test_string) else "ε"
                    print(f"Paso {i:2d}: '{symbol}' → ERROR: Sin transición desde {current_state}")
                    break
                else:
                    # Determine what symbol was processed
                    if input_pos < len(test_string):
                        symbol = test_string[input_pos]
                        input_pos += 1
                    else:
                        symbol = "ε"
                    
                    prev_stack = stack_trace[i-1]
                    curr_stack = stack_trace[i]
                    
                    # Describe stack operation
                    if len(prev_stack) < len(curr_stack):
                        stack_op = f"push({curr_stack[-1]})"
                    elif len(prev_stack) > len(curr_stack):
                        popped = prev_stack[-1] if prev_stack else "?"
                        stack_op = f"pop({popped})"
                    else:
                        stack_op = "no change"
                    
                    print(f"Paso {i:2d}: '{symbol}' → {current_state} → {path[i]} | Pila: {prev_stack} → {curr_stack} ({stack_op})")
                    current_state = path[i]
        
        print("-" * 60)
    
    is_accepted = final_state in automaton.accepting_states and len(stack_trace[-1]) == 1
    result_icon = "✅" if is_accepted else "❌"
    result_text = "ACEPTADA" if is_accepted else "RECHAZADA"
    
    print(f"Estado final: {final_state}")
    print(f"Pila final: {stack_trace[-1] if stack_trace else []}")
    print(f"Camino completo: {' → '.join(path)}")
    print(f"Resultado: {result_icon} La cadena es {result_text}")
    
    return is_accepted


def analyze_language_components():
    """
    Analyze the components of the context-free language
    """
    print(f"\n{'='*80}")
    print("ANÁLISIS DEL LENGUAJE LIBRE DE CONTEXTO")
    print(f"{'='*80}")
    print("Lenguaje: L = {a^i b^j c^k a^l | i,j > 0; k = j}")
    print()
    print("🔍 COMPONENTES:")
    print("   • a^i  - Secuencia inicial de 'a's donde i > 0 (al menos una 'a')")
    print("   • b^j  - Secuencia de 'b's donde j > 0 (al menos una 'b')")
    print("   • c^k  - Secuencia de 'c's donde k = j (mismo número que 'b's)")
    print("   • a^l  - Secuencia final de 'a's donde l >= 0 (cero o más 'a's)")
    print()
    print("🎯 RESTRICCIÓN CLAVE:")
    print("   • k = j: El número de 'c's debe ser exactamente igual al número de 'b's")
    print("   • Esta restricción requiere el uso de una pila para contar")
    print()
    print("📝 ESTRATEGIA DEL AUTÓMATA:")
    print("   1. Leer las 'a's iniciales sin usar la pila")
    print("   2. Por cada 'b', empujar un símbolo 'B' a la pila")
    print("   3. Por cada 'c', desapilar un símbolo 'B' de la pila")
    print("   4. Leer las 'a's finales sin usar la pila")
    print("   5. Aceptar solo si la pila queda con el símbolo inicial Z0")
    print()
    print("🔢 EJEMPLOS VÁLIDOS:")
    print("   • 'abc'       - i=1, j=1, k=1, l=0")
    print("   • 'abbcca'    - i=1, j=2, k=2, l=1")
    print("   • 'aabbccaa'  - i=2, j=2, k=2, l=2")
    print("   • 'abbbccc'   - i=1, j=3, k=3, l=0")


def main():
    """
    Main function to test the pushdown automaton
    """
    print("🤖 IMPLEMENTACIÓN DE AUTÓMATA A PILA (PDA)")
    print("📚 Curso: Lenguajes y Autómatas")
    print("📋 Ejercicio: Construcción de PDA para Lenguaje Libre de Contexto")
    print(f"{'='*80}")
    
    # Analyze the language components
    analyze_language_components()
    
    # Create automaton instance
    pda = LanguageAutomaton()
    
    # Comprehensive test cases
    test_cases = [
        # Basic valid cases
        ("abc", True),           # i=1, j=1, k=1, l=0
        ("abca", True),          # i=1, j=1, k=1, l=1
        ("abbcca", True),        # i=1, j=2, k=2, l=1
        ("aabbcc", True),        # i=2, j=2, k=2, l=0
        ("aabbccaa", True),      # i=2, j=2, k=2, l=2
        ("abbbccc", True),       # i=1, j=3, k=3, l=0
        ("aaabbbcccaaa", True),  # i=3, j=3, k=3, l=3
        
        # Invalid cases - wrong structure
        ("", False),             # Empty string
        ("a", False),            # Only 'a' - incomplete
        ("ab", False),           # Missing 'c's
        ("ac", False),           # Missing 'b's
        ("bc", False),           # Missing initial 'a's
        ("cab", False),          # Wrong order
        
        # Invalid cases - wrong counts
        ("abcc", False),         # i=1, j=1, k=2 (k≠j)
        ("abbcc", False),        # i=1, j=2, k=1 (k≠j)
        ("abbbcc", False),       # i=1, j=3, k=2 (k≠j)
        ("abbccc", False),       # i=1, j=2, k=3 (k≠j)
        
        # Invalid cases - wrong symbols
        ("abcd", False),         # Invalid symbol 'd'
        ("ab1c", False),         # Invalid symbol '1'
        
        # Edge cases
        ("aabc", True),          # Multiple initial 'a's
        ("abcaa", True),         # Multiple final 'a's
        ("aaaabbbbcccc", True),  # Large equal counts
        ("aaaabbbbcccca", True), # Large equal counts with final 'a'
        
        # Complex invalid patterns
        ("aabbc", False),        # Missing one 'c'
        ("aabbccc", False),      # Extra 'c'
        ("abcb", False),         # 'b' after 'c'
        ("acbc", False),         # Wrong order
        ("abac", False),         # 'a' in wrong position
    ]
    
    # Test the automaton
    all_tests_passed = test_automaton(pda, test_cases, 
                                     "L = {a^i b^j c^k a^l | i,j > 0; k = j}")
    
    # Demonstrate step-by-step processing for key examples
    print(f"\n{'='*80}")
    print("DEMOSTRACIONES DETALLADAS")
    print(f"{'='*80}")
    
    demo_strings = ["abc", "abbcca", "aabbccaa", "abcc", "abbbcc", "ac"]
    for demo_string in demo_strings:
        demonstrate_string_processing(pda, demo_string, show_details=True)
    
    # Interactive testing section
    print(f"\n{'='*80}")
    print("🎮 MODO INTERACTIVO - PRUEBA TUS PROPIAS CADENAS")
    print(f"{'='*80}")
    
    while True:
        try:
            print(f"\nLenguaje: L = {{a^i b^j c^k a^l | i,j > 0; k = j}}")
            print("Ingresa una cadena para probar (solo a, b, c), o 'quit' para salir:")
            
            user_input = input("► Cadena: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'salir', 'q']:
                print("👋 ¡Hasta luego!")
                break
            
            # Validate input
            if not all(c in "abc" for c in user_input):
                print("⚠️  Entrada inválida! Usa solo a, b, c.")
                continue
            
            # Process the string
            print(f"\n{'🔍 ANÁLISIS COMPLETO':<30}")
            print("=" * 60)
            
            result = demonstrate_string_processing(pda, user_input, show_details=True)
            
            # Manual validation
            manual_analysis = validate_string_pattern(user_input)
            
            print(f"\n📊 COMPARACIÓN DE RESULTADOS:")
            print("-" * 50)
            display_string = f'"{user_input}"' if user_input else "ε (cadena vacía)"
            
            automaton_result = "ACEPTA" if result else "RECHAZA"
            manual_result = "VÁLIDO" if manual_analysis['valid'] else "INVÁLIDO"
            consistency = "✅ Consistente" if result == manual_analysis['valid'] else "❌ Inconsistente"
            
            print(f"   Cadena analizada: {display_string}")
            print(f"   Resultado del autómata: {automaton_result}")
            print(f"   Análisis manual: {manual_result}")
            print(f"   Consistencia: {consistency}")
            
            if result:
                print(f"   🎉 La cadena PERTENECE al lenguaje L")
            else:
                print(f"   ⛔ La cadena NO PERTENECE al lenguaje L")
                print(f"   💡 Razón: {manual_analysis['reason']}")
                
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
    print(f"📝 Lenguaje implementado: L = {{a^i b^j c^k a^l | i,j > 0; k = j}}")
    print(f"🎯 Estados del autómata: 6 estados (q0, q1, q2, q3, q4, qf)")
    print(f"🔤 Alfabeto de entrada: {{a, b, c}}")
    print(f"📚 Alfabeto de pila: {{B, Z0}}")
    print(f"✨ Estado de aceptación: {{qf}}")
    print(f"🏗️  Tipo: Autómata a Pila Determinista (DPDA)")


if __name__ == "__main__":
    main()