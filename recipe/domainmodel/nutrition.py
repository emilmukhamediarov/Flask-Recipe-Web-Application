import math

DATA_THRESHOLD = 0.01

class Nutrition:
    id_count = 1
    def __init__(self, data: dict):
        self.__data = data
        self.__id = Nutrition.id_count
        Nutrition.id_count += 1
        self.__score = self.health_score()

    @property
    def id(self):
        return self.__id

    @property
    def data(self):
        return self.__data

    @property
    def score(self):
        return self.__score

    def __repr__(self):
        return f"Nutrition(id={self.id}, data={self.data})"

    def __eq__(self, other):
        if not isinstance(other, Nutrition):
            return False
        return self.__id == other.id

    def __lt__(self, other):
        if not isinstance(other, Nutrition):
            return False
        return self.__id < other.__id

    def health_score(self) -> str:
        daily_limit = {
            "Calories": 2000,
            "Fat": 78,
            "Saturated Fat": 20,
            "Cholesterol": 300,
            "Sodium": 2300,
            "Carbohydrate": 275,
            "Fiber": 28,
            "Sugar": 50,
            "Protein": 50,
        }
        missing_data_count = 0
        proportional_data = {}
        for key in self.__data:
            daily_proportion = self.data[key] / daily_limit[key] or 0
            if daily_proportion > DATA_THRESHOLD: #Only calculate with nutrition contributing more than 1% of DI
                proportional_data[key] = self.__data[key] / daily_limit[key]
            else:
                missing_data_count += 1
        if missing_data_count > 3: #If more than 50% of values are missing or insignificant
            return "Insufficient data for Health Score"

        negative_impacts = {
            "Calories": 0.5,
            "Saturated Fat": 0.75,
            "Sodium": 1.0,
            "Sugar": 1.25
        }
        positive_impacts = {
            "Fiber": 1.5,
            "Protein": 1
        }

        mean_neg_impact, mean_pos_impact, neg_weight, pos_weight = 0, 0, 0, 0

        for key in proportional_data:
            if key in negative_impacts:
                mean_neg_impact += negative_impacts[key] * proportional_data[key]
                neg_weight = negative_impacts[key]
            elif key in positive_impacts:
                mean_pos_impact += positive_impacts[key] * proportional_data[key]
                pos_weight = positive_impacts[key]

        if neg_weight > 0:
            mean_neg_impact /= neg_weight
        else:
            mean_neg_impact = 0

        if pos_weight > 0:
            mean_pos_impact /= pos_weight
        else:
            mean_pos_impact = 0

        raw_score = (2*mean_pos_impact - mean_neg_impact) / 3
        scaled_score = 4 / (1 + math.exp(-raw_score))
        rounded_score = round(scaled_score * 2) + 1

        return "★" * (rounded_score // 2) + "⯨" * (rounded_score % 2)