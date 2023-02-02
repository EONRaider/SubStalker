import argparse

class CLIArgumentsParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description="Enumerate subdomains on given target(s)"
        )
        self.target_group = self.parser.add_mutually_exclusive_group(required=True)
        self.args = None

    def parse(self, *args, **kwargs) -> argparse.Namespace:
        self.target_group.add_argument(
            "-u",
            "--url",
            type=str,
            help="Target URL to enumerate"
        )
        self.target_group.add_argument(
            "-U",
            "--url-list",
            type=str,
            help="Can pass multiple URLs separated by a comma"
            " or a wordlist (one URL per line)"
        )
        self.parser.add_argument(
            "-o",
            "--output",
            type=str,
            help="Save the output to the specified filepath"
        )
        self.parser.add_argument(
            "-t",
            "--threads",
            type=int,
            help="Specify number of threads (default=10)",
            default=10
        )

        self.args = self.parser.parse_args(*args, **kwargs)

        self.args.url = tuple(self.parse_urls())

        return self.args

    @staticmethod
    def read_from_file(filepath):
        try:
            with open(filepath, mode="r", encoding="utf-8") as f:
                yield from (str(line.strip()) for line in f)
        except FileNotFoundError:
            raise SystemExit(f"Error reading from file {filepath}")

    def parse_urls (self):
        if self.args.url:
            yield str(self.args.url)
        elif self.args.url_list:
            if "," in self.args.url_list:
                for url in self.args.url_list.split(","):
                    yield url
            else:
                yield from self.read_from_file(self.args.url_list)
