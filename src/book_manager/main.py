"""Punto de entrada del sistema Book Manager."""
from __future__ import annotations

from book_manager.preload_data.preload_data import (
    cargar_datos_desde_csv,
    generar_csv_demo,
)
from book_manager.services.services import LibreriaService
from book_manager.ui.console import ConsolaLibreria


def crear_app(import_default_data: bool = True) -> LibreriaService:
    """Crea la aplicación y, opcionalmente, carga los datos CSV iniciales."""
    service = LibreriaService()
    if import_default_data:
        base_csv = generar_csv_demo()
        cargar_datos_desde_csv(service, str(base_csv))
    return service


def main(
    import_default_data: bool = True, interactive: bool = True
) -> LibreriaService:
    """Inicia la aplicación.

    ``interactive=False`` permite validar el notebook con "Ejecutar todo"
    sin bloquear la ejecución esperando entradas del usuario.
    """
    service = crear_app(import_default_data=import_default_data)
    if interactive:
        ConsolaLibreria(service).ejecutar()
    return service


if __name__ == "__main__":
    main(import_default_data=True, interactive=True)
