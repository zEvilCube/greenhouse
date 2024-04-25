from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class Greenhouse(Base):
    __tablename__ = "greenhouse"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_key = Column(String, unique=True, nullable=False)
    device_key = Column(String, unique=True, nullable=False)

    sensors = relationship("Sensor", back_populates="greenhouse")
    controllers = relationship("Controller", back_populates="greenhouse")


class Sensor(Base):
    __tablename__ = "sensor"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey("greenhouse.id"), nullable=False)
    name = Column(String, default=None)
    type = Column(String, nullable=False)
    reading = Column(Integer)
    reference = Column(Integer)

    greenhouse = relationship("Greenhouse", back_populates="sensors")
    connections = relationship("SensorControllerConnection", back_populates="sensor")


class Controller(Base):
    __tablename__ = "controller"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey("greenhouse.id"), nullable=False)
    name = Column(String, default=None)
    type = Column(String, nullable=False)
    status = Column(Boolean)

    greenhouse = relationship("Greenhouse", back_populates="controllers")
    connections = relationship("SensorControllerConnection", back_populates="controller")


class SensorControllerConnection(Base):
    __tablename__ = "sensor_controller_connection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sensor_id = Column(Integer, ForeignKey("sensor.id"), nullable=False)
    controller_id = Column(Integer, ForeignKey("controller.id"), nullable=False)
    type = Column(String, nullable=False)

    sensor = relationship("Sensor", back_populates="connections")
    controller = relationship("Controller", back_populates="connections")
