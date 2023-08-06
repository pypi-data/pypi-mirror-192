import math

from httpx import (
    AsyncClient,
    TimeoutException,
    NetworkError,
    InvalidURL,
    ProtocolError,
    CookieConflict,
    HTTPStatusError, HTTPError, StreamError,
)


def unpack_matrix(old_matrix: list[list[int]]) -> list[int]:
    result = []
    while old_matrix:
        result += old_matrix[-1][::-1]
        del old_matrix[-1]

        if old_matrix:
            for row in old_matrix[-1::-1]:
                result.append(row[0])
                del row[0]

            if old_matrix:
                result += old_matrix[0]
                del old_matrix[0]

                for row in old_matrix:
                    result.append(row[-1])
                    del row[-1]
    return result


def create_matrix(matrix_elements: list[int]) -> list[list[int]]:
    matrix_size = int(math.sqrt(len(matrix_elements)))
    if not matrix_size:
        return [[]]
    return [
        matrix_elements[i:i + matrix_size]
        for i in range(0, len(matrix_elements), matrix_size)
    ]


async def matrix_parse(url: str) -> list[int]:
    try:
        async with AsyncClient() as client:
            response = await client.get(url)

        if response.status_code == 200:
            matrix_elements = [
                int(x) for x in response.text.split() if x.isalnum()
            ]
            old_matrix = create_matrix(matrix_elements)
            return unpack_matrix(old_matrix)

        response.raise_for_status()
    except TimeoutException as _:
        print(f"An operation has timed out, while requesting URL({url!r}).")
    except ProtocolError as _:
        print("The protocol was violated.")
    except NetworkError as exc:
        print(
            f"Error while requesting {exc.request.url!r}, "
            f"check url and try again."
        )
    except InvalidURL as _:
        print(f"URL({url!r}) is improperly formed or cannot be parsed.")
    except CookieConflict as _:
        print(
            "Error, attempted to lookup a cookie by name, "
            "but multiple cookies existed"
        )
    except HTTPStatusError as exc:
        print(
            f"Error response {exc.response.status_code} "
            f"while requesting {exc.request.url!r}."
        )
    except (HTTPError, StreamError) as _:
        print(
            "Something went wrong, please, "
            f"check the URL({url!r}) and try again"
        )
