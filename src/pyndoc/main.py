import argparse
from src.pyndoc.readers import reader
from src.pyndoc.writers.native_writer import NativeWriter


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="Pyndoc", description="Converter of markup languages."
    )

    parser.add_argument("-f", "--from", dest="from_format", help="Source format")
    parser.add_argument("-t", "--to", dest="to_format", help="Target format")
    parser.add_argument("file", help="Input file")
    parser.add_argument(
        "-o", "--output", dest="output", default=None, help="Output file (optional)"
    )
    parser.add_argument(
        "-n", dest="native", choices=["native"], help="Perform native format."
    )

    args = parser.parse_args()

    input_file = args.file
    output_file = args.output
    from_format = args.from_format
    native_action = args.native

    try:
        if not from_format:
            file_extension = input_file.split(".")[-1]
            from_format = file_extension.lstrip(".").lower()

        if not from_format:
            raise ValueError(
                "Could not determine the source format from the file extension."
            )

        r = reader.Reader(from_format)
        r.read(input_file)

        if native_action == "native":
            native = NativeWriter()
            native.print_tree(r._parser._tree)
            if output_file:
                native.write_tree_to_file(output_file, r._parser._tree)
            return

        if output_file:
            with open(output_file, "w") as file:
                file.write("\n".join(str(element) for element in r._parser._tree))

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
