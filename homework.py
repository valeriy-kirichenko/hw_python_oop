from dataclasses import dataclass, field


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float = field(default_factory=float)

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
    LEN_STEP: float = field(default=0.65, init=False)
    M_IN_KM: float = field(default=1000, init=False)
    MIN_IN_HOUR: float = field(default=60, init=False)
    RUN_CALORIE_CONSTANT_1: float = field(default=18, init=False)
    RUN_CALORIE_CONSTANT_2: float = field(default=20, init=False)
    WLK_CALORIE_CONSTANT_1: float = field(default=0.035, init=False)
    WLK_CALORIE_CONSTANT_2: float = field(default=0.029, init=False)
    SWM_CALORIE_CONSTANT_1: float = field(default=1.1, init=False)
    SWM_CALORIE_CONSTANT_2: float = field(default=2, init=False)

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            training_type=type(self).__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.RUN_CALORIE_CONSTANT_1 * self.get_mean_speed()
             - self.RUN_CALORIE_CONSTANT_2)
            * self.weight / self.M_IN_KM * self.duration
            * self.MIN_IN_HOUR
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.WLK_CALORIE_CONSTANT_1 * self.weight
             + (self.get_mean_speed()**2 // self.height)
             * self.WLK_CALORIE_CONSTANT_2
             * self.weight) * self.duration * self.MIN_IN_HOUR
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float
    count_pool: int
    LEN_STEP: float = field(default=1.38, init=False)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.get_mean_speed() + self.SWM_CALORIE_CONSTANT_1)
            * self.SWM_CALORIE_CONSTANT_2 * self.weight
        )


TYPES_AND_TRAININGS = {
    'RUN': Running,
    'WLK': SportsWalking,
    'SWM': Swimming
}

WORKOUT_EXCEPTION = '"{}" is unsupported type'
LEN_DATA_EXCEPTION = 'Incorrect amount of data for {}: {}'


def count_fields(training) -> int:
    """Посчитать количество полей."""
    count = 0
    for i in training.__dataclass_fields__.items():
        if i[1].init is True:
            count += 1
    return count


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type in TYPES_AND_TRAININGS:
        if count_fields(TYPES_AND_TRAININGS[workout_type]) == len(data):
            return TYPES_AND_TRAININGS[workout_type](*data)
        else:
            raise Exception(
                LEN_DATA_EXCEPTION.format(
                    TYPES_AND_TRAININGS[workout_type].__name__,
                    len(data)
                )
            )
    else:
        raise Exception(WORKOUT_EXCEPTION.format(workout_type))


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
