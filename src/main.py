# We initiate our tickets program
from escpos.printer import Usb
import flet as ft
import mysql.connector

# Conexion con la BD
config = {
    'user': 'root',
    'password': 'Enini300723@',
    'host': 'localhost',
    'database': 'tickets_crazy_washsers',
    'raise_on_warnings': True
}

class Ticket:

    def __init__(self):
        self.fecha_entrega = None
        self.fecha_recepcion = None
        self.nombre_receptor = None
        self.numero_pares = None
        self.numero_gorras = None
        self.otros = None
        self.total = None
        self.a_cuenta = None
        self.resta = None
        self.describe_pares = None
        self.describe_gorras = None
        self.describe_otros = None
        self.codigo_cliente = None
        self.ticket_en_bd = False


    def conexion_base_datos_tickets(self, consulta, datos):

        try:

            conexion_tickets = mysql.connector.connect(**config)

            print("Conexión exitosa con la base de datos desde tickets")

            cursor_tickets = conexion_tickets.cursor()
            cursor_tickets.execute(consulta, datos)

            resultados_tickets = cursor_tickets.fetchall()

            if resultados_tickets:

                for k in resultados_tickets:

                    for m in k:

                        print(m)

                self.ticket_en_bd = True

            conexion_tickets.commit()

            cursor_tickets.close()
            conexion_tickets.close()
            print("Conexión cerrada")

        except mysql.connector.Error as err:

            print(f'Error: {err}')

    def agregar_ticket_bd(self):

        consulta = ("INSERT INTO tickets (fecha_entrega, fecha_recepcion, nombre_receptor, numero_pares, numero_gorras\
        , otros, total, a_cuenta, resta, describe_pares, describe_gorras, describe_otros, codigo_cliente) VALUES (%s, \
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

        datos = (self.fecha_entrega, self.fecha_recepcion, self.nombre_receptor, self.numero_pares, self.numero_gorras,\
                 self.otros, self.total, self.a_cuenta, self.resta, self.describe_pares, self.describe_gorras,\
                 self.describe_otros, self.codigo_cliente)

        self.conexion_base_datos_tickets(consulta, datos)

class Cliente:

    def __init__(self):
        self.id_cliente = None
        self.nombre_completo = None
        self.telefono = None
        self.correo = None
        self.cliente_en_bd = False

    # El metodo conexion_base_datos conecta con la base de datos para consultas a la tabla clientes
    def conexion_base_datos(self, consulta, datos):

        # Try catch que maneja el evento de conexion con la BD MySQL
        try:

            # variable conexion contiene la "conexion" con la BD"
            conexion = mysql.connector.connect(**config)

            # Imprime en pantalla que hubo conexion exitosa
            print("Conexión exitosa con la base de datos.")

            # La variable cursor contiene el posicionamiento para las consultas a la BC
            cursor = conexion.cursor()

            # Se ejecuta la sentencia con la propiedad "execute" del objeto cursor pasandole argumentos: consulta y
            # datos que en este caso contiene la consulta "select" previamente declarada y datos contiene el numero
            # de telefono previamente asignado
            cursor.execute(consulta, datos)

            # Se asigna a la variable resultados los datos obtenidos despues de aplicar la consulta, en este caso
            # el metodo fetchall() del objeto cursor contiene la informacion
            resultados = cursor.fetchall()

            # Se aplica un if que "si hay resultados entramos al control de flujo"
            if resultados:

                # Testeo de los resultados
                print(resultados)

                # Para cada resultado del set de resultados se aplica un for anidado
                for i in resultados:

                    # Testeo de los resultados
                    print(i)

                    # Para
                    for j in i:

                        # Testeo de los resultados
                        print(j)

                        # Se asigna a la propiedad id_cliente del objeto cliente el valor del resultado
                        self.id_cliente = j

                        # Testeo de los resultados
                        print(j)

                # Se asigna a la propiedad cliente_en_bd del objeto cliente el valor True (si existe)
                self.cliente_en_bd = True

            # Se realiza la consulta erectivamente con el metodo commit() del objeto conexion creado
            conexion.commit()

            # Se cierra el objeto cursor y el objeto conexion para no dejar abierta la conexion con la BD*
            cursor.close()
            conexion.close()

            # Se imprime en pantalla que se cerro la conexion
            print('Conexion cerrada')

        # La excepcion se ejecuta cuando hubo un error con la conexion a la BD
        except mysql.connector.Error as err:

            # Imprime en pantalla el error y que tipo de error
            print(f'Error: {err}')

    def agregarse_bd(self):

        consulta = ("INSERT INTO clientes (nombre, telefono, correo) VALUES (%s, %s, %s)")
        datos = (self.nombre_completo, self.telefono, self.correo)

        self.conexion_base_datos(consulta, datos)

    # El metodo buscar_cliente_en_bd consulta en la base de datos si existe el registro
    def buscar_cliente_en_bd(self):

        # La variable consulta contiene la sentencia SQL que selecciona el id_cliente de la tabla clientes filtrando
        # por el numero de telefono proporcionado
        consulta = ("SELECT id_cliente FROM clientes WHERE telefono = %s")

        # Imprime en pantalla la consulta
        # print(consulta) "solo para debugging"

        # Asignacion de la propiedad telefono del objeto cliente creado a la variable telefono
        telefono = (self.telefono,)

        # Se invoca al metodo del objeto Cliente conexion_base_datos y se le pasan dos argumentos: consulta y telefono
        self.conexion_base_datos(consulta, telefono)


def agregar_cliente():

    cliente = Cliente()
    cliente.nombre_completo = input("Ingrese nombre completo: ")
    cliente.telefono = input("Ingrese número de teléfono: ")
    cliente.correo = input("Ingrese correo: ")

    cliente.agregarse_bd()

def buscar_cliente():

    # Se crea un objeto Cliente
    cliente = Cliente()

    # Se asigna un valor a la propiedad telefono del objeto cliente para buscarlo en la BD
    cliente.telefono = input("Ingrese el número de teléfono para buscar al cliente: ")

    # el objeto cliente llama a su metodo buscar_cliente_en_bd()
    cliente.buscar_cliente_en_bd()

    # Si la propiedad cliente_en_bd del objeto cliente creado es True (si existe en la BD) se aplica un If
    if cliente.cliente_en_bd:

        # Impresion en pantalla de que el cliente esta en la BD
        print("Cliente en Base de Datos.")

        # Asignacion de y/n para agregar un ticket a la base de datos para el cliente encontrado
        pregunta_ticket = input("¿Desea agregar ticket de servicio? (y/n): ")

        # Si la respuesta fue "y" o "Y" se ejecuta el siguiente if anidado
        if pregunta_ticket == "y" or pregunta_ticket == "Y":

            # Se crea un objeto ticket
            ticket = Ticket()

            # Se le asigna valor a cada uno de las propiedades del objeto ticket
            ticket.fecha_entrega = input("Ingrese la fecha de entrega (aaaa-mm-dd): ")
            ticket.fecha_recepcion = input("Ingrese la fecha de entrega (aaaa-mm-dd): ")
            ticket.nombre_receptor = input("Ingrese el nombre del cliente: ")
            ticket.numero_pares = input("Ingrese el numero de pares: ")
            ticket.numero_gorras = input("Ingrese el numero de gorras: ")
            ticket.otros = input("Ingrese otros articulos (si los hay): ")
            ticket.total = input("Ingrese el total: ")
            ticket.a_cuenta = input("Ingrese cuánto deja a cuenta: ")
            ticket.resta = int(ticket.total) - int(ticket.a_cuenta)
            ticket.describe_pares = input("Describa los pares (Usar código de servicio CW): ")
            ticket.describe_gorras = input("Describa las gorras (Usar código de servicio CW): ")
            ticket.describe_otros = input("Describa otros (Usar código de servicio CW): ")

            # Testeo de que se le esta asignando el id_cliente correcto a la propiedad codigo_cliente del objeto ticket
            # para que esten relacionados de manera correcta
            print(cliente.id_cliente)

            # Se asigna el parametro id_cliente del objeto cliente a la propiedad codigo_cliente del objeto ticket
            ticket.codigo_cliente = cliente.id_cliente

            # Se llama al metodo agregar_ticket_db() del objeto ticket
            ticket.agregar_ticket_bd()

    else:

        agregar = input("¿Deseas agregar al cliente? (s/n): ")

        if agregar == "s" or agregar == "S":

            agregar_cliente()

def main():

    # Aqui empieza el programa!

    # Menu para seleccionar el evento
    print("----Menu----")
    print("1 - Buscar cliente\n2 - Agregar cliente\n3 - Buscar ticket")

    # variable opcion contiene el evento
    opcion = input("Elija la opcion que desea ejecutar: ")

    # control de flujo para evento
    if opcion == "1":

        # se llama a la funcion buscar_cliente
        buscar_cliente()

    elif opcion == "2":

        agregar_cliente()

    else:

        print("Escogiste buscar ticket")

main()

# Conectar a la impresora USB con endpoints manuales
#p = Usb(0x1fc9, 0x2016, in_ep=0x129, out_ep=0x03)  # Reemplaza con tus valores

# Imprimir texto
#p.text("CRAZY WASHERS!\n")
#p.text("CRAZY WASHERS!\n")
#p.text("CRAZY WASHERS!\n")
#p.cut()
