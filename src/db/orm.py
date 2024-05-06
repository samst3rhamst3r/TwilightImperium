import typing as t
import sqlalchemy as sql
from sqlalchemy import orm

@orm.as_declarative()
class ORM_Base:

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

class ORM_TechType(ORM_Base):

    __tablename__ = "tech_type"

    name: orm.Mapped[str] = orm.mapped_column(unique=True)
    color: orm.Mapped[str] = orm.mapped_column(unique=True)

class ORM_PlanetTrait(ORM_Base):

    __tablename__ = "planet_trait"

    trait: orm.Mapped[str] = orm.mapped_column(unique=True)

class ORM_Planet(ORM_Base):

    __tablename__ = "planet"

    name: orm.Mapped[str] = orm.mapped_column(unique=True)
    rsrcs: orm.Mapped[int]
    inf: orm.Mapped[int]
    trait: orm.Mapped[int]
    system_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey("system_tile.id"))
    tech_specialty_id: orm.Mapped[t.Optional[int]] = orm.mapped_column(sql.ForeignKey("tech_type.id"))

    system: orm.Mapped["ORM_SystemTile"] = orm.relationship(back_populates="planets")
    tech_specialty: orm.Mapped[t.Optional["ORM_TechType"]] = orm.relationship()

class ORM_SystemTileColor(ORM_Base):

    __tablename__ = "system_tile_color"

    color: orm.Mapped[str] = orm.mapped_column(unique=True)

class ORM_SystemAnomaly(ORM_Base):

    __tablename__ = "system_anomaly"

    type: orm.Mapped[str] = orm.mapped_column(unique=True)

class ORM_SystemWormhole(ORM_Base):

    __tablename__ = "system_wormhole"

    type: orm.Mapped[str] = orm.mapped_column(unique=True)

class ORM_SystemTile(ORM_Base):

    __tablename__ = "system_tile"

    tile_num: orm.Mapped[int] = orm.mapped_column(unique=True)
    tile_color_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey("system_tile_color.id"))
    anomaly_id: orm.Mapped[t.Optional[int]] = orm.mapped_column(sql.ForeignKey("system_anomaly.id"))
    wormhole_id: orm.Mapped[t.Optional[int]] = orm.mapped_column(sql.ForeignKey("system_wormhole.id"))

    tile_color: orm.Mapped["ORM_SystemTileColor"] = orm.relationship()
    anomaly: orm.Mapped[t.Optional["ORM_SystemAnomaly"]] = orm.relationship()
    wormhole: orm.Mapped[t.Optional["ORM_SystemWormhole"]] = orm.relationship()
    planets: orm.Mapped[t.Optional[t.List["ORM_Planet"]]] = orm.relationship(back_populates="system")

class ORM_Tech(ORM_Base):

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

class ORM_UnitUpgrade(ORM_Tech):
    
    __mapper_args__ = {
        "polymorphic_identity": 1,
    }

class ORM_RegTech(ORM_Tech):

    __mapper_args__ = {
        "polymorphic_identity": 2,
    }

    type_id: orm.Mapped[t.Optional[int]] = orm.mapped_column(sql.ForeignKey("tech_type.id"))

class ORM_Unit(ORM_Base):

    __tablename__ = "unit"

    name: orm.Mapped[str] = orm.mapped_column(unique=True)
    cost: orm.Mapped[t.Optional[int]]
    units_per_cost: orm.Mapped[t.Optional[int]]
    combat: orm.Mapped[t.Optional[int]]
    hits_per_success: orm.Mapped[t.Optional[int]]
    move: orm.Mapped[t.Optional[int]]
    capacity: orm.Mapped[t.Optional[int]]

class ORM_Faction(ORM_Base):

    __tablename__ = "faction"

    name: orm.Mapped[str] = orm.mapped_column(unique=True)
    home_system_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey("system_tile.id"), unique=True)
    flagship_unit_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey("unit.id"), unique=True)
    start_tech_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey("tech.id"))
    max_commodities: orm.Mapped[int]
    start_carriers: orm.Mapped[int] = orm.mapped_column(default=0)
    start_cruisers: orm.Mapped[int] = orm.mapped_column(default=0)
    start_fighters: orm.Mapped[int] = orm.mapped_column(default=0)
    start_infantry: orm.Mapped[int] = orm.mapped_column(default=0)
    start_space_docks: orm.Mapped[int] = orm.mapped_column(default=0)
    start_pds: orm.Mapped[int] = orm.mapped_column(default=0)

    home_system: orm.Mapped["ORM_SystemTile"] = orm.relationship()
    flagship: orm.Mapped["ORM_Unit"] = orm.relationship()
    start_tech: orm.Mapped["ORM_Tech"] = orm.relationship()

class DB_Engine:

    e = sql.create_engine("sqlite:///twilight_imperium.db")

    def __init__(self) -> None:
        pass
