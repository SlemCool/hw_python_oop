from dataclasses import dataclass, asdict
from typing import Dict, Type, ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE_TEXT: ClassVar[str] = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.MESSAGE_TEXT.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    MIN_IN_HOUR: ClassVar[int] = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""

    SPEND_CALORIES_FACTOR: ClassVar[int] = 18
    SPEND_CALORIES_FACTOR_1: ClassVar[int] = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (
                self.SPEND_CALORIES_FACTOR * self.get_mean_speed()
                - self.SPEND_CALORIES_FACTOR_1
            )
            * self.weight
            / self.M_IN_KM
            * (self.duration * self.MIN_IN_HOUR)
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: int
    SPEND_CALORIES_FACTOR: ClassVar[float] = 0.035
    SPEND_CALORIES_FACTOR_1: ClassVar[int] = 2
    SPEND_CALORIES_FACTOR_2: ClassVar[float] = 0.029

    def get_spent_calories(self) -> float:
        return (
            (
                self.SPEND_CALORIES_FACTOR * self.weight
                + (
                    self.get_mean_speed() ** self.SPEND_CALORIES_FACTOR_1
                    // self.height
                )
                * self.SPEND_CALORIES_FACTOR_2
                * self.weight
            )
            * self.duration
            * self.MIN_IN_HOUR
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    length_pool: int
    count_pool: float
    LEN_STEP: ClassVar[float] = 1.38
    SPEND_CALORIES_FACTOR: ClassVar[float] = 1.1
    SPEND_CALORIES_FACTOR_1: ClassVar[int] = 2

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.get_mean_speed() + self.SPEND_CALORIES_FACTOR)
            * self.SPEND_CALORIES_FACTOR_1
            * self.weight
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    types_training: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    if workout_type not in types_training:
        raise ValueError('Не известный тип тренировки.')
    return types_training[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
