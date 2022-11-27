# 
# Assignment one:
# Implementation of a parser tree for TINY Language Parsing
# 
# Submitted By: Chloe Healy - 118720535.
# 
# Reference: Assignment one provided code files for project structure.
#
#

from tiny_scanner import *
from pt_node import *
import sys

import pickle

class TinyParser:
    
     def __init__(self, sourcepath):
        self.__scanner = TinyScanner(sourcepath, verbose = True)
        
     def parse_program(self):
        """ A Program is a statement sequence.
            This fuction will parse tokens matching the following 
            declaration:
            <program > ::= <stmtseq>
        """
        self.__scanner.log("Parsing <program > ::= <stmtseq>")
        # Call the parse_statement_seq fucntion
        c = self.parse_statement_seq()
        return PTNode("program", [c])
     
     def parse_statement_seq(self):     
        """ A function to parse the given statement sequence.
            <stmtseq > ::= <stmtseq> ; <statement> |   <statement>
        """
        self.__scanner.log("Parsing <stmtseq > ::= <stmtseq> ; <statement> |   <statement>")
        
        # Call the parse statement function.
        c = self.parse_statement()
        children = [c]
        while self.__scanner.current.kind in {"ID", "IF", "REPEAT", "ASSIGN", 
                                    "READ", "WRITE"}:
            children.append(self.parse_statement())
            
        return PTNode("statement_sequence", children)
    
     def parse_statement(self):     
        """ A function which will parse the given statement from:
                <statement> ::= <ifstmt> >
            |   <repeatstmt>
            |   <assignstmt>
            |   <readstmt>
            |   <writestmt>
        """
    
        self.__scanner.log("Parsing ::= <ifstmt> > "
                          " |   <repeatstmt>" 
                          " |   <assignstmt>"
                          " |   <readstmt>"
                          " |   <writestmt>  " 
                    )
        

        if self.__scanner.current.kind in {"ID", "READ", "WRITE"}:
            c = self.parse_simple_stmt()
        elif self.__scanner.current.kind == "REPEAT":
            c = self.parse_repeat_stmt()
        elif self.__scanner.current.kind == "ASSIGN":
            c = self.parse_assign_stmt()
        elif self.__scanner.current.kind == "IF":
            c = self.parse_if_stmt()
        else:
            c = self.parse_compound_stmt()
        return PTNode("statement", [c])
       
        return PTNode("statement", [])
    
     def parse_compound_stmt(self):     
        """ A function which parses a compund operation according to the 
            following statement:
            <comp-op> ::= < | =
        """
        self.__scanner.log("Parsing <comp-op> ::= < | =")
        # Get current value of the PTNode
        r = PTNode("comp-op",  [], value = self.__scanner.current.value)
        # Match the statement tokens in order
        if self.__scanner.current.kind in {"LT", "ASSIGN"}:
            self.__scanner.advance()
        return r
        
    
     def parse_simple_stmt(self):     
        """ This function will parse tokens according to the following
            simple statement expression:
            <simple-expr> ::= <simple-expr> <addop> <term> | <term>
        """
        self.__scanner.log("Parsing <simple-expr> ::= <simple-expr> <addop> <term> | <term>")
        
        # Parse the given term - create a list of terms
        t = self.parse_term()
        children = [t]
        # while token contains addop 
        while self.token == "PLUS, MINUS":
            # Parse addop and append to children
            a = self.parse_addop()
            children.append(a)
            # Parse term and append to children
            t = self.parse_term()
            children.append(t)
        # Else parse the term and append to children
        t = self.parse_term()
        children.append(t)
        
        # Return the childrens list.
        return PTNode("simple-exp", children)  
        
     def parse_if_stmt(self):     
        """ This fuction parses tokens according to the following
            declaration of an if statement:
            <ifstmt> ::= if<exp> then <stmtseq> end
            | if <exp> then <stmtseq> else <stmtseq> end
        """
        self.__scanner.log("Parsing Statement: "
                           "<ifstmt> ::= if<exp> then <stmtseq> end"
                           "| if <exp> then <stmtseq> else <stmtseq> end")
        # If the scanner matches if, parse the expression
        self.__scanner.match("IF")
        c = self.parse_expression()
        # Then parse the statement Sequence
        self.__scanner.match("THEN")
        s1 = self.parse_statement_seq()
        children = [c, s1] 
        # If an else statement exists
        if self.__scanner.current.kind == "ELSE":
            self.__scanner.match("ELSE")
            s2 = self.parse_statement()
            children.append(s2)
            # if scanner matches end - return the ptnode
        self.__scanner.match("END")
        return PTNode("selection_stmt", children) 
    
     def parse_read_stmt(self):     
        """ This function will parse tiny tokens according to the 
            following declaration:
            <readstmt>  ::= read identifier
        """
        self.__scanner.log("Parsing <readstmt>  ::= read identifier")
        self.__scanner.match("READ")
        # Set a variable name for the current value of the READ stmt.
        varname = self.__scanner.current.value
        self.__scanner.match("ID")
        return PTNode("readstmt", [], value = varname) 
    
     def parse_write_stmt(self):     
        """ This function will parse tiny tokens according to the 
            following declaration:
            <writestmt>  ::= write <exp>
        """
        self.__scanner.log("Parsing <writestmt>  ::= write <exp>")
        self.__scanner.match("WRITE")
        e = self.parse_expression()
        return PTNode("writestmt", [e]) 
    
     def parse_assign_stmt(self):     
        """ This function will parse tiny tokens according to the 
            following declaration:
            <assignstmt> ::= identifier := <exp>
        """
        self.__scanner.log("Parsing <assignstmt> ::= identifier := <exp>")
        identifier = self.__scanner.match("ID")
        self.__scanner.match("ASSIGN")
        e = self.parse_expression()
        return PTNode("assignstmt", [e], value = identifier) 
    
     def parse_expression(self):     
        """ This function will parse a tiny token expression according 
            to the following declaration:
            <exp> ::= <simple-expr> <comp-op> <simple-expr>
            | <simple-expr>
        """
        self.__scanner.log("Parsing<exp> ::= <simple-expr> <comp-op> <simple-expr>"
                            " | <simple-expr>}")
        
        # Parse the simple statement
        t = self.parse_simple_stmt()
        children = [t]
        # while token contains comp operations
        while self.token == "LT, EQ":
            # Parse comp-op and append to children
            a = self.parse_compound_stmt()
            children.append(a)
            # Parse simple-stmt and append to children
            t = self.parse_simple_stmt()
            children.append(t)
        # Or else parse the simple-stmt and append to children
        t = self.parse_simple_stmt()
        children.append(t)
        
        # Return the childrens list.
        return PTNode("exp", children) 
       
     def parse_addop(self):     
        """ Function to parse tokens according to the following production:
            <addop> ::=   + | -
        """
        self.__scanner.log("Parsing <addop> ::=   + | -")
        r = PTNode("addop",  [], value = self.__scanner.current.value)
        
        if self.__scanner.current.kind in {"PLUS", "MINUS"}:
            self.__scanner.advance()
        return r
    
     def parse_repeat_stmt(self):     
        """ Function to parse tokens according to the following production:
            <repeatstmt > ::= repeat <stmtseq> until <exp>
        """
        self.__scanner.log("Parsing <repeatstmt > ::= repeat <stmtseq> until <exp>")
        
        # Parse statement sequence
        s = self.parse_statement_seq()
        children = [s]
        # if scanner matches repeat
        if self.__scanner.current.kind == "REPEAT":
            self.__scanner.match("REPEAT")
            # parse statementseq and append to chidren
            s2 = self.parse_statement_seq()
            children.append(s2)
            # if scanner matches until - parse exp & return the ptnode
            self.__scanner.match("UNTIL")
            s3 = self.parse_expression()
            children.append(s3)
        return PTNode("repeatstmt", children) 
    
     def parse_term(self):     
        """ A function to parse a term in tiny language using the following 
            declaration:
            <term> ::= <term> <mulop> <factor> | <factor>
        """
        self.__scanner.log("Parsing <term> ::= <term> <mulop> <factor> | <factor>")
        
        # Parse the factor
        t = self.parse_factor()
        children = [t]
        # while token contains mulop operations
        while self.token == "MUL, DIV":
            # Parse mulop and append to children
            m = self.parse_mulop()
            children.append(m)
            # Parse factor and append to children
            f = self.parse_factor
            children.append(f)
        # Or else parse the factor and append to children
        t = self.parse_factor()
        children.append(t)
        
        # Return the childrens list.
        return PTNode("term", children) 
    
     def parse_mulop(self):     
        """ Parse tokens matching following production:
            <mulop> -> * | /
        """
        self.__scanner.log("Parsing <mulop> -> * | /")
        r = PTNode("mulop",  [], value = self.__scanner.current.value)
        if self.__scanner.current.kind in {"TIMES", "OVER"}:
            self.__scanner.advance()
        return r
    
     def parse_factor(self):     
        """ Parse tokens matching following production:
            <factor> ::= ( <exp> ) | number | identifier
        """
        self.__scanner.log(
            "Parsing <factor> ::= ( <exp> ) | number | identifier")
    
        if self.__scanner.current.kind == "OPENBRACKET":
            self.__scanner.match("OPENBRACKET")
            c = self.parse_expression()
            self.__scanner.match("CLOSEBRACKET")
            return PTNode("factor", [c])
        elif self.__scanner.current.kind in {"ID", "INT"}:
            val = self.__scanner.current.value
            self.__scanner.advance()
            return PTNode("factor", [], val)
        else:
            self.__scanner.shriek("I'm lost . . .")
            
if __name__ == "__main__":

    fpath = "write.tny"
  
    parser = TinyParser(fpath)
    ptroot = parser.parse_program()

    print("Parse tree:")
    print("-" * 25)
    ptroot.dump()
    print("=" * 25)
    print()
    