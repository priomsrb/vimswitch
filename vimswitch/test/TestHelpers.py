def assertNoCall(mock, *args):
    calledWith = False
    try:
        mock.assert_any_call(*args)
        calledWith = True
    except AssertionError:
        pass

    if calledWith:
        raise AssertionError('Mock called with arguments', mock, args)


class Contains(str):
    def __eq__(self, other):
        return self in other
