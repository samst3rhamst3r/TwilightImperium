import typing as t

import sqlalchemy as sql
from sqlalchemy import orm
from sqlalchemy.ext import associationproxy as proxy

class Base(orm.DeclarativeBase):

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

class TechType(Base):

    __tablename__ = "tech_type"

    name: orm.Mapped[str] = orm.mapped_column(unique=True)
    color: orm.Mapped[str] = orm.mapped_column(unique=True)

class PlanetTrait(Base):

    __tablename__ = "planet_trait"

    trait: orm.Mapped[str] = orm.mapped_column(unique=True)

class Planet(Base):

    __tablename__ = "planet"

    name: orm.Mapped[str] = orm.mapped_column(unique=True)
    rsrcs: orm.Mapped[int]
    inf: orm.Mapped[int]
    trait_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey("planet_trait.id"))
    system_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey("system_tile.id"))
    tech_specialty_id: orm.Mapped[t.Optional[int]] = orm.mapped_column(sql.ForeignKey("tech_type.id"))

    trait: orm.Mapped["PlanetTrait"] = orm.relationship()
    system: orm.Mapped["SystemTile"] = orm.relationship(back_populates="planets")
    tech_specialty: orm.Mapped[t.Optional["TechType"]] = orm.relationship()

class SystemTileColor(Base):

    __tablename__ = "system_tile_color"

    color: orm.Mapped[str] = orm.mapped_column(unique=True)

class SystemAnomaly(Base):

    __tablename__ = "system_anomaly"

    type: orm.Mapped[str] = orm.mapped_column(unique=True)

class SystemWormhole(Base):

    __tablename__ = "system_wormhole"

    type: orm.Mapped[str] = orm.mapped_column(unique=True)

class SystemTile(Base):

    __tablename__ = "system_tile"

    tile_num: orm.Mapped[int] = orm.mapped_column(unique=True)
    tile_color_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey("system_tile_color.id"))
    anomaly_id: orm.Mapped[t.Optional[int]] = orm.mapped_column(sql.ForeignKey("system_anomaly.id"))
    wormhole_id: orm.Mapped[t.Optional[int]] = orm.mapped_column(sql.ForeignKey("system_wormhole.id"))

    tile_color: orm.Mapped["SystemTileColor"] = orm.relationship()
    anomaly: orm.Mapped[t.Optional["SystemAnomaly"]] = orm.relationship()
    wormhole: orm.Mapped[t.Optional["SystemWormhole"]] = orm.relationship()
    planets: orm.Mapped[t.Optional[t.List["Planet"]]] = orm.relationship(back_populates="system")

class Tech(Base):

    __tablename__ = "tech"

    type: orm.Mapped[int]

    __mapper_args__ = {
        "polymorphic_on": "type",
    }

    name: orm.Mapped[str] = orm.mapped_column(unique=True)
    prereq_bio: orm.Mapped[int] = orm.mapped_column(default=0)
    prereq_war: orm.Mapped[int] = orm.mapped_column(default=0)
    prereq_prop: orm.Mapped[int] = orm.mapped_column(default=0)
    prereq_cyber: orm.Mapped[int] = orm.mapped_column(default=0)

class UnitUpgrade(Tech):
    
    __mapper_args__ = {
        "polymorphic_identity": 1,
    }

class RegTech(Tech):

    __mapper_args__ = {
        "polymorphic_identity": 2,
    }

    type_id: orm.Mapped[t.Optional[int]] = orm.mapped_column(sql.ForeignKey("tech_type.id"))

class Ability(Base):

    __tablename__ = "ability"

    name: orm.Mapped[str]

class Unit_Ability_Assoc(Base):
    
    __tablename__ = "unit_ability"

    unit_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey("unit.id"))
    ability_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey("ability.id"))
    success_res: orm.Mapped[t.Optional[int]]
    dice: orm.Mapped[t.Optional[int]]

    unit: orm.Mapped["Unit"] = orm.relationship(back_populates="_unit_ability_assocs")
    ability: orm.Mapped["Ability"] = orm.relationship()

class Unit(Base):

    __tablename__ = "unit"

    name: orm.Mapped[str] = orm.mapped_column(unique=True)
    cost: orm.Mapped[t.Optional[int]]
    units_per_cost: orm.Mapped[t.Optional[int]]
    combat: orm.Mapped[t.Optional[int]]
    hits_per_success: orm.Mapped[t.Optional[int]]
    move: orm.Mapped[t.Optional[int]]
    capacity: orm.Mapped[t.Optional[int]]

    abilities: proxy.AssociationProxy[t.List[int]]

    _unit_ability_assocs: orm.Mapped[t.List["Unit_Ability_Assoc"]] = orm.relationship(back_populates="unit")

class Faction(Base):

    __tablename__ = "faction"

    name: orm.Mapped[str] = orm.mapped_column(unique=True)
    home_system_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey("system_tile.id"), unique=True)
    flagship_unit_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey("unit.id"), unique=True)
    start_tech_id: orm.Mapped[t.Optional[int]] = orm.mapped_column(sql.ForeignKey("tech.id"))
    max_commodities: orm.Mapped[int]
    start_carriers: orm.Mapped[int] = orm.mapped_column(default=0)
    start_cruisers: orm.Mapped[int] = orm.mapped_column(default=0)
    start_fighters: orm.Mapped[int] = orm.mapped_column(default=0)
    start_infantry: orm.Mapped[int] = orm.mapped_column(default=0)
    start_space_docks: orm.Mapped[int] = orm.mapped_column(default=0)
    start_pds: orm.Mapped[int] = orm.mapped_column(default=0)

    home_system: orm.Mapped["SystemTile"] = orm.relationship()
    flagship: orm.Mapped["Unit"] = orm.relationship()
    start_tech: orm.Mapped["Tech"] = orm.relationship()

class DB_Engine:

    e = sql.create_engine("sqlite:///twilight_imperium.db")

    def __init__(self) -> None:
        pass
