"""
Parser and tokenizer for microPROLOG syntax.
"""
import re
from typing import List, Tuple, Optional
from terms import Atom, Variable, Compound, List as ListTerm, Term


class TokenType:
    """Token type constants."""
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    LBRACKET = 'LBRACKET'
    RBRACKET = 'RBRACKET'
    PIPE = 'PIPE'
    ATOM = 'ATOM'
    VARIABLE = 'VARIABLE'
    NUMBER = 'NUMBER'
    EOF = 'EOF'


class Token:
    """Represents a token."""
    def __init__(self, type_: str, value: any):
        self.type = type_
        self.value = value
    
    def __repr__(self):
        return f"Token({self.type}, {self.value!r})"


class Tokenizer:
    """Converts string input into tokens."""
    
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.current_char = self.text[0] if text else None
    
    def error(self, msg: str):
        raise SyntaxError(f"Tokenizer error at position {self.pos}: {msg}")
    
    def advance(self):
        """Move to next character."""
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    
    def peek(self, offset: int = 1) -> Optional[str]:
        """Look ahead at character without advancing."""
        peek_pos = self.pos + offset
        if peek_pos < len(self.text):
            return self.text[peek_pos]
        return None
    
    def skip_whitespace(self):
        """Skip whitespace characters."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def skip_comment(self):
        """Skip comments starting with %."""
        if self.current_char == '%':
            while self.current_char is not None and self.current_char != '\n':
                self.advance()
            self.advance()  # Skip newline
    
    def read_number(self) -> Token:
        """Read a number token."""
        num_str = ''
        has_dot = False
        
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if has_dot:
                    break  # Second dot, stop
                has_dot = True
            num_str += self.current_char
            self.advance()
        
        value = float(num_str) if has_dot else int(num_str)
        return Token(TokenType.NUMBER, value)
    
    def read_identifier(self) -> Token:
        """Read an identifier (atom or variable)."""
        id_str = ''
        
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            id_str += self.current_char
            self.advance()
        
        # Variable starts with uppercase or underscore
        if id_str[0].isupper() or id_str[0] == '_':
            return Token(TokenType.VARIABLE, id_str)
        else:
            return Token(TokenType.ATOM, id_str)
    
    def tokenize(self) -> List[Token]:
        """Convert text into list of tokens."""
        tokens = []
        
        while self.current_char is not None:
            # Skip whitespace
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            # Skip comments
            if self.current_char == '%':
                self.skip_comment()
                continue
            
            # Special characters
            if self.current_char == '(':
                tokens.append(Token(TokenType.LPAREN, '('))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TokenType.RPAREN, ')'))
                self.advance()
            elif self.current_char == '[':
                tokens.append(Token(TokenType.LBRACKET, '['))
                self.advance()
            elif self.current_char == ']':
                tokens.append(Token(TokenType.RBRACKET, ']'))
                self.advance()
            elif self.current_char == '|':
                tokens.append(Token(TokenType.PIPE, '|'))
                self.advance()
            
            # Numbers
            elif self.current_char.isdigit():
                tokens.append(self.read_number())
            
            # Identifiers (atoms or variables)
            elif self.current_char.isalpha() or self.current_char == '_':
                tokens.append(self.read_identifier())
            
            else:
                self.error(f"Unexpected character: {self.current_char}")
        
        tokens.append(Token(TokenType.EOF, None))
        return tokens


class Parser:
    """Converts tokens into Term objects."""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def error(self, msg: str):
        raise SyntaxError(f"Parser error at token {self.pos}: {msg}")
    
    def advance(self):
        """Move to next token."""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
    
    def expect(self, token_type: str):
        """Consume a token of expected type."""
        if self.current_token.type != token_type:
            self.error(f"Expected {token_type}, got {self.current_token.type}")
        self.advance()
    
    def parse_term(self) -> Term:
        """Parse a single term (atom, variable, compound, or list)."""
        
        # Atom
        if self.current_token.type == TokenType.ATOM:
            value = self.current_token.value
            self.advance()
            return Atom(value)
        
        # Variable
        elif self.current_token.type == TokenType.VARIABLE:
            name = self.current_token.value
            self.advance()
            return Variable(name)
        
        # Number
        elif self.current_token.type == TokenType.NUMBER:
            value = self.current_token.value
            self.advance()
            return Atom(value)
        
        # Compound term: (functor arg1 arg2 ...) or special list form
        elif self.current_token.type == TokenType.LPAREN:
            self.advance()  # Consume '('
            
            # Empty parentheses
            if self.current_token.type == TokenType.RPAREN:
                self.error("Empty compound term")
            
            # Check if first element is a compound (for rules like ((head) body...))
            # or an atom (normal compound term)
            if self.current_token.type == TokenType.LPAREN:
                # Special case: list of compounds (used for rules)
                # Parse as compound with empty functor, treating all elements as args
                args = []
                args.append(self.parse_term())  # Parse first compound
                
                # Parse remaining elements
                while self.current_token.type != TokenType.RPAREN:
                    if self.current_token.type == TokenType.EOF:
                        self.error("Unexpected EOF in compound term")
                    args.append(self.parse_term())
                
                self.expect(TokenType.RPAREN)
                # Return as a special compound with empty string functor
                return Compound("", tuple(args))
            
            # Functor must be an atom
            if self.current_token.type != TokenType.ATOM:
                self.error(f"Compound functor must be an atom, got {self.current_token.type}")
            
            functor = self.current_token.value
            self.advance()
            
            # Parse arguments
            args = []
            while self.current_token.type != TokenType.RPAREN:
                if self.current_token.type == TokenType.EOF:
                    self.error("Unexpected EOF in compound term")
                args.append(self.parse_term())
            
            self.expect(TokenType.RPAREN)
            return Compound(functor, tuple(args))
        
        # List: [elem1 elem2 ...] or [elem1 | tail]
        elif self.current_token.type == TokenType.LBRACKET:
            self.advance()  # Consume '['
            
            # Empty list
            if self.current_token.type == TokenType.RBRACKET:
                self.advance()
                return ListTerm(tuple())
            
            # Parse elements
            elements = []
            tail = None
            
            while True:
                if self.current_token.type == TokenType.RBRACKET:
                    break
                
                if self.current_token.type == TokenType.PIPE:
                    # List with tail: [elem1 elem2 | tail]
                    self.advance()  # Consume '|'
                    tail = self.parse_term()
                    break
                
                elements.append(self.parse_term())
            
            self.expect(TokenType.RBRACKET)
            return ListTerm(tuple(elements), tail)
        
        else:
            self.error(f"Unexpected token: {self.current_token}")
    
    def parse(self) -> Term:
        """Parse input and return a term."""
        term = self.parse_term()
        if self.current_token.type != TokenType.EOF:
            self.error(f"Unexpected tokens after term: {self.current_token}")
        return term


def parse_text(text: str) -> Term:
    """Convenience function to parse text into a term."""
    tokenizer = Tokenizer(text)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    return parser.parse()
