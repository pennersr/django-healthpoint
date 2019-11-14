from healthpoint.decorators import health_check


@health_check
def failure():
    return False, 'This check always fails'


@health_check
def success():
    return True, 'This check always succeeds'
