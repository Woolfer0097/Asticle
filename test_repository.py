from app.database import Base, SessionLocal, engine
from app.models.article import Tank
from app.repositories.article_repository import TankRepository

Base.metadata.create_all(bind=engine)

db = SessionLocal()

repository = TankRepository(db)

tank = Tank(
    title="XM551 Sheridan",
    photo_path="photo",
    health="1832",
    damage="560",
    armor="25 / 32 / 12",
    recommendation="Предпочтительный стиль игры - атаковать зазевавшихся противников из-за укрытий."
    " Хорошая мобильность позволяет быстро занимать позиции и менять направление. У танка плохой ДПМ, поэтому прямых столкновений"
    " с врагами нужно избегать. (ПТУР'ов больше нет)",
    category="Лёгкий",
    nation="США",
    level="X",
)

repository.delete(1)
repository.create(tank)


tanks = repository.get_all()

for tank in tanks:
    print(
        tank.id,
        tank.title,
        tank.photo_path,
        tank.health,
        tank.damage,
        tank.armor,
        tank.history,
        tank.recommendation,
        tank.category,
        tank.nation,
        tank.level,
    )

db.close()
