class ReactionFiltersEnum:
    NON_SELECTIVE = "non_selective"
    SELECTIVE = "selective"
    DEFINED_SELECTIVE = "defined_selective"

    # try to find the internal value and return
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

    # prohibit any attempt to set any values
    def __setattr__(self, key, value):
        raise ValueError("No changes allowed.")
