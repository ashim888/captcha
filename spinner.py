import random

def spin(content):
    start = content.find('{')
    end = content.find('}')

    if start == -1 and end == -1:
        #none left
        return content
    elif start == -1:
        return content
    elif end == -1:
        raise "unbalanced brace"
    elif end < start:
        return content
    elif start < end:
        rest = spin(content[start+1:])
        end = rest.find('}')
        if end == -1:
            raise "unbalanced brace"
        return content[:start] + random.choice(rest[:end].split('|')) + spin(rest[end+1:])

def check_text(content):
    try:
        spin(content)
    except:
        print "There is an error in your spintax"
