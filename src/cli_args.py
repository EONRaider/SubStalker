import argparse


class CLIArgumentsParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description="Enumerate subdomains on given target(s)",
        )
        self.target_group = self.parser.add_mutually_exclusive_group(required=True)
        self.args = None

    def parse(self, *args, **kwargs) -> argparse.Namespace:
        self.target_group.add_argument(
            "-d", "--domain", type=str, help="Target domain to enumerate"
        )
        self.target_group.add_argument(
            "-D",
            "--domain-list",
            type=str,
            help="Absolute path to a file containing comma- or line-separated domain "
            "names to enumerate",
        )
        self.parser.add_argument(
            "-o", "--output", type=str, help="Save the output to the specified filepath"
        )
        self.parser.add_argument(
            "-t",
            "--threads",
            type=int,
            help="Maximum number of threads to use when enumerating subdomains "
            "(defaults to 10)",
            default=10,
        )

        self.args = self.parser.parse_args(*args, **kwargs)

        self.args.domain = tuple(self.parse_domains())

        return self.args

    @staticmethod
    def read_from_file(filepath):
        try:
            with open(filepath, mode="r", encoding="utf-8") as f:
                yield from (str(line.strip()) for line in f)
        except FileNotFoundError:
            raise SystemExit(f"Error reading from file {filepath}")

    def parse_domains(self):
        if self.args.domain:
            yield str(self.args.domain)
        elif self.args.domain_list:
            if "," in self.args.domain_list:
                for domain in self.args.domain_list.split(","):
                    yield domain
            else:
                yield from self.read_from_file(self.args.domain_list)
