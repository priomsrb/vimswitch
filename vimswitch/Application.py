class Application:
    """
    A container for components that are used application-wide.

    Examples of how this class can be used:

      - Set a component
        `app.foo = myFoo`

      - Get (or create) a component:
        `foo = app.get('foo', Foo())`
        This will try to return `app.foo`. If that does not exist, then it will
        set `app.foo = Foo()` and return that instead.

      - Get an already created component
        `foo = app.foo`
        Use this when you are sure that app.foo has already been set
    """

    def get(self, attr, default):
        """
        Returns self.attr. If attr does not exist, then make self.attr = default
        and then return default.
        """
        if hasattr(self, attr):
            return getattr(self, attr)
        else:
            setattr(self, attr, default)
            return default
