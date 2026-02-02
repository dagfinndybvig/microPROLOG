#!/usr/bin/env python3
"""
microPROLOG - A simplified PROLOG interpreter.
Main entry point.
"""
from repl import REPL


def main():
    """Start the microPROLOG REPL."""
    repl = REPL()
    repl.run()


if __name__ == "__main__":
    main()
