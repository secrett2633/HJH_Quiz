from collections.abc import Generator
from typing import Any

import phonenumbers
from pydantic.typing import AnyCallable
from pydantic.validators import str_validator


class PhoneNumber(str):
    @classmethod
    def __modify_schema__(cls, field_schema: dict[str, Any]) -> None:
        field_schema.update(type="string", format="phone_number")

    @classmethod
    def __get_validators__(cls) -> Generator[AnyCallable, None, None]:
        # included here and below so the error happens straight away
        yield str_validator
        yield cls.validate

    @classmethod
    def validate(cls: Any, value: str) -> str:
        try:
            parsed_number = phonenumbers.parse(value, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValueError("Invalid phone number")
            formatted_number = phonenumbers.format_number(
                parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL
            )
            return formatted_number
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValueError("Invalid phone number")
