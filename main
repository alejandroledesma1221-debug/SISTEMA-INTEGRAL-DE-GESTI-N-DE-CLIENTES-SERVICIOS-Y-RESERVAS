"""
Punto de entrada principal del Sistema Integral de Gestión de Clientes, Servicios y Reservas
Empresa: Software FJ - Curso Programación (213023) - UNAD.

Incluye:
1. Simulación automatizada de 12 operaciones completas (válidas e inválidas) demostrando
   abstracción, herencia, polimorfismo, encapsulación, sobrecarga y manejo avanzado de excepciones.
2. Menú interactivo en consola para pruebas adicionales sin interrupciones.
"""

from entidades import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reservas import GestorSoftwareFJ
from excepciones import SistemaFJError


def ejecutar_simulacion_completa(gestor: GestorSoftwareFJ) -> None:
    print("=" * 80)
    print("EJECUTANDO SIMULACIÓN DE 12 OPERACIONES COMPLETAS - SOFTWARE FJ")
    print("=" * 80)

    # 1. Registro válido de clientes
    print("\n[Operación 1] Registro válido de clientes:")
    try:
        c1 = Cliente("CLI-01", "Laura Gómez", "1020456789", "laura.gomez@empresa.com", "3104567890")
        c2 = Cliente("CLI-02", "Carlos Mendoza", "79854123", "cmendoza@techcol.co", "3157894561")
        gestor.registrar_cliente(c1)
        gestor.registrar_cliente(c2)
        print(f"  OK -> {c1.obtener_resumen()}")
        print(f"  OK -> {c2.obtener_resumen()}")
    except SistemaFJError as exc:
        gestor.logger.registrar_error(exc, "Op 1")

    # 2. Registro inválido de cliente (correo y documento incorrectos)
    print("\n[Operación 2] Registro inválido de cliente (datos mal formados):")
    try:
        c_invalido = Cliente("CLI-03", "Ana 123", "12", "correo-sin-arroba", "123")
        gestor.registrar_cliente(c_invalido)
    except SistemaFJError as exc:
        gestor.logger.registrar_error(exc, "Op 2 - Validación de cliente")
        print(f"  [EXCEPCIÓN CAPTURADA] {exc}")

    # 3. Registro de cliente duplicado
    print("\n[Operación 3] Intento de registro de cliente con documento duplicado:")
    try:
        c_duplicado = Cliente("CLI-04", "Laura Gómez Copia", "1020456789", "otra@empresa.com", "3001112233")
        gestor.registrar_cliente(c_duplicado)
    except SistemaFJError as exc:
        gestor.logger.registrar_error(exc, "Op 3")

    # 4. Creación válida de los 3 tipos de servicios especializados
    print("\n[Operación 4] Creación válida de servicios (Sala, Equipo, Asesoría):")
    try:
        s_sala = ReservaSala("SRV-01", "Sala Innovación", 80000, capacidad_maxima=12, tiene_videoconferencia=True)
        s_equipo = AlquilerEquipo("SRV-02", "Estación Workstation RTX", 45000, "Cómputo Alto Rendimiento", stock_disponible=2)
        s_asesoria = AsesoriaEspecializada("SRV-03", "Arquitectura Cloud", 120000, "Nube y Microservicios", nivel_consultor="Arquitecto")
        gestor.registrar_servicio(s_sala)
        gestor.registrar_servicio(s_equipo)
        gestor.registrar_servicio(s_asesoria)
        for srv in gestor.servicios:
            print(f"  OK -> {srv.describir_servicio()}")
    except SistemaFJError as exc:
        gestor.logger.registrar_error(exc, "Op 4")

    # 5. Creación incorrecta de servicios (tarifa negativa y nivel inválido)
    print("\n[Operación 5] Creación incorrecta de servicios (parámetros inválidos):")
    try:
        s_err1 = ReservaSala("SRV-ERR1", "Sala Fantasma", -50000, capacidad_maxima=5)
        gestor.registrar_servicio(s_err1)
    except SistemaFJError as exc:
        gestor.logger.registrar_error(exc, "Op 5a - Tarifa negativa")
        print(f"  [EXCEPCIÓN CAPTURADA] {exc}")

    try:
        s_err2 = AsesoriaEspecializada("SRV-ERR2", "Soporte Básico", 60000, "Redes", nivel_consultor="MasterSupreme")
        gestor.registrar_servicio(s_err2)
    except SistemaFJError as exc:
        gestor.logger.registrar_error(exc, "Op 5b - Nivel consultor inválido")
        print(f"  [EXCEPCIÓN CAPTURADA] {exc}")

    # 6. Demostración de métodos sobrecargados de cálculo de costos
    print("\n[Operación 6] Cálculo polimórfico y sobrecargado de costos (IVA, exento, descuento):")
    if gestor.servicios:
        sala = gestor.servicios[0]
        print(f"  - Con IVA estándar (3h): ${sala.calcular_costo_total(3):,.2f}")
        print(f"  - Exento de IVA (3h):    ${sala.calcular_costo_total(3, incluir_iva=False):,.2f}")
        print(f"  - Con 15% descuento (3h):${sala.calcular_costo_total(3, descuento_porcentaje=15.0):,.2f}")

    # 7. Reserva exitosa de Sala, confirmación y procesamiento completo
    print("\n[Operación 7] Reserva exitosa, confirmación y procesamiento de Sala:")
    r1 = gestor.crear_reserva("RES-01", "CLI-01", "SRV-01", duracion_horas=4, parametros_extra={"asistentes": 8})
    if r1:
        try:
            r1.confirmar(descuento_porcentaje=10.0)
            factura = r1.procesar()
            print(f"  OK -> {factura}")
        except SistemaFJError as exc:
            print(f"  [EXCEPCIÓN CAPTURADA] {exc}")

    # 8. Reserva fallida por exceso de capacidad en Sala
    print("\n[Operación 8] Reserva fallida de Sala (asistentes superan capacidad máxima):")
    gestor.crear_reserva("RES-02", "CLI-02", "SRV-01", duracion_horas=2, parametros_extra={"asistentes": 25})

    # 9. Reserva exitosa de Alquiler de Equipo (descuenta stock) y segundo intento sin stock
    print("\n[Operación 9] Alquiler de equipos (consumo de stock y fallo por falta de stock):")
    r3 = gestor.crear_reserva("RES-03", "CLI-02", "SRV-02", duracion_horas=5, parametros_extra={"cantidad": 2})
    if r3:
        try:
            r3.confirmar()
            print(f"  OK -> {r3.obtener_resumen()}")
        except SistemaFJError as exc:
            print(f"  [EXCEPCIÓN CAPTURADA] {exc}")

    # Intento de reservar 1 equipo adicional cuando el stock quedó en 0
    gestor.crear_reserva("RES-04", "CLI-01", "SRV-02", duracion_horas=3, parametros_extra={"cantidad": 1})

    # 10. Cancelación de reserva de equipo (libera stock) y error al intentar procesarla luego
    print("\n[Operación 10] Cancelación de reserva (libera stock) + intento inválido de procesar cancelada:")
    if r3:
        try:
            r3.cancelar("Cambio de cronograma del proyecto")
            print(f"  OK -> {r3.obtener_resumen()}")
            # Intento prohibido: procesar una reserva ya cancelada (prueba encadenamiento de excepciones)
            r3.procesar()
        except SistemaFJError as exc:
            print(f"  [EXCEPCIÓN ENCADENADA CAPTURADA] {exc} | Causa: {exc.__cause__}")

    # 11. Reserva fallida por duración inválida en Asesoría Especializada (> 8 horas)
    print("\n[Operación 11] Reserva fallida de Asesoría (duración excede jornada de 8 horas):")
    gestor.crear_reserva("RES-05", "CLI-01", "SRV-03", duracion_horas=10, parametros_extra={"modalidad": "Remota"})

    # 12. Reserva exitosa de Asesoría Especializada y procesamiento final
    print("\n[Operación 12] Reserva exitosa y procesamiento de Asesoría Especializada:")
    r6 = gestor.crear_reserva("RES-06", "CLI-01", "SRV-03", duracion_horas=3, parametros_extra={"modalidad": "Presencial"})
    if r6:
        try:
            r6.confirmar()
            print(f"  OK -> {r6.procesar()}")
        except SistemaFJError as exc:
            print(f"  [EXCEPCIÓN CAPTURADA] {exc}")

    print("\n" + "=" * 80)
    print(f"SIMULACIÓN FINALIZADA SIN INTERRUPCIONES. Logs guardados en: {gestor.logger.ruta_archivo}")
    print("=" * 80)


