"""Entidades del dominio del sistema Book Manager.

Cada entidad encapsula sus atributos y valida sus invariantes,
aplicando herencia, propiedades y dataclasses según convenga.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any, Dict


class EntidadBase:
    """Clase base que encapsula el identificador de cada entidad."""

    def __init__(self, id: int) -> None:
        if id <= 0:
            raise ValueError("El id debe ser mayor a cero")
        self._id = id

    @property
    def id(self) -> int:
        """Identificador único de la entidad (solo lectura)."""
        return self._id

    def to_dict(self) -> Dict[str, Any]:
        """Representación de la entidad como diccionario."""
        raise NotImplementedError()


class EntidadNombrada(EntidadBase):
    """Entidad base con nombre encapsulado y validado."""

    def __init__(self, id: int, nombre: str) -> None:
        super().__init__(id)
        self.nombre = nombre

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        valor = valor.strip()
        if not valor:
            raise ValueError("El nombre no puede ser vacío")
        self._nombre = valor

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "nombre": self.nombre}


class Genero(EntidadNombrada):
    """Categoría literaria a la que pertenece un libro."""


class Editorial(EntidadNombrada):
    """Proveedor/distribuidora que provee los libros a la librería."""


class TipoCotizacion(EntidadNombrada):
    """Tipo de cotización del dólar (Oficial, Blue, MEP, etc.)."""


class Moneda(EntidadBase):
    """Moneda en la que se puede expresar un precio (ARS, USD, etc.)."""

    def __init__(self, id: int, codigo: str, descripcion: str) -> None:
        super().__init__(id)
        self.codigo = codigo
        self.descripcion = descripcion

    @property
    def codigo(self) -> str:
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        valor = valor.strip().upper()
        if len(valor) != 3 or not valor.isalpha():
            raise ValueError("El código de moneda debe tener 3 letras")
        self._codigo = valor

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        valor = valor.strip()
        if not valor:
            raise ValueError("La descripción no puede ser vacía")
        self._descripcion = valor

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "codigo": self.codigo,
            "descripcion": self.descripcion,
        }


class Libro(EntidadBase):
    """Cada título del catálogo de la librería."""

    def __init__(
        self,
        id: int,
        isbn: str,
        titulo: str,
        autor: str,
        editorial_id: int,
        genero_id: int,
    ) -> None:
        super().__init__(id)
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.editorial_id = editorial_id
        self.genero_id = genero_id

    @property
    def isbn(self) -> str:
        return self._isbn

    @isbn.setter
    def isbn(self, valor: str) -> None:
        valor = valor.strip()
        if not valor:
            raise ValueError("El ISBN no puede ser vacío")
        self._isbn = valor

    @property
    def titulo(self) -> str:
        return self._titulo

    @titulo.setter
    def titulo(self, valor: str) -> None:
        valor = valor.strip()
        if not valor:
            raise ValueError("El título no puede ser vacío")
        self._titulo = valor

    @property
    def autor(self) -> str:
        return self._autor

    @autor.setter
    def autor(self, valor: str) -> None:
        valor = valor.strip()
        if not valor:
            raise ValueError("El autor no puede ser vacío")
        self._autor = valor

    @property
    def editorial_id(self) -> int:
        return self._editorial_id

    @editorial_id.setter
    def editorial_id(self, valor: int) -> None:
        if valor <= 0:
            raise ValueError("editorial_id inválido")
        self._editorial_id = valor

    @property
    def genero_id(self) -> int:
        return self._genero_id

    @genero_id.setter
    def genero_id(self, valor: int) -> None:
        if valor <= 0:
            raise ValueError("genero_id inválido")
        self._genero_id = valor

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "isbn": self.isbn,
            "titulo": self.titulo,
            "autor": self.autor,
            "editorial_id": self.editorial_id,
            "genero_id": self.genero_id,
        }

    def __str__(self) -> str:
        return f"[{self.id}] {self.titulo} - {self.autor} (ISBN {self.isbn})"


class Precio(EntidadBase):
    """Valor monetario asociado a un libro en una moneda determinada."""

    def __init__(self, id: int, libro_id: int, moneda_id: int, monto: float) -> None:
        super().__init__(id)
        self.libro_id = libro_id
        self.moneda_id = moneda_id
        self.monto = monto

    @property
    def libro_id(self) -> int:
        return self._libro_id

    @libro_id.setter
    def libro_id(self, valor: int) -> None:
        if valor <= 0:
            raise ValueError("libro_id inválido")
        self._libro_id = valor

    @property
    def moneda_id(self) -> int:
        return self._moneda_id

    @moneda_id.setter
    def moneda_id(self, valor: int) -> None:
        if valor <= 0:
            raise ValueError("moneda_id inválido")
        self._moneda_id = valor

    @property
    def monto(self) -> float:
        return self._monto

    @monto.setter
    def monto(self, valor: float) -> None:
        if valor < 0:
            raise ValueError("El monto no puede ser negativo")
        self._monto = float(valor)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "libro_id": self.libro_id,
            "moneda_id": self.moneda_id,
            "monto": self.monto,
        }


@dataclass
class Stock:
    """Cantidad disponible de cada libro (clave: libro_id)."""

    libro_id: int
    cantidad: int

    def __post_init__(self) -> None:
        if self.libro_id <= 0:
            raise ValueError("libro_id inválido")
        if self.cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")

    def to_dict(self) -> Dict[str, Any]:
        return {"libro_id": self.libro_id, "cantidad": self.cantidad}


@dataclass
class CotizacionDolar:
    """Registro histórico de cotización por tipo y fecha."""

    tipo_id: int
    fecha: date
    valor: float

    def __post_init__(self) -> None:
        if self.tipo_id <= 0:
            raise ValueError("tipo_id inválido")
        if self.valor <= 0:
            raise ValueError("La cotización debe ser mayor a cero")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tipo_id": self.tipo_id,
            "fecha": self.fecha.isoformat(),
            "valor": self.valor,
        }
