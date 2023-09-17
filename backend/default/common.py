#Write down all the tool functions here.

#all pictures types
PICTYPE=0
PICTYPEICON = 1
PICTYPEILLUSTRATION = 2
PICTYPESOCIALMEDIA = 3

#request class defination.




#some tool functions.
def matchType(x):
    return {
        'icon':PICTYPEICON,
        'illustration':PICTYPEILLUSTRATION,
        'socialmedia':PICTYPESOCIALMEDIA
    }.get(x,PICTYPE)


def parametersCheck():
    #todo:do some request check here
    return true