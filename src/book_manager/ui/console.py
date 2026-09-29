"""Interfaz de consola (CLI) del sistema Book Manager.

Cada menú opera directamente sobre los CRUD del servicio de la librería,
permitiendo listar, dar de alta, modificar y borrar cada entidad.
"""
from __future__ import annotations

from datetime import date
from typing import Callable, List

from book_manager.entities.entities import (
    CotizacionDolar,
    Editorial,
    Genero,
    Libro,
    Moneda,
    Precio,
    Stock,
    TipoCotizacion,
)
from book_manager.services.services import LibreriaService


class ConsolaLibreria:
    """Menús de consola para operar el CRUD de cada entidad del sistema."""

    def __init__(self, service: LibreriaService) -> None:
        self.service = service

    # --------------------------- Utilidades de E/S ---------------------------
    def _leer_int(self, texto: str) -> int:
        return int(input(texto).strip())

    def _leer_float(self, texto: str) -> float:
        return float(input(texto).strip())

    def _pausa(self) -> None:
        input("\nEnter para continuar...")

    def _listar(self, nombre: str, items: List[object]) -> None:
        print(f"\n--- {nombre} ---")
        if not items:
            print("Sin registros")
            return
        for item in items:
            print(item)

    # --------------------------- Menú CRUD genérico --------------------------
    def _menu_crud_basico(
        self,
        titulo: str,
        crear_cb: Callable[[], object],
        actualizar_cb: Callable[[], object],
        eliminar_cb: Callable[[], object],
        listar_cb: Callable[[], List[object]],
    ) -> None:
        while True:
            print(f"\n{titulo}: 1-Listar 2-Alta 3-Modificar 4-Borrar 0-Volver")
            op = input("Opción: ").strip()
            try:
                if op == "1":
                    self._listar(titulo, listar_cb())
                    self._pausa()
                elif op == "2":
                    crear_cb()
                    print("Alta exitosa")
                    self._pausa()
                elif op == "3":
                    actualizar_cb()
                    print("Modificación exitosa")
                    self._pausa()
                elif op == "4":
                    eliminado = eliminar_cb()
                    print("Borrado exitoso" if eliminado else "No se encontró el registro")
                    self._pausa()
                elif op == "0":
                    return
                else:
                    print("Opción inválida")
            except (ValueError, TypeError) as exc:
                print(f"Error: {exc}")
                self._pausa()

    # ---------------------------- Menús por entidad --------------------------
    def menu_generos(self) -> None:
        self._menu_crud_basico(
            "Géneros",
            lambda: self.service.alta_genero(
                Genero(self._leer_int("ID: "), input("Nombre: "))
            ),
            lambda: self.service.modificar_genero(
                Genero(self._leer_int("ID: "), input("Nombre: "))
            ),
            lambda: self.service.eliminar_genero(self._leer_int("ID: ")),
            self.service.listar_generos,
        )

    def menu_editoriales(self) -> None:
        self._menu_crud_basico(
            "Editoriales",
            lambda: self.service.alta_editorial(
                Editorial(self._leer_int("ID: "), input("Nombre: "))
            ),
            lambda: self.service.modificar_editorial(
                Editorial(self._leer_int("ID: "), input("Nombre: "))
            ),
            lambda: self.service.eliminar_editorial(self._leer_int("ID: ")),
            self.service.listar_editoriales,
        )

    def menu_monedas(self) -> None:
        self._menu_crud_basico(
            "Monedas",
            lambda: self.service.alta_moneda(
                Moneda(
                    self._leer_int("ID: "),
                    input("Código: "),
                    input("Descripción: "),
                )
            ),
            lambda: self.service.modificar_moneda(
                Moneda(
                    self._leer_int("ID: "),
                    input("Código: "),
                    input("Descripción: "),
                )
            ),
            lambda: self.service.eliminar_moneda(self._leer_int("ID: ")),
            self.service.listar_monedas,
        )

    def menu_tipos_cotizacion(self) -> None:
        self._menu_crud_basico(
            "Tipos de cotización",
            lambda: self.service.alta_tipo_cotizacion(
                TipoCotizacion(self._leer_int("ID: "), input("Nombre: "))
            ),
            lambda: self.service.modificar_tipo_cotizacion(
                TipoCotizacion(self._leer_int("ID: "), input("Nombre: "))
            ),
            lambda: self.service.eliminar_tipo_cotizacion(self._leer_int("ID: ")),
            self.service.listar_tipos_cotizacion,
        )

    def menu_libros(self) -> None:
        self._menu_crud_basico(
            "Libros",
            lambda: self.service.alta_libro(
                Libro(
                    self._leer_int("ID: "),
                    input("ISBN: "),
                    input("Título: "),
                    input("Autor: "),
                    self._leer_int("Editorial ID: "),
                    self._leer_int("Género ID: "),
                )
            ),
            lambda: self.service.modificar_libro(
                Libro(
                    self._leer_int("ID: "),
                    input("ISBN: "),
                    input("Título: "),
                    input("Autor: "),
                    self._leer_int("Editorial ID: "),
                    self._leer_int("Género ID: "),
                )
            ),
            lambda: self.service.eliminar_libro(self._leer_int("ID: ")),
            self.service.listar_libros,
        )

    def menu_precios(self) -> None:
        self._menu_crud_basico(
            "Precios",
            lambda: self.service.alta_precio(
                Precio(
                    self._leer_int("ID: "),
                    self._leer_int("Libro ID: "),
                    self._leer_int("Moneda ID: "),
                    self._leer_float("Monto: "),
                )
            ),
            lambda: self.service.modificar_precio(
                Precio(
                    self._leer_int("ID: "),
                    self._leer_int("Libro ID: "),
                    self._leer_int("Moneda ID: "),
                    self._leer_float("Monto: "),
                )
            ),
            lambda: self.service.eliminar_precio(self._leer_int("ID: ")),
            self.service.listar_precios,
        )

    def menu_stock(self) -> None:
        self._menu_crud_basico(
            "Stock",
            lambda: self.service.alta_stock(
                Stock(self._leer_int("Libro ID: "), self._leer_int("Cantidad: "))
            ),
            lambda: self.service.modificar_stock(
                Stock(self._leer_int("Libro ID: "), self._leer_int("Cantidad: "))
            ),
            lambda: self.service.eliminar_stock(self._leer_int("Libro ID: ")),
            self.service.listar_stock,
        )

    def menu_cotizaciones(self) -> None:
        self._menu_crud_basico(
            "Cotizaciones",
            lambda: self.service.alta_cotizacion(
                CotizacionDolar(
                    self._leer_int("Tipo ID: "),
                    date.fromisoformat(input("Fecha (YYYY-MM-DD): ").strip()),
                    self._leer_float("Valor: "),
                )
            ),
            lambda: self.service.modificar_cotizacion(
                CotizacionDolar(
                    self._leer_int("Tipo ID: "),
                    date.fromisoformat(input("Fecha (YYYY-MM-DD): ").strip()),
                    self._leer_float("Valor: "),
                )
            ),
            lambda: self.service.eliminar_cotizacion(
                self._leer_int("Tipo ID: "),
                date.fromisoformat(input("Fecha (YYYY-MM-DD): ").strip()),
            ),
            self.service.listar_cotizaciones,
        )

    def menu_reportes(self) -> None:
        print("\n1-Stock bajo\n2-Libros por género")
        op = input("Opción: ").strip()
        if op == "1":
            minimo = self._leer_int("Mínimo: ")
            for item in self.service.reporte_stock_bajo(minimo=minimo):
                print(item)
        elif op == "2":
            reporte = self.service.reporte_libros_por_genero()
            for genero, libros in reporte.items():
                print(f"\n{genero}")
                for libro in libros:
                    print(f"- {libro.titulo}")
        else:
            print("Opción inválida")
        self._pausa()

    # ------------------------------ Menú principal ---------------------------
    def ejecutar(self) -> None:
        while True:
            print("\n=== Book Manager ===")
            print("1. Géneros")
            print("2. Editoriales")
            print("3. Monedas")
            print("4. Tipos de cotización")
            print("5. Libros")
            print("6. Precios")
            print("7. Stock")
            print("8. Cotizaciones")
            print("9. Reportes")
            print("0. Salir")

            opcion = input("Seleccionar opción: ").strip()
            if opcion == "1":
                self.menu_generos()
            elif opcion == "2":
                self.menu_editoriales()
            elif opcion == "3":
                self.menu_monedas()
            elif opcion == "4":
                self.menu_tipos_cotizacion()
            elif opcion == "5":
                self.menu_libros()
            elif opcion == "6":
                self.menu_precios()
            elif opcion == "7":
                self.menu_stock()
            elif opcion == "8":
                self.menu_cotizaciones()
            elif opcion == "9":
                self.menu_reportes()
            elif opcion == "0":
                print("Saliendo...")
                break
            else:
                print("Opción inválida")
