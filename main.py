#!/usr/bin/env python3
"""
microPROLOG - A simplified PROLOG interpreter.
Main entry point.
"""
import sys
from repl import REPL


def main():
    """Start the microPROLOG REPL."""
    repl = REPL()
    
    # Check if a file was provided as command line argument
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        print(f"microPROLOG v1.0")
        print(f"Loading {filename}...")
        print()
        repl._load_file(filename)
        print()
    
    repl.run()


if __name__ == "__main__":
    main()
