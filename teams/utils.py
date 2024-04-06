from teams.exceptions import NegativeTitlesError, ImpossibleTitlesError, InvalidYearCupError


def data_processing(dict: dict):
    if dict["titles"] < 0:
        raise NegativeTitlesError("titles cannot be negative")

    if dict["first_cup"] < 1930:
        raise InvalidYearCupError("there was no world cup this year")

    if dict["titles"] > 23:
        raise ImpossibleTitlesError("impossible to have more titles than disputed cups")