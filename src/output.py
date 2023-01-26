from abc import ABC, abstractmethod

class Output(ABC):
    def __init__(self, subject):
        subject.attach(self)
        self.subject = subject

    @abstractmethod
    def update(self, domains) -> None:
        pass


class ScreenOutput(Output):
    def __init__(self, subject):
        super().__init__(subject)

    def update(self, domains) -> None:
        for domain in domains:
            print(f"[+] {domain}")
