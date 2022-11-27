# 
# Assignment one:
# Implementation of a scanner for TINY Language Parsing
# 
# Submitted By: Chloe Healy - 118720535.
# 
# Reference: Assignment one provided code files for project structure.
#
# 

import re
import sys
import traceback

# Define the tiny language comments.
COMMENTS = re.compile(r"#.*\n")

# Define tiny tokens.
TOKENS = re.compile(r"|[+-/*=<();>]"
                    r"|[0-9]"
                    r"|[a-z]"
                    r"|==|!=|<=|<|>=|>|="
                    )

# Tiny's list of reserved words.
RESERVED_NAMES = {
    "if" : "IF", "then" : "THEN", "else" : "ELSE", "end" : "END", 
    "repeat" : "REPEAT", "until" : "UNTIL", "read" : "READ",
    "write" : "WRITE", "EOS" : "EOS"
    }

# Tiny's list of special symbols.
SYMBOLS = {
    ";" : "SEMI", ":" : "COLON", "(" : "OPENBRACKET", 
    ")" : "CLOSEBRACKET", "=" : "ASSIGN","<=" : "LTE", 
    "<" : "LT",  ">" : "GT",  ">=" : "GTE", "==" : "EQ",  
    "!=" : "NOTEQ", "+" : "PLUS",  "-" : "MINUS", "*" : "MUL", 
    "/" : "DIV","" : "DIV", "STATEMENT" : "STATEMENT"
    }
# Used for testing
LOGPAD = " " * 10


class tinyToken:
    "Class for implementation of tiny token objects"
    def __init__(self, tkn):
        ''' string: string representation of the token
            value: numerical value'''
            
        self.string = tkn
        self.value = tkn
        
        # if the token is alphabetical   
        if tkn.isalpha():
            self.spelling = tkn
            # if it is in reserved names list
            if tkn in RESERVED_NAMES:
                self.kind = RESERVED_NAMES[tkn]
            else:
                self.kind = "ID"
                #self.value = tkn
        # If it is a numerical value
        elif tkn.isdigit():
            self.kind = "INT"
            self.value = int(tkn)
        elif tkn in SYMBOLS:
            self.kind = SYMBOLS[tkn]
        else:
            self.shriek("Illegal symbol '%s'." % tkn)
            
    def __str__(self):
        """ Return string representation of this token. """
        return ("[Token: '%s' (%s)]" 
               % (self.string, self.kind) )
        
class TinyScanner:
    """ Class implementation which performs a lexical analysis on a
        provided file which contains a tiny language source."""
    
    def __init__(self, fpath, verbose = False):
        """ Function which initialises the tiny scanner class and creates
            a scanner object.
            Parameters:
            self: initialisation of scanner object.
            fpath: pass the filepath to the file which contains the tiny
            language source.
        """
        
        # Open the provided file path if it exists.
        try:
            self.__source = open(fpath, "r").read()
        except Exception:
            traceback.print_exc()
            sys.exit(-1)
            
         # Set silent output.
        self.verbose = verbose
            
        # Eliminate comments.
        self.__source = COMMENTS.sub("", self.__source)
        
        # Set up token sequence.
        self.__tokens = TOKENS.findall(self.__source)
        self.__tokens.append("EOS")
        
        # Stage the first token.
        self.current = None
        self.advance()
        
    def has__next(self):
        """ A fuction which will find and return the next token 
            or if there is no next token it will return none."""
        if self.current != "EOS":
            tkn =  self.__tokens.pop(0)
            return tinyToken(tkn)
        else:
            return None
        
    def shriek(self, msg):
        """ A function which will print error message 'msg' and 
            terminate execution.
        """
        self.log("*** TinyScanner: %s" % msg, pad = False)
        sys.exit(-1)
     
    def log_nopad(self, msg):
        """ A fuction to print the 'msg' in the terminal. """
        # If output is set to silent.
        if self.verbose:
            print(msg)
        
    def log(self,  msg, pad = True):
        """A function to print 'msg', will Indent if 'pad' is set. """
        if self.verbose:
            print("%s%s" % (LOGPAD if pad else "", msg)) 
            
    def has_more(self):
        """ This function will return true if there are some tokens which 
        have been left unread.
        """
        return len(self.__tokens) > 0
  
    def advance(self):
        """ A function which moves the pointer one token forward.
        """
        if self.has_more:
            self.current = self.has__next()
            self.log_nopad("['%s']" % self.current.string)
            
    def match(self, expected):
        """ A fucntion which checks if the current token matches 
        'expected', then advance one token forward, otherwise issue 
        error and terminate.
        """
        # Get the current value.
        val = self.current.value
        # If the current value is not equal to the expected value
        if self.current.kind != expected:
            # output error message.
           self.shriek("Expected '%s', saw '%s'." 
                % (expected, self.current.string))
  
        # Move to the next token.
        self.advance() 
        return val