from abc import ABCMeta
from abc import abstractmethod
from dataclasses import asdict
from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import Type
from typing import Union


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    TEXT_MESSAGE: str = ('Тип тренировки: {0}; '
                         'Длительность: {1:.3f} ч.; '
                         'Дистанция: {2:.3f} км; '
                         'Ср. скорость: {3:.3f} км/ч; '
                         'Потрачено ккал: {4:.3f}.')

    def get_message(self) -> str:
        """Возвращает строку сообщения."""
        result_training_data = asdict(self)
        return self.TEXT_MESSAGE.format(*result_training_data.values())


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    M_IN_HOUR: int = 60
    __metaclass__ = ABCMeta

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    @abstractmethod
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Method get_spent_calories() '
                                  'must be overridden in derived classes')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_RUN_1: int = 18
    COEFF_CALORIE_RUN_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFF_CALORIE_RUN_1 * self.get_mean_speed()
                - self.COEFF_CALORIE_RUN_2)
                * self.weight / self.M_IN_KM
                * (self.duration * self.M_IN_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_WLK_1: float = 0.035
    COEFF_CALORIE_WLK_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFF_CALORIE_WLK_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.COEFF_CALORIE_WLK_2 * self.weight)
                * (self.duration * self.M_IN_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEFF_CALORIE_SWM_1: float = 1.1
    COEFF_CALORIE_SWM_2: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed()
                + self.COEFF_CALORIE_SWM_1)
                * self.COEFF_CALORIE_SWM_2
                * self.weight)


def read_package(workout_type: str, data: List[Union[int, float]]) -> Training:
    """Прочитать данные полученные от датчиков."""
    supported_workout_types: Dict[str, Type[Training]]
    supported_workout_types = {'SWM': Swimming,
                               'RUN': Running,
                               'WLK': SportsWalking}
    if workout_type in supported_workout_types:
        return supported_workout_types[workout_type](*data)
    raise ValueError(f'{workout_type} is inappropriate value '
                     f'for training type. Check supported_workout_types '
                     f'in read_package() function.')


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
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
