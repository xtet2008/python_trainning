import traceback


try:
    response = func(self, *args, **kwargs)
except Exception, ex:
    print '-------------------------------------------------------'
    # print 'expression: ', Exception, '\n\n'
    # print 'str(exression): ', str(Exception), '\n\n'
    # print 'expression.message', Exception.message, '\n\n'
    print 'traceback.format_exc()，', traceback.format_exc(),
    # print 'ex，', ex, '\n\n'
    # print 'ex.message，', ex.message, '\n\n'
    print '-------------------------------------------------------'
    response = ex
finally:
    return response