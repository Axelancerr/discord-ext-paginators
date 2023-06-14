import enum


__all__ = [
    "CodeblockType",
    "codeblock"
]


class CodeblockType(enum.Enum):
    NONE = 0
    INLINE = 1
    BLOCK = 2


def codeblock(_type: CodeblockType, /, *, language: str | None) -> tuple[str, str]:
    match _type:
        case CodeblockType.NONE:
            return "", ""
        case CodeblockType.INLINE:
            return "`", "`"
        case CodeblockType.BLOCK:
            return (
                f"```{language or ''}\n",
                "\n```"
            )
