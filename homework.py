class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Возвращает строку сообщения."""
        return (f"Тип тренировки: {self.training_type}; "
                f"Длительность: {'%.3f'% self.duration} ч.; "
                f"Дистанция: {'%.3f'% self.distance} км;p "
                f"Дистанция: {'%.3f'% self.distance} км; "
                f"Ср. скорость: {'%.3f'% self.speed} км/ч; "
                f"Потрачено ккал: {'%.3f'% self.calories}.")


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    M_IN_HOUR: int = 60

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

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1: int = 18
        coeff_calorie_2: int = 20
        return ((coeff_calorie_1 * self.get_mean_speed() - coeff_calorie_2)
                * self.weight / self.M_IN_KM
                * (self.duration * self.M_IN_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1: float = 0.035
        coeff_calorie_2: float = 0.029
        return ((coeff_calorie_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * coeff_calorie_2 * self.weight)
                * (self.duration * self.M_IN_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38

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
        coeff_calorie_1: float = 1.1
        coeff_calorie_2: float = 2
        return ((self.get_mean_speed()
                + coeff_calorie_1)
                * coeff_calorie_2
                * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_dict: Dict[str, Union[Swimming, Running, SportsWalking]]
    workout_type_dict = {'SWM': Swimming,
                         'RUN': Running,
                         'WLK': SportsWalking}
    if workout_type in workout_type_dict:
        return workout_type_dict.get(workout_type)(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    from typing import Dict
    from typing import Union

    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
