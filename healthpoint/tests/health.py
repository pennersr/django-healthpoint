from healthpoint.decorators import health_check


@health_check
def failure():
    return False, 'This check always fails'
