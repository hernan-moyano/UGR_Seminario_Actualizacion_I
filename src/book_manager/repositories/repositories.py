"""Repositorios responsables de la persistencia de datos.

Se definen las interfaces (contratos) de cada repositorio y sus
implementaciones en memoria, con el CRUD completo por entidad.
"""
from __future__ import annotations

import abc
import datetime
from typing import Dict, Generic, List, Optional, TypeVar

from book_manager.entities.entities import (
    CotizacionDolar,
    EntidadBase,
    Stock,
)

T = TypeVar("T", bound=EntidadBase)


class IRepositorio(abc.ABC, Generic[T]):
    """Interfaz para repositorios que manejan entidades con operaciones CRUD básicas."""

    @abc.abstractmethod
    def crear(self, entidad: T) -> T:
        """Crea una nueva entidad en el repositorio.

        Args:
            entidad (T): La entidad a crear.

        Returns:
            T: La entidad creada.

        Raises:
            ValueError: Si ya existe una entidad con el mismo ID.
        """
        pass

    @abc.abstractmethod
    def leer_por_id(self, id: int) -> Optional[T]:
        """Lee una entidad del repositorio por su ID.

        Args:
            id (int): El ID de la entidad a leer.

        Returns:
            Optional[T]: La entidad si se encuentra, None en caso contrario.
        """
        pass

    @abc.abstractmethod
    def leer_todos(self) -> List[T]:
        """Lee todas las entidades del repositorio.

        Returns:
            List[T]: Una lista de todas las entidades.
        """
        pass

    @abc.abstractmethod
    def actualizar(self, entidad: T) -> T:
        """Actualiza una entidad existente en el repositorio.

        Args:
            entidad (T): La entidad a actualizar (debe tener un ID existente).

        Returns:
            T: La entidad actualizada.

        Raises:
            ValueError: Si no se encuentra la entidad para actualizar.
        """
        pass

    @abc.abstractmethod
    def eliminar(self, id: int) -> bool:
        """Elimina una entidad del repositorio por su ID.

        Args:
            id (int): El ID de la entidad a eliminar.

        Returns:
            bool: True si la entidad fue eliminada, False si no se encontró.
        """
        pass


class RepositorioEnMemoria(IRepositorio[T], Generic[T]):
    """Implementación en memoria del repositorio genérico (diccionario por ID)."""

    def __init__(self) -> None:
        self._data: Dict[int, T] = {}

    def crear(self, entidad: T) -> T:
        if entidad.id in self._data:
            raise ValueError(f"Ya existe una entidad con id={entidad.id}")
        self._data[entidad.id] = entidad
        return entidad

    def leer_por_id(self, id: int) -> Optional[T]:
        return self._data.get(id)

    def leer_todos(self) -> List[T]:
        return list(self._data.values())

    def actualizar(self, entidad: T) -> T:
        if entidad.id not in self._data:
            raise ValueError(f"No existe entidad con id={entidad.id}")
        self._data[entidad.id] = entidad
        return entidad

    def eliminar(self, id: int) -> bool:
        if id not in self._data:
            return False
        del self._data[id]
        return True


class IRepositorioStock(abc.ABC):
    """Interfaz para repositorios del tipo Stock."""

    @abc.abstractmethod
    def crear(self, stock: Stock) -> Stock:
        """Crea un nuevo registro de stock.

        Args:
            stock (Stock): El objeto Stock a crear.

        Returns:
            Stock: El objeto Stock creado.

        Raises:
            ValueError: Si ya existe un registro de stock para el mismo libro.
        """
        pass

    @abc.abstractmethod
    def leer_por_libro(self, libro_id: int) -> Optional[Stock]:
        """Lee un registro de stock por ID de libro.

        Args:
            libro_id (int): El ID del libro asociado al stock.

        Returns:
            Optional[Stock]: El objeto Stock si se encuentra, None en caso contrario.
        """
        pass

    @abc.abstractmethod
    def actualizar(self, stock: Stock) -> Stock:
        """Actualiza un registro de stock existente.

        Args:
            stock (Stock): El objeto Stock a actualizar (debe tener un libro_id existente).

        Returns:
            Stock: El objeto Stock actualizado.

        Raises:
            ValueError: Si no se encuentra el stock para actualizar.
        """
        pass

    @abc.abstractmethod
    def eliminar(self, libro_id: int) -> bool:
        """Elimina un registro de stock por ID de libro.

        Args:
            libro_id (int): El ID del libro asociado al stock a eliminar.

        Returns:
            bool: True si el stock fue eliminado, False si no se encontró.
        """
        pass


