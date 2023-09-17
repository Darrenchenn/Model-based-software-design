#Write down all the tool functions here.

#all pictures types
picType=0
picTypeIcon = 1
picTypeIllustration = 2
picTypeSocialMedia = 3





def matchType(x):
    return {
        'icon':picTypeIcon,
        'illustration':picTypeIllustration,
        'socialmedia':picTypeSocialMedia
    }.get(x,picType)


def parametersCheck():
    #todo:do some request check here
    return true