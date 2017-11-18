class Survey:
    def __init__(self):
        self.indicators = {}
        return

    def __init__(self, names):
        self.indicators = {}
        for n in names:
            if n not in self.indicators:
                self.indicators[n] = {}

    def __init__(self, names, categories):
        # print(names)
        # print(categories)
        # print(len(names))
        # print(len(categories))

        self.indicators = {}
        for n in names:
            if n not in self.indicators:
                self.indicators[n] = {}

        for index, c in enumerate(categories):
            crt_indicator = names[index]
            crt_category = c
            self.indicators[crt_indicator][crt_category] = 0