"""
The functions for the course project.

Author: Orlando McEwan
Date: 08/27/2022
"""

import introcs

def matching_parens(s):
  """
  Returns True if the string s has a matching pair of parentheses.

  A matching pair of parentheses is an open parens '(' followed by a closing parens ')'.  
  Any thing can be between the two pair (including other parens).

  Example: matching_parens('A (B) C') returns True
  Example: matching_parens('A )B( C') returns False

  Parameter s: The string to check
  Precondition: s is a string (possibly empty)
  """
  
  assert type(s) == str, f'The value {s} is not a string!'

  openParen = introcs.find_str(s, '(')
  # print(openParen)
  
  closeParen = introcs.find_str(s[openParen:], ')')
  # print(closeParen)
  
  return openParen != -1 and closeParen != -1
  
def first_in_parens(s):
  """
  Returns: The substring of s that is inside the first pair of parentheses.

  The first pair of parenthesis consist of the first instance of character
  '(' and the first instance of ')' that follows it.

  Example: first_in_parens('A (B) C') returns 'B'
  Example: first_in_parens('A (B) (C)') returns 'B'
  Example: first_in_parens('A ((B) (C))') returns '(B'

  Parameter s: a string to check
  Precondition: s is a string with a matching pair of parens '()'.
  """
  assert type(s) == str, f'The value {s} is not a string!'
  assert ('(' in s ) and (')' in s[introcs.find_str(s, '('):]), f'The value {s} is not a valid string with matching pair of parens!'
  
  openParen = introcs.find_str(s, '(')
  # print(openParen)
  
  closeParen = introcs.find_str(s[openParen:], ')')
  # print(closeParen)
  
  return s[openParen + 1: closeParen + openParen]