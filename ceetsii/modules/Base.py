from pick import pick
from ceetsii.models import Option

class Base:
    def _pick(self, options: list[Option], title: str):
        names = [o.name for o in options]
        _, index = pick(names, title, clear_screen=False)

        options[index].action()
