#!/usr/bin/env python3

# Copyright Louis Paternault 2014-2023
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Main function for the command."""

import collections
import math
import sys
from decimal import Decimal

from pdfautonup import LOGGER, errors, geometry, options, paper, pdfbackend
from pdfautonup.pdfbackend.auto import (  # pylint: disable=no-name-in-module
    PDFFileReader,
)


def lcm(a, b):
    """Return least common divisor of arguments"""
    # pylint: disable=invalid-name, deprecated-method
    return (a * b) // math.gcd(a, b)


def _none_function(*args, **kwargs):  # pylint: disable=unused-argument
    """Accept any number of arguments. and does nothing."""


def _progress_printer(string):
    """Returns a function that prints the progress message."""

    def print_progress(page, total):
        """Print progress message."""
        try:
            text = string.format(
                page=page, total=total, percent=int(page * 100 / total)
            )
        except:  # pylint: disable=bare-except
            text = string
        print(text, end="")
        sys.stdout.flush()

    return print_progress


class PageSequence(collections.abc.Sequence):
    """Sequence of pages of several PDF files."""

    def __init__(self, filenames):
        self.files = []
        self._filenames = filenames

    def __enter__(self):
        for name in self._filenames:
            try:
                if name == "-":
                    self.files.append(PDFFileReader())
                else:
                    self.files.append(PDFFileReader(name))
            except (FileNotFoundError, PermissionError) as error:
                raise errors.PdfautonupError(
                    f"Error while reading file '{name}': {error}."
                )
            except RuntimeError as error:
                raise errors.PdfautonupError(
                    f"Error: Malformed file '{name}': {error}."
                )
        return self

    def __exit__(self, *exc):
        for file in self.files:
            file.close()

    def __iter__(self):
        for pdf in self.files:
            yield from pdf

    def __len__(self):
        return sum(len(pdf) for pdf in self.files)

    def __getitem__(self, index):
        for file in self.files:
            try:
                return file[index]
            except IndexError:
                index -= len(file)
        raise IndexError

    def metadata(self):
        """Aggregate metadata from input files."""
        if len(self.files) == 1:
            return self.files[0].metadata

        input_info = [pdf.metadata for pdf in self.files]
        output_info = {}
        for key in pdfbackend.METADATA_KEYS:
            values = list(
                data[key]
                for data in input_info
                if (key in data and (data[key] is not None))
            )
            if values:
                output_info[key] = " / ".join([f"“{item}”" for item in values])
        return output_info


def nup(arguments, progress=_none_function):
    """Build destination file."""
    # pylint: disable=too-many-branches

    with PageSequence(arguments.files) as pages:
        if not pages:
            raise errors.PdfautonupError("Error: PDF files have no pages to process.")

        page_sizes = list(zip(*[page.mediabox_size for page in pages]))
        source_size = (Decimal(max(page_sizes[0])), Decimal(max(page_sizes[1])))
        target_size = paper.target_papersize(arguments.target_size)

        if [len(set(page_sizes[i])) for i in (0, 1)] != [1, 1]:
            LOGGER.warning(
                "Pages have different sizes. The result might be unexpected."
            )

        if arguments.algorithm is None:
            if arguments.gap[0] is None and arguments.margin[0] is None:
                fit = geometry.Fuzzy
            else:
                fit = geometry.Panelize
        else:
            fit = {"fuzzy": geometry.Fuzzy, "panel": geometry.Panelize}[
                arguments.algorithm
            ]

        dest = fit(source_size, target_size, arguments=arguments)

        if arguments.repeat == "auto":
            if len(pages) == 1:
                arguments.repeat = "fit"
            else:
                arguments.repeat = 1
        if isinstance(arguments.repeat, int):
            repeat = arguments.repeat
        elif arguments.repeat == "fit":
            repeat = lcm(dest.pages_per_page, len(pages)) // len(pages)

        totalpages = repeat * len(pages)
        progress(0, totalpages)
        for destcount in range(math.ceil(totalpages / dest.pages_per_page)):
            with dest.new_page() as destpage:
                for sourcecount in range(
                    destcount * dest.pages_per_page,
                    (destcount + 1) * dest.pages_per_page,
                ):
                    if sourcecount < totalpages:
                        dest.add_page(
                            pages[sourcecount % len(pages)],
                            destpage,
                            sourcecount % dest.pages_per_page,
                        )
                        progress(sourcecount + 1, totalpages)

        dest.write(arguments.output, arguments.files[0], metadata=pages.metadata())


def main():
    """Main function"""
    try:
        arguments = options.commandline_parser().parse_args(sys.argv[1:])

        if arguments.verbose:
            # pylint: disable=no-member
            sys.stderr.write(f"Using pdf backend {pdfbackend.auto.VERSION}\n")

        if "-" in arguments.files and arguments.interactive:
            LOGGER.error(
                """Cannot ask user input while reading files from standard input. """
                """Try removing the "--interactive" (or "-i") option."""
            )
            sys.exit(1)

        nup(arguments, progress=_progress_printer(arguments.progress))
        if not (arguments.progress.endswith("\n") or arguments.progress == ""):
            print()
    except KeyboardInterrupt:
        print()
        sys.exit(1)
    except errors.PdfautonupError as error:
        LOGGER.error(error)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
