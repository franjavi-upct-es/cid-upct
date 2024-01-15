def get_names(prompt, count):
    names = set()
    for _ in range(count):
        name = input(prompt)
        names.add(name)
    return names

def main():
    employees = get_names("Ingrese el nombre del empleado: ", 3)
    clients = get_names("Ingrese el nombre del cliente: ", 1)

    # 1. Mostrar los nombres de todas las personas sin repeticiones.
    print("Todos los nombres: ", employees.union(clients))

    # 2. Informar qué nombres se repiten entre los empleados y clientes.
    print("Nombres repetidos: ", employees.intersection(clients))

    # 3. Informar de los nombres de empleados que no aparecen en los clientes
    print("Empleados que no son clientes: ", employees.difference(clients))

if __name__ == '__main__':
    main()