class RepositorioStockEnMemoria(IRepositorioStock):
    """Implementación en memoria del repositorio de Stock (clave: libro_id)."""

    def __init__(self) -> None:
        self._data: Dict[int, Stock] = {}

    def crear(self, stock: Stock) -> Stock:
        if stock.libro_id in self._data:
            raise ValueError(f"Ya existe stock para libro_id={stock.libro_id}")
        self._data[stock.libro_id] = stock
        return stock

    def leer_por_libro(self, libro_id: int) -> Optional[Stock]:
        return self._data.get(libro_id)

    def leer_todos(self) -> List[Stock]:
        return list(self._data.values())

    def actualizar(self, stock: Stock) -> Stock:
        if stock.libro_id not in self._data:
            raise ValueError(f"No existe stock para libro_id={stock.libro_id}")
        self._data[stock.libro_id] = stock
        return stock

    def eliminar(self, libro_id: int) -> bool:
        if libro_id not in self._data:
            return False
        del self._data[libro_id]
        return True


class IRepositorioCotizacionDolar(abc.ABC):
    """Interfaz para repositorios del tipo RepositorioCotizacionDolar."""

    @abc.abstractmethod
    def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        """Crea una nueva cotización de dólar.

        Args:
            cotizacion (CotizacionDolar): El objeto CotizacionDolar a crear.

        Returns:
            CotizacionDolar: El objeto CotizacionDolar creado.

        Raises:
            ValueError: Si ya existe una cotización para el mismo tipo y fecha.
        """
        pass

    @abc.abstractmethod
    def leer_por_tipo_y_fecha(
        self, tipo_id: int, fecha: datetime.date
    ) -> Optional[CotizacionDolar]:
        """Lee una cotización de dólar por tipo y fecha.

        Args:
            tipo_id (int): El ID del tipo de cotización (e.g., 'Oficial', 'Blue').
            fecha (datetime.date): La fecha de la cotización.

        Returns:
            Optional[CotizacionDolar]: La cotización si se encuentra, None en caso contrario.
        """
        pass

    @abc.abstractmethod
    def leer_historico_por_tipo(self, tipo_id: int) -> List[CotizacionDolar]:
        """Lee el histórico de cotizaciones para un tipo específico.

        Args:
            tipo_id (int): El ID del tipo de cotización.

        Returns:
            List[CotizacionDolar]: Una lista de cotizaciones históricas para el tipo dado.
        """
        pass

    @abc.abstractmethod
    def actualizar(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        """Actualiza una cotización de dólar existente.

        Args:
            cotizacion (CotizacionDolar): El objeto CotizacionDolar a actualizar.

        Returns:
            CotizacionDolar: El objeto CotizacionDolar actualizado.
        """
        pass

    @abc.abstractmethod
    def eliminar(self, tipo_id: int, fecha: datetime.date) -> bool:
        """Elimina una cotización de dólar por tipo y fecha.

        Args:
            tipo_id (int): El ID del tipo de cotización.
            fecha (datetime.date): La fecha de la cotización a eliminar.

        Returns:
            bool: True si la cotización fue eliminada, False si no se encontró.
        """
        pass


class RepositorioCotizacionDolarEnMemoria(IRepositorioCotizacionDolar):
    """Implementación en memoria del repositorio de cotizaciones (clave: tipo_id + fecha)."""

    def __init__(self) -> None:
        self._data: Dict[tuple, CotizacionDolar] = {}

    def _key(self, tipo_id: int, fecha: datetime.date) -> tuple:
        return (tipo_id, fecha.isoformat())

    def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        key = self._key(cotizacion.tipo_id, cotizacion.fecha)
        if key in self._data:
            raise ValueError("Ya existe una cotización para el mismo tipo y fecha")
        self._data[key] = cotizacion
        return cotizacion

    def leer_por_tipo_y_fecha(
        self, tipo_id: int, fecha: datetime.date
    ) -> Optional[CotizacionDolar]:
        return self._data.get(self._key(tipo_id, fecha))

    def leer_historico_por_tipo(self, tipo_id: int) -> List[CotizacionDolar]:
        cotizaciones = [x for x in self._data.values() if x.tipo_id == tipo_id]
        return sorted(cotizaciones, key=lambda x: x.fecha)

    def actualizar(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        key = self._key(cotizacion.tipo_id, cotizacion.fecha)
        if key not in self._data:
            raise ValueError("No existe la cotización solicitada")
        self._data[key] = cotizacion
        return cotizacion

    def eliminar(self, tipo_id: int, fecha: datetime.date) -> bool:
        key = self._key(tipo_id, fecha)
        if key not in self._data:
            return False
        del self._data[key]
        return True
