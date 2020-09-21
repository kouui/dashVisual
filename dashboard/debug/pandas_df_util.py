import pandas as pd

df = pd.read_csv("./dashboard/data/gapminderDataFiveYear.csv")
default_country = 'Afghanistan'

def _get_sub_df(_key="country", _value=default_country, _sort_key="year", _as=True):

    _df1 = df[df[_key]==_value]
    if _sort_key is not None:
        _df1 = _df1.sort_values(by=_sort_key, ascending=_as)

    return _df1

def _get_countries():
    return list( df["country"].unique() )

def _get_years():
    return sorted( list( df["year"].unique() ) )

def _get_x_variables():
    return ["year", "pop", "lifeExp", "gdpPercap"]

def _get_y_variables():
    return ["gdpPercap", "pop", "lifeExp"]

def _get_pie_data(_year):
    _df1 = _get_sub_df(_key="year", _value=_year, _sort_key="gdpPercap", _as=False)
    _k = 30
    _labels = _df1["country"][:_k].tolist() + ["Others"]
    _values = _df1["gdpPercap"][:_k].tolist() +  [_df1["gdpPercap"][_k:].sum()]
    _values = [int(_v) for _v in _values]
    return _labels, _values




if __name__ == "__main__":
    # debug this script at dashVisual
    df1 = _get_sub_df()
    country_list = _get_countries()
    print(_get_pie_data(1962))
