from datetime import date

class InvalidPESEL(Exception):
    pass


def parse_pesel(pesel: str) -> dict:
    if not pesel.isdigit():
        raise InvalidPESEL("PESEL może zawierać tylko cyfry.")

    if len(pesel) != 11:
        raise InvalidPESEL("PESEL powinien mieć dokładnie 11 cyfr.")

    year = int(pesel[0:2])
    month = int(pesel[2:4])
    day = int(pesel[4:6])

    if month > 80:
        year += 1800
        month -= 80
    elif month > 60:
        year += 2200
        month -= 60
    elif month > 40:
        year += 2100
        month -= 40
    elif month > 20:
        year += 2000
        month -= 20
    else:
        year += 1900

    try:
        birth_date = date(year, month, day)
    except ValueError:
        raise InvalidPESEL("Niepoprawna data urodzenia w numerze PESEL.")

    weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
    checksum = sum(int(p) * w for p, w in zip(pesel[:10], weights))
    control_digit = (10 - checksum % 10) % 10
    if control_digit != int(pesel[10]):
        raise InvalidPESEL("Niepoprawna cyfra kontrolna PESEL.")

    gender = 'Kobieta' if int(pesel[9]) % 2 == 0 else 'Mężczyzna'

    return {
        'birth_date': birth_date,
        'gender': gender,
    }