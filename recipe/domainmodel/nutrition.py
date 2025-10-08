import math

DATA_THRESHOLD = 0.01

class Nutrition:
    id_count = 1
    def __init__(self,
                 recipe_id: int,
                 calories : int, fat : int, saturated_fat : int, cholesterol : int,
                 sodium : int, carbohydrate : int, fiber : int, sugar : int, protein : int,
                 id: int | None = None):
        if id is None:
            self.__id = Nutrition.id_count
            Nutrition.id_count += 1
        else:
            self.__id = id
        self.recipe_id = recipe_id
        self.__calories = calories
        self.__fat = fat
        self.__saturated_fat = saturated_fat
        self.__cholesterol = cholesterol
        self.__sodium = sodium
        self.__carbohydrate = carbohydrate
        self.__fiber = fiber
        self.__sugar = sugar
        self.__protein = protein
        self.__score = self.health_score()


    @property
    def id(self):
        return self.__id


    @property
    def score(self):
        return self.__score

    @property
    def calories(self) -> float:
        return self.__calories

    @property
    def fat(self) -> float:
        return self.__fat

    @property
    def saturated_fat(self) -> float:
        return self.__saturated_fat

    @property
    def cholesterol(self) -> float:
        return self.__cholesterol

    @property
    def sodium(self) -> float:
        return self.__sodium

    @property
    def carbohydrates(self) -> float:
        return self.__carbohydrates

    @property
    def fiber(self) -> float:
        return self.__fiber

    @property
    def sugar(self) -> float:
        return self.__sugar

    @property
    def protein(self) -> float:
        return self.__protein

    def __repr__(self):
        nutrition_data = {
            "Calories": self.__calories,
            "Fat": self.__fat,
            "Saturated Fat": self.__saturated_fat,
            "Cholesterol": self.__cholesterol,
            "Sodium": self.__sodium,
            "Carbohydrate": self.__carbohydrate,
            "Fiber": self.__fiber,
            "Sugar": self.__sugar,
            "Protein": self.__protein,
        }
        return nutrition_data

    def __str__(self):
        nutrition_data = {
            "Calories": self.__calories,
            "Fat": self.__fat,
            "Saturated Fat": self.__saturated_fat,
            "Cholesterol": self.__cholesterol,
            "Sodium": self.__sodium,
            "Carbohydrate": self.__carbohydrate,
            "Fiber": self.__fiber,
            "Sugar": self.__sugar,
            "Protein": self.__protein,
        }
        return nutrition_data

    def get_data(self):
        nutrition_data = {
            "Calories": self.__calories,
            "Fat": self.__fat,
            "Saturated Fat": self.__saturated_fat,
            "Cholesterol": self.__cholesterol,
            "Sodium": self.__sodium,
            "Carbohydrate": self.__carbohydrate,
            "Fiber": self.__fiber,
            "Sugar": self.__sugar,
            "Protein": self.__protein,
        }
        return nutrition_data

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
        for key in self.get_data():
            daily_proportion = self.get_data()[key] / daily_limit[key] or 0
            if daily_proportion > DATA_THRESHOLD: #Only calculate with nutrition contributing more than 1% of DI
                proportional_data[key] = self.get_data()[key] / daily_limit[key]
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