class TwYearConverter():

    def from_tw_year(self, tw_year):
        if isinstance(tw_year, str):
            tw_year = eval(tw_year)
        self.tw_year = tw_year
        return self

    def to_tw_year(self):
        if self.year is not None:
            return self.year - 1911

    def from_year(self, year):
        if isinstance(year, str):
            year = eval(year)
        self.year = year
        return self

    def to_year(self):
        if self.tw_year is not None:
            return self.tw_year + 1911