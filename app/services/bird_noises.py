import random

BIRD_SOUNDS = ["squak", "chirp", "tweet", "worble", "caw", "peep", "coo", "trill"]

EXTENDED_SOUNDS = [
    lambda: "Twee" + "eee" * random.randint(5, 15) + "w" + "ee" * random.randint(3, 8),
    lambda: "Haw" + "a" * random.randint(8, 20) + "w!",
    lambda: "Caw" + "a" * random.randint(6, 18) + "w!",
    lambda: "Pee" + "ee" * random.randint(4, 12) + "p" * random.randint(3, 6),
    lambda: "Wor" + "o" * random.randint(5, 15) + "rble",
    lambda: "Squ" + "a" * random.randint(4, 10) + "k!",
    lambda: "C" + "o" * random.randint(4, 40) + "!",
]


def generate_bird_response() -> str:
    if random.randint(1, 50) == 1:
        return extended_sound() + random.choice(["!", "."])

    if random.randint(1, 30) == 1:
        num_sounds = random.randint(50, 150)
    else:
        num_sounds = random.randint(3, 12)

    sounds = [random.choice(BIRD_SOUNDS) for _ in range(num_sounds)]

    result = []
    for i, sound in enumerate(sounds):
        sound = sound.capitalize()

        punct = random.choice(["!", ".", ",", ""])
        if punct == "," and i == len(sounds) - 1:
            punct = random.choice(["!", "."])

        result.append(sound + punct)

    response = " ".join(result)

    if not response.endswith(("!", ".")):
        response = response.rstrip(",") + random.choice(["!", "."])

    return response


def extended_sound() -> str:
    return random.choice(EXTENDED_SOUNDS)()


async def stream_bird_response():
    response = generate_bird_response()
    for char in response:
        yield char
