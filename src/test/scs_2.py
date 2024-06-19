def int_to_bin_le(num, bits=8):
    """
    Convierte un número entero a su representación binaria en notación little-endian
    :param num: El número entero a convertir
    :param bits: La cantidad de bits (8 en este caso)
    :return: La representación binaria en notación little-endian
    """
    # Convertir a binario y rellenar con ceros a la izquierda para tener una longitud de 8 bits
    bin_str = f'{num:0{bits}b}'
    # Invertir el orden de los bits para obtener little-endian
    return bin_str[::-1]

# Generar y mostrar la secuencia
for i in range(256):
    print(int_to_bin_le(i))