def menu_interactivo(gestor: GestorSoftwareFJ) -> None:
    while True:
        print("\n--- MENÚ INTERACTIVO SOFTWARE FJ ---")
        print("1. Listar clientes registrados")
        print("2. Listar servicios disponibles")
        print("3. Listar reservas")
        print("4. Registrar nuevo cliente")
        print("5. Crear y confirmar reserva")
        print("6. Ver últimas 10 líneas del archivo de logs")
        print("0. Salir")

        opcion = input("Seleccione una opción: ").strip()
        try:
            if opcion == "1":
                for c in gestor.clientes:
                    print(" ", c.obtener_resumen())
            elif opcion == "2":
                for s in gestor.servicios:
                    print(" ", s.describir_servicio())
            elif opcion == "3":
                for r in gestor.reservas:
                    print(" ", r.obtener_resumen())
            elif opcion == "4":
                id_c = input("ID Cliente (ej. CLI-05): ")
                nom = input("Nombre completo: ")
                doc = input("Documento (6-12 dígitos): ")
                cor = input("Correo electrónico: ")
                tel = input("Teléfono (7-10 dígitos): ")
                nuevo = Cliente(id_c, nom, doc, cor, tel)
                if gestor.registrar_cliente(nuevo):
                    print("Cliente registrado exitosamente.")
            elif opcion == "5":
                id_r = input("ID Reserva (ej. RES-10): ")
                id_c = input("ID Cliente: ")
                id_s = input("ID Servicio: ")
                horas = int(input("Duración en horas: "))
                res = gestor.crear_reserva(id_r, id_c, id_s, horas)
                if res:
                    res.confirmar()
                    print("Reserva creada y confirmada:", res.obtener_resumen())
            elif opcion == "6":
                with open(gestor.logger.ruta_archivo, "r", encoding="utf-8") as f:
                    lineas = f.readlines()
                    for linea in lineas[-10:]:
                        print(" ", linea.strip())
            elif opcion == "0":
                print("Cerrando sistema Software FJ. ¡Hasta pronto!")
                break
            else:
                print("Opción no válida.")
        except ValueError as err:
            gestor.logger.registrar_error(err, "Entrada numérica inválida en menú")
            print("  [ERROR] Debe ingresar un valor numérico válido.")
        except SistemaFJError as err:
            gestor.logger.registrar_error(err, "Operación en menú interactivo")
            print(f"  [ERROR CONTROLADO] {err}")


if __name__ == "__main__":
    sistema = GestorSoftwareFJ("logs_software_fj.log")
    ejecutar_simulacion_completa(sistema)
    # Descomenta la siguiente línea si deseas usar también el menú interactivo en consola:
    # menu_interactivo(sistema)
