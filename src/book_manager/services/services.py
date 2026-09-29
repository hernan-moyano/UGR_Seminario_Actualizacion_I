"""Servicios del sistema Book Manager.

Contiene la lógica de negocio que se aplica a cada operación CRUD,
la validación de relaciones entre entidades y los reportes del sistema.
"""
from __future__ import annotations

from datetime import date
from typing import Dict, List, Optional

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
from book_manager.repositories.repositories import (
    RepositorioCotizacionDolarEnMemoria,
    RepositorioEnMemoria,
    RepositorioStockEnMemoria,
)


class LibreriaService:
    """Servicio central: concentra la lógica de negocio de la librería."""

    def __init__(self) -> None:
        self.repo_generos = RepositorioEnMemoria[Genero]()
        self.repo_editoriales = RepositorioEnMemoria[Editorial]()
        self.repo_monedas = RepositorioEnMemoria[Moneda]()
        self.repo_tipos_cotizacion = RepositorioEnMemoria[TipoCotizacion]()
        self.repo_libros = RepositorioEnMemoria[Libro]()
        self.repo_precios = RepositorioEnMemoria[Precio]()
        self.repo_stock = RepositorioStockEnMemoria()
        self.repo_cotizaciones = RepositorioCotizacionDolarEnMemoria()

    # ------------------------------ CRUD Genero ------------------------------
    def alta_genero(self, genero: Genero) -> Genero:
        return self.repo_generos.crear(genero)

    def modificar_genero(self, genero: Genero) -> Genero:
        return self.repo_generos.actualizar(genero)

    def eliminar_genero(self, id: int) -> bool:
        return self.repo_generos.eliminar(id)

    def listar_generos(self) -> List[Genero]:
        return self.repo_generos.leer_todos()

    # --------------------------- CRUD Editorial ------------------------------
    def alta_editorial(self, editorial: Editorial) -> Editorial:
        return self.repo_editoriales.crear(editorial)

    def modificar_editorial(self, editorial: Editorial) -> Editorial:
        return self.repo_editoriales.actualizar(editorial)

    def eliminar_editorial(self, id: int) -> bool:
        return self.repo_editoriales.eliminar(id)

    def listar_editoriales(self) -> List[Editorial]:
        return self.repo_editoriales.leer_todos()

    # ----------------------------- CRUD Moneda -------------------------------
    def alta_moneda(self, moneda: Moneda) -> Moneda:
        return self.repo_monedas.crear(moneda)

    def modificar_moneda(self, moneda: Moneda) -> Moneda:
        return self.repo_monedas.actualizar(moneda)

    def eliminar_moneda(self, id: int) -> bool:
        return self.repo_monedas.eliminar(id)

    def listar_monedas(self) -> List[Moneda]:
        return self.repo_monedas.leer_todos()

    # ------------------------ CRUD TipoCotizacion ----------------------------
    def alta_tipo_cotizacion(self, tipo: TipoCotizacion) -> TipoCotizacion:
        return self.repo_tipos_cotizacion.crear(tipo)

    def modificar_tipo_cotizacion(self, tipo: TipoCotizacion) -> TipoCotizacion:
        return self.repo_tipos_cotizacion.actualizar(tipo)

    def eliminar_tipo_cotizacion(self, id: int) -> bool:
        return self.repo_tipos_cotizacion.eliminar(id)

    def listar_tipos_cotizacion(self) -> List[TipoCotizacion]:
        return self.repo_tipos_cotizacion.leer_todos()

    # ------------------------------ CRUD Libro -------------------------------
    def _validar_relaciones_libro(self, libro: Libro) -> None:
        """Verifica que la editorial y el género del libro existan."""
        if self.repo_editoriales.leer_por_id(libro.editorial_id) is None:
            raise ValueError("Editorial inexistente")
        if self.repo_generos.leer_por_id(libro.genero_id) is None:
            raise ValueError("Género inexistente")

    def alta_libro(self, libro: Libro) -> Libro:
        self._validar_relaciones_libro(libro)
        return self.repo_libros.crear(libro)

    def modificar_libro(self, libro: Libro) -> Libro:
        self._validar_relaciones_libro(libro)
        return self.repo_libros.actualizar(libro)

    def eliminar_libro(self, id: int) -> bool:
        return self.repo_libros.eliminar(id)

    def listar_libros(self) -> List[Libro]:
        return self.repo_libros.leer_todos()

    # ------------------------------ CRUD Precio ------------------------------
    def _validar_relaciones_precio(self, precio: Precio) -> None:
        """Verifica que el libro y la moneda del precio existan."""
        if self.repo_libros.leer_por_id(precio.libro_id) is None:
            raise ValueError("Libro inexistente")
        if self.repo_monedas.leer_por_id(precio.moneda_id) is None:
            raise ValueError("Moneda inexistente")

    def alta_precio(self, precio: Precio) -> Precio:
        self._validar_relaciones_precio(precio)
        return self.repo_precios.crear(precio)

    def modificar_precio(self, precio: Precio) -> Precio:
        self._validar_relaciones_precio(precio)
        return self.repo_precios.actualizar(precio)

    def eliminar_precio(self, id: int) -> bool:
        return self.repo_precios.eliminar(id)

    def listar_precios(self) -> List[Precio]:
        return self.repo_precios.leer_todos()

    # ------------------------------ CRUD Stock -------------------------------
    def _validar_relaciones_stock(self, stock: Stock) -> None:
        """Verifica que el libro asociado al stock exista."""
        if self.repo_libros.leer_por_id(stock.libro_id) is None:
            raise ValueError("Libro inexistente")

    def alta_stock(self, stock: Stock) -> Stock:
        self._validar_relaciones_stock(stock)
        return self.repo_stock.crear(stock)

    def modificar_stock(self, stock: Stock) -> Stock:
        self._validar_relaciones_stock(stock)
        return self.repo_stock.actualizar(stock)

    def eliminar_stock(self, libro_id: int) -> bool:
        return self.repo_stock.eliminar(libro_id)

    def listar_stock(self) -> List[Stock]:
        return self.repo_stock.leer_todos()

    # ------------------------- CRUD CotizacionDolar --------------------------
    def _validar_relaciones_cotizacion(self, cotizacion: CotizacionDolar) -> None:
        """Verifica que el tipo de cotización exista."""
        if self.repo_tipos_cotizacion.leer_por_id(cotizacion.tipo_id) is None:
            raise ValueError("Tipo de cotización inexistente")

    def alta_cotizacion(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        self._validar_relaciones_cotizacion(cotizacion)
        return self.repo_cotizaciones.crear(cotizacion)

    def modificar_cotizacion(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        self._validar_relaciones_cotizacion(cotizacion)
        return self.repo_cotizaciones.actualizar(cotizacion)

    def eliminar_cotizacion(self, tipo_id: int, fecha: date) -> bool:
        return self.repo_cotizaciones.eliminar(tipo_id, fecha)

    def listar_cotizaciones(
        self, tipo_id: Optional[int] = None
    ) -> List[CotizacionDolar]:
        if tipo_id is not None:
            return self.repo_cotizaciones.leer_historico_por_tipo(tipo_id)
        salida: List[CotizacionDolar] = []
        for tipo in self.repo_tipos_cotizacion.leer_todos():
            salida.extend(self.repo_cotizaciones.leer_historico_por_tipo(tipo.id))
        return sorted(salida, key=lambda x: (x.tipo_id, x.fecha))

    # ------------------------------- Reportes --------------------------------
    def reporte_stock_bajo(self, minimo: int = 5) -> List[Stock]:
        """Libros cuyo stock es menor o igual al mínimo indicado."""
        return [s for s in self.repo_stock.leer_todos() if s.cantidad <= minimo]

    def reporte_libros_por_genero(self) -> Dict[str, List[Libro]]:
        """Agrupa los libros del catálogo por nombre de género."""
        genero_map = {g.id: g.nombre for g in self.repo_generos.leer_todos()}
        salida: Dict[str, List[Libro]] = {}
        for libro in self.repo_libros.leer_todos():
            nombre = genero_map.get(libro.genero_id, "Sin género")
            salida.setdefault(nombre, []).append(libro)
        return salida

    def cotizacion_hoy(self, tipo_id: int) -> Optional[float]:
        """Valor de la cotización del día para el tipo indicado."""
        item = self.repo_cotizaciones.leer_por_tipo_y_fecha(tipo_id, date.today())
        return None if item is None else item.valor
