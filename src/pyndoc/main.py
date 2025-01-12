import argparse
from pyndoc.readers import reader
from pyndoc.writers.native_writer import NativeWriter
from pyndoc.writers.latex_writer import LatexWriter
from pyndoc.writers.typst_writer import TypstWriter

writers_dict = {"native": NativeWriter(), "latex": LatexWriter(), "typst": TypstWriter()}


def main() -> None:
    parser = argparse.ArgumentParser(prog="Pyndoc", description="Converter of markup languages.")

    parser.add_argument("-f", "--from", dest="from_format", help="Source format")
    parser.add_argument("-t", "--to", dest="to_format", help="Target format")
    parser.add_argument("file", help="Input file")
    parser.add_argument("-o", "--output", dest="output", default=None, help="Output file (optional)")

    args = parser.parse_args()

    input_file = args.file
    output_file = args.output
    from_format = args.from_format
    to_format = args.to_format

    try:
        if not from_format:
            file_extension = input_file.split(".")[-1]
            from_format = file_extension.lstrip(".").lower()

        if not from_format:
            raise ValueError("Could not determine the source format from the file extension.")

        r = reader.Reader(from_format)
        r.read(input_file)

        ast_tree = r._parser._tree
        writer = writers_dict[to_format]

        if output_file:
            writer.write_tree_to_file(output_file, ast_tree)
            return
        writer.print_tree(ast_tree)

    except KeyError:
        print(f"Incorrect target format specified: {to_format}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
