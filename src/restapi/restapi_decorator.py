def restapi(api):
    # noinspection PyBroadException
    def wrapper(*args, **kwargs):
        try:
            result = api(*args, **kwargs)
            return {
                "code": 200,
                "message": "调用成功！",
                "data": result
            }
        except Exception as ex:
            print(ex)
            return {
                "code": 400,
                "message": str(ex),
                "data": {}
            }
    wrapper.__name__ = api.__name__
    return wrapper
