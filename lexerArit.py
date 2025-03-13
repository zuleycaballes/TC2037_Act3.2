def lexerAritmetico(archivo):
    # Lista para almacenar los tokens encontrados
    tokens = []

    # Intentar abrir y leer el archivo de entrada
    try:
        f = open(archivo, 'r')
        lineas = f.readlines()
        f.close()
    except:
        print('Error al abrir el archivo')
        return

    # Procesar cada línea del archivo
    for linea in lineas:
        i = 0              # Índice para recorrer la línea
        n = len(linea)     # Longitud de la línea
        while i < n:
            c = linea[i]   # Carácter actual

            # Omitir espacios, tabulaciones y saltos de línea para evitar tokens vacíos
            if c == ' ' or c == '\t' or c == '\n':
                i += 1
                continue

            # Si se detecta el inicio de un comentario ('//'),
            # se toma el resto de la línea como un único token
            if c == '/' and i + 1 < n and linea[i + 1] == '/':
                tokens.append((linea[i:].strip(), 'Comentario'))
                break  # Se finaliza el análisis de la línea actual

            # Reconocimiento de números (Enteros y Reales)
            # Se acepta:
            #   - Un dígito, o
            #   - Un punto seguido de dígito, o
            #   - Un signo (+ o -) seguido de dígito, o
            #   - Un signo seguido de punto y dígito.
            if (('0' <= c <= '9') or 
                (c == '.' and i + 1 < n and '0' <= linea[i+1] <= '9') or 
                ((c == '+' or c == '-') and i + 1 < n and (('0' <= linea[i+1] <= '9') or (linea[i+1] == '.' and i + 2 < n and '0' <= linea[i+2] <= '9')))):
                inicio = i  # Marca el inicio del número
                # Si comienza con un signo, avanzar el índice
                if c == '+' or c == '-':
                    i += 1
                punto = False  # Bandera para indicar si ya se encontró un punto decimal
                exp = False    # Bandera para indicar si ya se encontró la notación exponencial

                # Si el número inicia con un punto, se marca y se avanza
                if i < n and linea[i] == '.':
                    punto = True
                    i += 1
                # Recorrer la secuencia numérica
                while i < n:
                    ch = linea[i]
                    # Si es un dígito, continuar avanzando
                    if '0' <= ch <= '9':
                        i += 1
                    # Si es un punto y aún no se ha usado en el número, se marca
                    elif ch == '.' and not punto and not exp:
                        punto = True
                        i += 1
                    # Si se detecta notación exponencial ('e' o 'E') y aún no se ha usado
                    elif (ch == 'e' or ch == 'E') and not exp:
                        exp = True
                        i += 1
                        # Se permite un signo después de la 'e' o 'E'
                        if i < n and (linea[i] == '+' or linea[i] == '-'):
                            i += 1
                    else:
                        break
                num = linea[inicio:i]  # Extraer el número completo
                # Clasificar el número como Real si contiene un punto o notación exponencial, de lo contrario Entero
                if ('.' in num) or ('e' in num) or ('E' in num):
                    tokens.append((num, 'Real'))
                else:
                    tokens.append((num, 'Entero'))
                continue

            # Reconocimiento de variables: deben iniciar con una letra (mayúscula o minúscula)
            if (('a' <= c <= 'z') or ('A' <= c <= 'Z')):
                inicio = i
                i += 1
                # Se aceptan letras, dígitos y guión bajo en el resto de la variable
                while i < n:
                    ch = linea[i]
                    if (('a' <= ch <= 'z') or ('A' <= ch <= 'Z') or ('0' <= ch <= '9') or (ch == '_')):
                        i += 1
                    else:
                        break
                tokens.append((linea[inicio:i], 'Variable'))
                continue

            # Reconocimiento de operadores y símbolos especiales (manteniendo la lógica original)
            if c in '=+-*/()^':
                if c == '=':
                    tokens.append(('=', 'Asignacion'))
                elif c == '+':
                    tokens.append(('+', 'Suma'))
                elif c == '-':
                    tokens.append(('-', 'Resta'))
                elif c == '*':
                    tokens.append(('*', 'Multiplicacion'))
                elif c == '/':
                    tokens.append(('/', 'Division'))
                elif c == '^':
                    tokens.append(('^', 'Potencia'))
                elif c == '(':
                    tokens.append(('(', 'Parentesis que abre'))
                elif c == ')':
                    tokens.append((')', 'Parentesis que cierra'))
                i += 1
                continue

            # Si el carácter no coincide con ningún patrón conocido, se marca como token inválido
            tokens.append((c, 'Token invalido'))
            i += 1

    # Imprimir la tabla de tokens y sus respectivos tipos
    print('Token\t\tTipo')
    for token, tipo in tokens:
        print(f'{token}\t\t{tipo}')

# Llamada a la función con el archivo de entrada (asegúrate de tener "archivo.txt")
lexerAritmetico('archivo.txt')