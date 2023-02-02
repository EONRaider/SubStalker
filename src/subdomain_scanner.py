from collections.abc import Collection
from concurrent.futures import ThreadPoolExecutor
from reconlib import CRTShAPI, HackerTargetAPI, VirusTotalAPI


class SubdomainScanner:
    def __init__(self, domains: Collection[str], output_file: str, threads: int):
        self.domains = domains
        self.output_file = output_file
        self.threads = threads
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def notify(self, result):
        for observer in self.observers:
            observer.update(result)

    @staticmethod
    def scan_url(domain) -> set[str]:
        apis = CRTShAPI(), HackerTargetAPI(), VirusTotalAPI()
        return set().union(*(api.fetch_subdomains(target=domain) for api in apis))

    def scan(self):
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            try:
                for result in executor.map(self.scan_url, self.domains):
                    self.notify(result)
            except KeyboardInterrupt:
                print("\n[-] Scan ended by user input")

        for observer in self.observers:
            observer.end_output()
