"""
A module to encode with Caesar-style substitution ciphers.

Early (pre-20th century) encrypted messages letter substitution techniques.  To encrypt
a message like this:
    
    Attack at dawn!

you first removed all punctuation, spaces, and capitalization, like this:
    
    attackatdawn
    
The idea is that the reader can add all that information just inferring it from the text.

Now that the message only has letters, you then substitute each letter for another.  In 
Caesar's original cipher, each letter was shifted 3 positions, wrapping around at the end.  
So 'a' became 'd', 'b' become 'e',...,'w' became 'z', 'x' became 'a', 'y' became 'b' and 
'z' became 'c'. So this message becomes 
    
    dwwdfndwgdzq

To decrypt the message, you simply shift back in the reverse direction.  Or, you can just 
shift 26-3 = 23 spots and you will wrap back around to the original message.  Because of
this, rot-13 (shifting by 13 positions instead of 3) is another popular technique. 
Encoding a message with rot-13 twice gives you the original message.

This way of encoding messages is no longer used for secure communication, because it
is so easy to break.  But rot-13 can still be found on some Internet message boards
where people use it to hide movie spoilers and for other light-hearted topics.

Author: Orlando McEwan  
Date: 10/11/2022
"""
import introcs


def encode(text,n):
    """
    Returns the text encoded by shifting each letter by n positions.
    
    Letters at the end of the alphabet wrap back around.  So if n is 3, 'x' becomes 'a'.
    
    Examples:
        encode('attackatdawn',3) returns 'dwwdfndwgdzq'
        encode('dwwdfndwgdzq',23) returns 'attackatdawn'
        encode('attackatdawn',13) returns 'nggnpxngqnja'
        encode('',13) returns ''
    
    Parameter text: the text to encode
    Precondition: text is a string
    
    Parameter n: the number of positions to shift
    Precondition: n is an int between 0 and 25 (inclusive)
    """
    # Hint: Look at the Python functions ord and chr
    # Lower case letters have ord values 97 to 122
    
    if len(text) == 0:
        return text
    
    encoded_text = ''
    
    for char in text:
        ord_num = ord(char)
        
        new_ord = ord_num + n
        
        if new_ord > 122:
            new_ord = (new_ord - 122) + 96
        
        new_char = chr(new_ord)
        
        encoded_text += new_char
    
    return encoded_text
        
