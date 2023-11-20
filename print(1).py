import re

class TablaSimbolos:
    def __init__(self):
        self.symbols = {}

    def insert(self, name, type):
        self.symbols[name] = type

    def lookup(self, name):
        return self.symbols.get(name, None)

    def delete(self, name):
        if name in self.symbols:
            del self.symbols[name]

class AnalizadorSemantico:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.errors = []

    def analyze_code(self, source_code):
        lines = source_code.split('\n')
        self.errors = []
        current_function = None

        def report_error(message, line_number):
            self.errors.append(f"Error - Línea {line_number}: {message}")

        for i, line in enumerate(lines, start=1):
            line = line.strip()

            # Ignore empty lines
            if not line:
                continue

            # Check for variable declarations
            match = re.match(r'^\s*([a-zA-Z_]\w*)\s*=\s*(.*)$', line)
            if match:
                name, value = match.groups()
                if current_function is None:
                    report_error(f"'{name}' no está declarado", i)
                else:
                    self.symbol_table.insert(name, current_function)
                continue

            # Check for function declarations
            match = re.match(r'^\s*([a-zA-Z_]\w*)\s+([a-zA-Z_]\w*)\s*\(([^)]*)\)\s*{?$', line)
            if match:
                return_type, func_name, params = match.groups()
                current_function = func_name
                continue

            # Check for return statements
            if current_function and line.startswith("return"):
                if not line.endswith(';'):
                    report_error(f"valor de retorno no coincide con la declaración de '{current_function}'", i)
                continue

            # Check for invalid statements
            if re.match(r'^\s*(if|while)\s*\(', line):
                report_error(f"Sentencia '{line.split('(')[0]}' no permitida en este contexto", i)
                continue

            # Check for unknown statements
            if re.match(r'^\s*(\w+)\s*\(', line):
                report_error(f"Declaración de función o variable desconocida: {line.split('(')[0]}", i)
                continue

        return self.errors

def read_source_code(file_path):
    try:
        with open(file_path, 'r') as file:
            source_code = file.read()
        return source_code
    except FileNotFoundError:
        print(f"El archivo '{file_path}' no se encontró.")
        return None

if __name__ == "__main__":
    file_path = "codigo_fuente.txt"  # Reemplaza con la ruta de tu archivo
    source_code = read_source_code(file_path)

    if source_code:
        symbol_table = TablaSimbolos()
        analyzer = AnalizadorSemantico(symbol_table)
        errors = analyzer.analyze_code(source_code)

        if errors:
            for error in errors:
                print(error)
        else:
            print("El código fuente es correcto.")

            
