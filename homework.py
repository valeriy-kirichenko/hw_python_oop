from dataclasses import dataclass, fields
from typing import List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE = (
        'Тип тренировки: {}; '
        'Длительность: {:.3f} ч.; '
        'Дистанция: {:.3f} км; '
        'Ср. скорость: {:.3f} км/ч; '
        'Потрачено ккал: {:.3f}.'
    )

    def get_message(self) -> str:
        """Вернуть информационное сообщение о тренировке."""
        return self.MESSAGE.format(
            self.training_type,
            self.duration,
            self.distance,
            self.speed,
            self.calories
        )


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    LEN_STEP = 0.65
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_HOUR = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Необходимо переопределить get_spent_calories в %s.'
            % (self.__class__.__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            training_type=type(self).__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories()
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""
    SPEED_MULTIPLIER = 18
    SPEED_SHIFT = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.SPEED_MULTIPLIER * self.get_mean_speed()
             - self.SPEED_SHIFT)
            * self.weight / self.M_IN_KM * self.duration
            * self.MIN_IN_HOUR
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float
    WEIGHT_MULTIPLIER_1 = 0.035
    WEIGHT_MULTIPLIER_2 = 0.029

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.WEIGHT_MULTIPLIER_1 * self.weight
             + (self.get_mean_speed()**2 // self.height)
             * self.WEIGHT_MULTIPLIER_2
             * self.weight) * self.duration * self.MIN_IN_HOUR
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float
    count_pool: int
    LEN_STEP = 1.38
    SPEED_SHIFT = 1.1
    WEIGHT_MULTIPLIER = 2

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.get_mean_speed() + self.SPEED_SHIFT)
            * self.WEIGHT_MULTIPLIER * self.weight
        )


TRAININGS = {
    'RUN': Running,
    'WLK': SportsWalking,
    'SWM': Swimming
}

WORKOUT_MESSAGE = '"{type}" is unsupported type'
LEN_DATA_MESSAGE = (
    'Incorrect amount of data for {training}: {len_data}. '
    'Expected: {len_fields}'
)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in TRAININGS:
        raise KeyError(WORKOUT_MESSAGE.format(type=workout_type))
    training = TRAININGS[workout_type]
    if len(fields(training)) != len(data):
        raise TypeError(
            LEN_DATA_MESSAGE.format(
                training=training.__name__,
                len_data=len(data),
                len_fields=len(fields(training))
            )
        )
    return training(*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
