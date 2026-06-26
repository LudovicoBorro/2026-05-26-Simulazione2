from dataclasses import dataclass
import datetime

@dataclass
class Actor:
    id: str
    name: str
    height: int
    date_of_birth: datetime.date
    known_for_movies: str

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return f"{self.name}"