from copy import deepcopy
import datetime as dt
from dateutil.relativedelta import relativedelta
from functools import reduce
from logging import warning
from math import ceil
from numpy import cov, cumprod, log, sqrt, square, zeros
from os import path
from pandas import (
    concat,
    DataFrame,
    date_range,
    DatetimeIndex,
    Int64Dtype,
    merge,
    MultiIndex,
    Series,
)
from pandas.tseries.offsets import CustomBusinessDay
from pathlib import Path
from plotly.graph_objs import Figure
from plotly.offline import plot
from random import choices
from scipy.stats import kurtosis, norm, skew
from statsmodels.api import OLS

# noinspection PyProtectedMember
from statsmodels.regression.linear_model import RegressionResults
from string import ascii_letters
from typing import List, Literal, TypeVar

from openseries.series import OpenTimeSeries
from openseries.datefixer import date_offset_foll, holiday_calendar
from openseries.load_plotly import load_plotly_dict
from openseries.risk import (
    drawdown_series,
    drawdown_details,
    cvar_down,
    var_down,
)

TOpenFrame = TypeVar("TOpenFrame", bound="OpenFrame")


class OpenFrame(object):
    constituents: List[OpenTimeSeries]
    tsdf: DataFrame
    weights: List[float]

    def __init__(
        self: TOpenFrame,
        constituents: List[OpenTimeSeries],
        weights: List[float] | None = None,
        sort: bool = True,
    ) -> None:
        """Instantiates an object of the class OpenFrame

        Parameters
        ----------
        constituents: List[OpenTimeSeries]
            List of objects of Class OpenTimeSeries
        weights: List[float], optional
            List of weights in float64 format.
        sort: bool, default: True
            argument in Pandas df.concat added to fix issue when upgrading
            Python & Pandas

        Returns
        -------
        OpenFrame
            Object of the class OpenFrame
        """
        self.weights = weights
        self.tsdf = DataFrame()
        self.constituents = constituents
        if constituents is not None and len(constituents) != 0:
            self.tsdf = reduce(
                lambda left, right: concat([left, right], axis="columns", sort=sort),
                [x.tsdf for x in self.constituents],
            )
        else:
            warning("OpenFrame() was passed an empty list.")

        if weights is not None:
            assert len(self.constituents) == len(
                self.weights
            ), "Number of TimeSeries must equal number of weights."

        if len(set(self.columns_lvl_zero)) != len(self.columns_lvl_zero):
            raise Exception("TimeSeries names/labels must be unique.")

    def __repr__(self: TOpenFrame) -> str:
        """
        Returns
        -------
        str
            A representation of an OpenFrame object
        """

        return "{}(constituents={}, weights={})".format(
            self.__class__.__name__, self.constituents, self.weights
        )

    def from_deepcopy(self: TOpenFrame) -> TOpenFrame:
        """Creates a copy of an OpenFrame object

        Returns
        -------
        OpenFrame
            An OpenFrame object
        """

        return deepcopy(self)

    def merge_series(
        self: TOpenFrame, how: Literal["outer", "inner"] = "outer"
    ) -> TOpenFrame:
        """Merges the Pandas Dataframes of the constituent OpenTimeSeries

        Parameters
        ----------
        how: Literal["outer", "inner"], default: "outer"
            The Pandas merge method.

        Returns
        -------
        OpenFrame
            An OpenFrame object
        """

        self.tsdf = reduce(
            lambda left, right: merge(
                left=left,
                right=right,
                how=how,
                left_index=True,
                right_index=True,
            ),
            [x.tsdf for x in self.constituents],
        )
        if self.tsdf.empty:
            raise Exception(
                f"Merging OpenTimeSeries DataFrames with "
                f"argument how={how} produced an empty DataFrame."
            )
        elif how == "inner":
            for x in self.constituents:
                x.tsdf = x.tsdf.loc[self.tsdf.index]
        return self

    def all_properties(self: TOpenFrame, properties: list | None = None) -> DataFrame:
        """Calculates the chosen timeseries properties

        Parameters
        ----------
        properties: list, optional
            The properties to calculate. Defaults to calculating all available.

        Returns
        -------
        pandas.DataFrame
            Properties of the contituent OpenTimeSeries
        """

        if not properties:
            properties = [
                "value_ret",
                "geo_ret",
                "arithmetic_ret",
                "vol",
                "downside_deviation",
                "ret_vol_ratio",
                "sortino_ratio",
                "z_score",
                "skew",
                "kurtosis",
                "positive_share",
                "var_down",
                "cvar_down",
                "vol_from_var",
                "worst",
                "worst_month",
                "max_drawdown",
                "max_drawdown_date",
                "max_drawdown_cal_year",
                "first_indices",
                "last_indices",
                "lengths_of_items",
                "span_of_days_all",
            ]
        prop_list = [getattr(self, x) for x in properties]
        results = concat(prop_list, axis="columns").T
        return results

    def calc_range(
        self: TOpenFrame,
        months_offset: int | None = None,
        from_dt: dt.date | None = None,
        to_dt: dt.date | None = None,
    ) -> (dt.date, dt.date):
        """Creates user defined date range

        Parameters
        ----------
        months_offset: int, optional
            Number of months offset as positive integer. Overrides use of from_date
            and to_date
        from_dt: datetime.date, optional
            Specific from date
        to_dt: datetime.date, optional
            Specific from date

        Returns
        -------
        (datetime.date, datetime.date)
            Start and end date of the chosen date range
        """
        earlier, later = None, None
        if months_offset is not None or from_dt is not None or to_dt is not None:
            if months_offset is not None:
                earlier = date_offset_foll(
                    raw_date=self.last_idx,
                    months_offset=-months_offset,
                    adjust=False,
                    following=True,
                )
                assert (
                    earlier >= self.first_idx
                ), "Function calc_range returned earlier date < series start"
                later = self.last_idx
            else:
                if from_dt is not None and to_dt is None:
                    assert (
                        from_dt >= self.first_idx
                    ), "Function calc_range returned earlier date < series start"
                    earlier, later = from_dt, self.last_idx
                elif from_dt is None and to_dt is not None:
                    assert (
                        to_dt <= self.last_idx
                    ), "Function calc_range returned later date > series end"
                    earlier, later = self.first_idx, to_dt
                elif from_dt is not None or to_dt is not None:
                    assert (
                        to_dt <= self.last_idx and from_dt >= self.first_idx
                    ), "Function calc_range returned dates outside series range"
                    earlier, later = from_dt, to_dt
            if earlier is not None:
                while not self.tsdf.index.isin([earlier]).any():
                    earlier -= dt.timedelta(days=1)
            if later is not None:
                while not self.tsdf.index.isin([later]).any():
                    later += dt.timedelta(days=1)
        else:
            earlier, later = self.first_idx, self.last_idx

        return earlier, later

    def align_index_to_local_cdays(
        self: TOpenFrame, countries: list | str = "SE"
    ) -> TOpenFrame:
        """Changes the index of the associated Pandas DataFrame .tsdf to align with
        local calendar business days

        Parameters
        ----------
        countries: list | str, default: "SE"
            (List of) country code(s) according to ISO 3166-1 alpha-2

        Returns
        -------
        OpenFrame
            An OpenFrame object
        """
        startyear = self.first_idx.year
        endyear = self.last_idx.year
        calendar = holiday_calendar(
            startyear=startyear, endyear=endyear, countries=countries
        )

        d_range = [
            d.date()
            for d in date_range(
                start=self.tsdf.first_valid_index(),
                end=self.tsdf.last_valid_index(),
                freq=CustomBusinessDay(calendar=calendar),
            )
        ]
        self.tsdf = self.tsdf.reindex(d_range, method=None, copy=False)
        return self

    @property
    def length(self: TOpenFrame) -> int:
        """
        Returns
        -------
        int
            Number of observations
        """

        return len(self.tsdf.index)

    @property
    def lengths_of_items(self: TOpenFrame) -> Series:
        """
        Returns
        -------
        Pandas.Series
            Number of observations of all constituents
        """

        return Series(
            data=[self.tsdf.loc[:, d].count() for d in self.tsdf],
            index=self.tsdf.columns,
            name="observations",
            dtype=Int64Dtype(),
        )

    @property
    def item_count(self: TOpenFrame) -> int:
        """
        Returns
        -------
        int
            Number of constituents
        """

        return len(self.constituents)

    @property
    def columns_lvl_zero(self: TOpenFrame) -> list:
        """
        Returns
        -------
        list
            Level 0 values of the Pandas.MultiIndex columns in the .tsdf
            Pandas.DataFrame
        """

        return self.tsdf.columns.get_level_values(0).tolist()

    @property
    def columns_lvl_one(self: TOpenFrame) -> list:
        """
        Returns
        -------
        list
            Level 1 values of the Pandas.MultiIndex columns in the .tsdf
            Pandas.DataFrame
        """

        return self.tsdf.columns.get_level_values(1).tolist()

    @property
    def first_idx(self: TOpenFrame) -> dt.date:
        """
        Returns
        -------
        datetime.date
            The first date in the index of the .tsdf Pandas.DataFrame
        """
        return self.tsdf.index[0]

    @property
    def first_indices(self: TOpenFrame) -> Series:
        """
        Returns
        -------
        Pandas.Series
            The first dates in the timeseries of all constituents
        """

        return Series(
            data=[i.first_idx for i in self.constituents],
            index=self.tsdf.columns,
            name="first indices",
        )

    @property
    def last_idx(self: TOpenFrame) -> dt.date:
        """
        Returns
        -------
        datetime.date
            The last date in the index of the .tsdf Pandas.DataFrame
        """
        return self.tsdf.index[-1]

    @property
    def last_indices(self: TOpenFrame) -> Series:
        """
        Returns
        -------
        Pandas.Series
            The last dates in the timeseries of all constituents
        """

        return Series(
            data=[i.last_idx for i in self.constituents],
            index=self.tsdf.columns,
            name="last indices",
        )

    @property
    def span_of_days(self: TOpenFrame) -> int:
        """
        Returns
        -------
        int
            Number of days from the first date to the last
            in the index of the .tsdf Pandas.DataFrame
        """

        return (self.last_idx - self.first_idx).days

    @property
    def span_of_days_all(self: TOpenFrame) -> Series:
        """
        Number of days from the first date to the last for all items in the frame.
        """
        return Series(
            data=[c.span_of_days for c in self.constituents],
            index=self.tsdf.columns,
            name="span of days",
            dtype=Int64Dtype(),
        )

    @property
    def yearfrac(self: TOpenFrame) -> float:
        """
        Returns
        -------
        float
            Length of the index of the .tsdf Pandas.DataFrame expressed in years
            assuming all years have 365.25 days
        """

        return self.span_of_days / 365.25

    @property
    def periods_in_a_year(self: TOpenFrame) -> float:
        """
        The number of businessdays in an average year for all days in the data.
        Be aware that this is not the same for all constituents.
        """
        return self.length / self.yearfrac

    @property
    def geo_ret(self: TOpenFrame) -> Series:
        """https://www.investopedia.com/terms/c/cagr.asp

        Returns
        -------
        Pandas.Series
            Compounded Annual Growth Rate (CAGR)
        """

        if self.tsdf.iloc[0].isin([0.0]).any() or self.tsdf.lt(0.0).any().any():
            raise Exception(
                "Geometric return cannot be calculated due to an "
                "initial value being zero or a negative value."
            )
        return Series(
            data=(self.tsdf.iloc[-1] / self.tsdf.iloc[0]) ** (1 / self.yearfrac) - 1,
            name="Geometric return",
            dtype="float64",
        )

    def geo_ret_func(
        self: TOpenFrame,
        months_from_last: int | None = None,
        from_date: dt.date | None = None,
        to_date: dt.date | None = None,
    ) -> Series:
        """https://www.investopedia.com/terms/c/cagr.asp

        Parameters
        ----------
        months_from_last : int, optional
            number of months offset as positive integer. Overrides use of from_date
            and to_date
        from_date : datetime.date, optional
            Specific from date
        to_date : datetime.date, optional
            Specific to date

        Returns
        -------
        Pandas.Series
            Compounded Annual Growth Rate (CAGR)
        """

        earlier, later = self.calc_range(months_from_last, from_date, to_date)

        if (
            self.tsdf.loc[earlier].isin([0.0]).any()
            or self.tsdf.loc[[earlier, later]].lt(0.0).any().any()
        ):
            raise Exception(
                "Geometric return cannot be calculated due to an "
                "initial value being zero or a negative value."
            )

        fraction = (later - earlier).days / 365.25

        return Series(
            data=(self.tsdf.loc[later] / self.tsdf.loc[earlier]) ** (1 / fraction) - 1,
            name="Subset Geometric return",
            dtype="float64",
        )

    @property
    def arithmetic_ret(self: TOpenFrame) -> Series:
        """https://www.investopedia.com/terms/a/arithmeticmean.asp

        Returns
        -------
        Pandas.Series
            Annualized arithmetic mean of returns
        """

        return Series(
            data=self.tsdf.pct_change().mean() * self.periods_in_a_year,
            name="Arithmetic return",
            dtype="float64",
        )

    def arithmetic_ret_func(
        self: TOpenFrame,
        months_from_last: int | None = None,
        from_date: dt.date | None = None,
        to_date: dt.date | None = None,
        periods_in_a_year_fixed: int | None = None,
    ) -> Series:
        """https://www.investopedia.com/terms/a/arithmeticmean.asp

        Parameters
        ----------
        months_from_last : int, optional
            number of months offset as positive integer. Overrides use of from_date
            and to_date
        from_date : datetime.date, optional
            Specific from date
        to_date : datetime.date, optional
            Specific to date
        periods_in_a_year_fixed : int, optional
            Allows locking the periods-in-a-year to simplify test cases and comparisons

        Returns
        -------
        Pandas.Series
            Annualized arithmetic mean of returns
        """

        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        if periods_in_a_year_fixed:
            time_factor = periods_in_a_year_fixed
        else:
            fraction = (later - earlier).days / 365.25
            how_many = int(
                self.tsdf.loc[earlier:later].count(numeric_only=True).iloc[0]
            )
            time_factor = how_many / fraction
        return Series(
            data=self.tsdf.loc[earlier:later].pct_change().mean() * time_factor,
            name="Subset Arithmetic return",
            dtype="float64",
        )

    @property
    def value_ret(self: TOpenFrame) -> Series:
        """
        Returns
        -------
        Pandas.Series
            Simple return
        """

        if self.tsdf.iloc[0].isin([0.0]).any():
            raise Exception(
                f"Error in function value_ret due to an initial value "
                f"being zero. ({self.tsdf.head(3)})"
            )
        else:
            return Series(
                data=self.tsdf.iloc[-1] / self.tsdf.iloc[0] - 1,
                name="Total return",
                dtype="float64",
            )

    def value_ret_func(
        self: TOpenFrame,
        months_from_last: int | None = None,
        from_date: dt.date | None = None,
        to_date: dt.date | None = None,
    ) -> Series:
        """
        Parameters
        ----------
        months_from_last : int, optional
            number of months offset as positive integer. Overrides use of from_date
            and to_date
        from_date : datetime.date, optional
            Specific from date
        to_date : datetime.date, optional
            Specific to date

        Returns
        -------
        Pandas.Series
            Simple return
        """

        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        if self.tsdf.iloc[0].isin([0.0]).any():
            raise Exception(
                f"Error in function value_ret due to an initial value "
                f"being zero. ({self.tsdf.head(3)})"
            )
        return Series(
            data=self.tsdf.loc[later] / self.tsdf.loc[earlier] - 1,
            name="Subset Total return",
            dtype="float64",
        )

    def value_ret_calendar_period(
        self: TOpenFrame, year: int, month: int | None = None
    ) -> Series:
        """
        Parameters
        ----------
        year : int
            Calendar year of the period to calculate.
        month : int, optional
            Calendar month of the period to calculate.

        Returns
        -------
        Pandas.Series
            Simple return for a specific calendar period
        """

        if month is None:
            period = str(year)
        else:
            period = "-".join([str(year), str(month).zfill(2)])
        vrdf = self.tsdf.copy()
        vrdf.index = DatetimeIndex(vrdf.index)
        rtn = vrdf.pct_change().copy()
        rtn = rtn.loc[period] + 1
        rtn = rtn.apply(cumprod, axis="index").iloc[-1] - 1
        rtn.name = period
        rtn = rtn.astype("float64")
        return rtn

    @property
    def vol(self: TOpenFrame) -> Series:
        """Based on Pandas .std() which is the equivalent of stdev.s([...])
        in MS Excel \n
        https://www.investopedia.com/terms/v/volatility.asp

        Returns
        -------
        Pandas.Series
            Annualized volatility
        """

        return Series(
            data=self.tsdf.pct_change().std() * sqrt(self.periods_in_a_year),
            name="Volatility",
            dtype="float64",
        )

    def vol_func(
        self: TOpenFrame,
        months_from_last: int | None = None,
        from_date: dt.date | None = None,
        to_date: dt.date | None = None,
        periods_in_a_year_fixed: int | None = None,
    ) -> Series:
        """Based on Pandas .std() which is the equivalent of stdev.s([...])
        in MS Excel \n
        https://www.investopedia.com/terms/v/volatility.asp

        Parameters
        ----------
        months_from_last : int, optional
            number of months offset as positive integer. Overrides use of from_date
            and to_date
        from_date : datetime.date, optional
            Specific from date
        to_date : datetime.date, optional
            Specific to date
        periods_in_a_year_fixed : int, optional
            Allows locking the periods-in-a-year to simplify test cases and comparisons

        Returns
        -------
        Pandas.Series
            Annualized volatility
        """

        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        if periods_in_a_year_fixed:
            time_factor = periods_in_a_year_fixed
        else:
            fraction = (later - earlier).days / 365.25
            how_many = int(
                self.tsdf.loc[earlier:later].count(numeric_only=True).iloc[0]
            )
            time_factor = how_many / fraction
        return Series(
            data=self.tsdf.loc[earlier:later].pct_change().std() * sqrt(time_factor),
            name="Subset Volatility",
            dtype="float64",
        )

    @property
    def downside_deviation(self: TOpenFrame) -> Series:
        """The standard deviation of returns that are below a Minimum Accepted
        Return of zero.
        It is used to calculate the Sortino Ratio \n
        https://www.investopedia.com/terms/d/downside-deviation.asp

        Returns
        -------
        Pandas.Series
            Downside deviation
        """

        dddf = self.tsdf.pct_change()

        return Series(
            data=sqrt((dddf[dddf < 0.0] ** 2).sum() / self.length)
            * sqrt(self.periods_in_a_year),
            name="Downside deviation",
            dtype="float64",
        )

    def downside_deviation_func(
        self: TOpenFrame,
        min_accepted_return: float = 0.0,
        months_from_last: int | None = None,
        from_date: dt.date | None = None,
        to_date: dt.date | None = None,
        periods_in_a_year_fixed: int | None = None,
    ) -> Series:
        """The standard deviation of returns that are below a Minimum Accepted
        Return of zero.
        It is used to calculate the Sortino Ratio \n
        https://www.investopedia.com/terms/d/downside-deviation.asp

        Parameters
        ----------
        min_accepted_return : float, optional
            The annualized Minimum Accepted Return (MAR)
        months_from_last : int, optional
            number of months offset as positive integer. Overrides use of from_date
            and to_date
        from_date : datetime.date, optional
            Specific from date
        to_date : datetime.date, optional
            Specific to date
        periods_in_a_year_fixed : int, optional
            Allows locking the periods-in-a-year to simplify test cases and
            comparisons

        Returns
        -------
        Pandas.Series
            Downside deviation
        """

        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        how_many = self.tsdf.loc[earlier:later].pct_change().count(numeric_only=True)
        if periods_in_a_year_fixed:
            time_factor = periods_in_a_year_fixed
        else:
            fraction = (later - earlier).days / 365.25
            time_factor = how_many / fraction

        dddf = (
            self.tsdf.loc[earlier:later]
            .pct_change()
            .sub(min_accepted_return / time_factor)
        )

        return Series(
            data=sqrt((dddf[dddf < 0.0] ** 2).sum() / how_many) * sqrt(time_factor),
            name="Subset Downside deviation",
            dtype="float64",
        )

    @property
    def ret_vol_ratio(self: TOpenFrame) -> Series:
        """
        Returns
        -------
        Pandas.Series
            Ratio of the annualized arithmetic mean of returns and annualized
            volatility.
        """

        ratio = self.arithmetic_ret / self.vol
        ratio.name = "Return vol ratio"
        ratio = ratio.astype("float64")
        return ratio

    def ret_vol_ratio_func(
        self: TOpenFrame,
        riskfree_rate: float | None = None,
        riskfree_column: tuple | int = -1,
        months_from_last: int | None = None,
        from_date: dt.date | None = None,
        to_date: dt.date | None = None,
        periods_in_a_year_fixed: int | None = None,
    ) -> Series:
        """The ratio of annualized arithmetic mean of returns and annualized
        volatility or, if riskfree return provided, Sharpe ratio calculated
        as ( geometric return - risk-free return ) / volatility. The latter ratio
        implies that the riskfree asset has zero volatility. \n
        https://www.investopedia.com/terms/s/sharperatio.asp

        Parameters
        ----------
        riskfree_rate : float, optional
            The return of the zero volatility asset used to calculate Sharpe ratio
        riskfree_column : int | None, default: -1
            The return of the zero volatility asset used to calculate Sharpe ratio
        months_from_last : int, optional
            number of months offset as positive integer. Overrides use of from_date
            and to_date
        from_date : datetime.date, optional
            Specific from date
        to_date : datetime.date, optional
            Specific to date
        periods_in_a_year_fixed : int, optional
            Allows locking the periods-in-a-year to simplify test cases and
            comparisons

        Returns
        -------
        Pandas.Series
            Ratio of the annualized arithmetic mean of returns and annualized
            volatility or,
            if risk-free return provided, Sharpe ratio
        """

        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        how_many = self.tsdf.loc[earlier:later].iloc[:, 0].count()
        fraction = (later - earlier).days / 365.25

        if periods_in_a_year_fixed:
            time_factor = periods_in_a_year_fixed
        else:
            time_factor = how_many / fraction

        ratios = []
        if riskfree_rate is None:
            if isinstance(riskfree_column, tuple):
                riskfree = self.tsdf.loc[earlier:later].loc[:, riskfree_column]
                riskfree_item = riskfree_column
                riskfree_label = self.tsdf.loc[:, riskfree_column].name[0]
            elif isinstance(riskfree_column, int):
                riskfree = self.tsdf.loc[earlier:later].iloc[:, riskfree_column]
                riskfree_item = self.tsdf.iloc[:, riskfree_column].name
                riskfree_label = self.tsdf.iloc[:, riskfree_column].name[0]
            else:
                raise Exception("base_column should be a tuple or an integer.")

            for item in self.tsdf:
                if item == riskfree_item:
                    ratios.append(0.0)
                else:
                    longdf = self.tsdf.loc[earlier:later].loc[:, item]
                    ret = float(longdf.pct_change().mean() * time_factor)
                    riskfree_ret = float(riskfree.pct_change().mean() * time_factor)
                    vol = float(longdf.pct_change().std() * sqrt(time_factor))
                    ratios.append((ret - riskfree_ret) / vol)

            return Series(
                data=ratios,
                index=self.tsdf.columns,
                name=f"Sharpe Ratios vs {riskfree_label}",
                dtype="float64",
            )
        else:
            for item in self.tsdf:
                longdf = self.tsdf.loc[earlier:later].loc[:, item]
                ret = float(longdf.pct_change().mean() * time_factor)
                vol = float(longdf.pct_change().std() * sqrt(time_factor))
                ratios.append((ret - riskfree_rate) / vol)

            return Series(
                data=ratios,
                index=self.tsdf.columns,
                name=f"Sharpe Ratios (rf={riskfree_rate:.2%})",
                dtype="float64",
            )

    def jensen_alpha(
        self: TOpenFrame,
        asset: tuple | int,
        market: tuple | int,
        riskfree_rate: float = 0.0,
    ) -> float:
        """The Jensen's measure, or Jensen's alpha, is a risk-adjusted performance
        measure that represents the average return on a portfolio or investment,
        above or below that predicted by the capital asset pricing model (CAPM),
        given the portfolio's or investment's beta and the average market return.
        This metric is also commonly referred to as simply alpha.
        https://www.investopedia.com/terms/j/jensensmeasure.asp

        Parameters
        ----------
        asset: tuple | int
            The column of the asset
        market: tuple | int
            The column of the market against which Jensen's alpha is measured
        riskfree_rate : float, default: 0.0
            The return of the zero volatility riskfree asset

        Returns
        -------
        float
            Jensen's alpha
        """
        if all(
            [
                True if x == "Return(Total)" else False
                for x in self.tsdf.columns.get_level_values(1).values
            ]
        ):
            if isinstance(asset, tuple):
                asset_log = self.tsdf.loc[:, asset]
                asset_cagr = asset_log.mean()
            elif isinstance(asset, int):
                asset_log = self.tsdf.iloc[:, asset]
                asset_cagr = asset_log.mean()
            else:
                raise Exception("asset should be a tuple or an integer.")
            if isinstance(market, tuple):
                market_log = self.tsdf.loc[:, market]
                market_cagr = market_log.mean()
            elif isinstance(market, int):
                market_log = self.tsdf.iloc[:, market]
                market_cagr = market_log.mean()
            else:
                raise Exception("market should be a tuple or an integer.")
        else:
            if isinstance(asset, tuple):
                asset_log = log(
                    self.tsdf.loc[:, asset] / self.tsdf.loc[:, asset].iloc[0]
                )
                if self.yearfrac > 1.0:
                    asset_cagr = (
                        self.tsdf.loc[:, asset].iloc[-1]
                        / self.tsdf.loc[:, asset].iloc[0]
                    ) ** (1 / self.yearfrac) - 1
                else:
                    asset_cagr = (
                        self.tsdf.loc[:, asset].iloc[-1]
                        / self.tsdf.loc[:, asset].iloc[0]
                        - 1
                    )
            elif isinstance(asset, int):
                asset_log = log(self.tsdf.iloc[:, asset] / self.tsdf.iloc[0, asset])
                if self.yearfrac > 1.0:
                    asset_cagr = (
                        self.tsdf.iloc[-1, asset] / self.tsdf.iloc[0, asset]
                    ) ** (1 / self.yearfrac) - 1
                else:
                    asset_cagr = (
                        self.tsdf.iloc[-1, asset] / self.tsdf.iloc[0, asset] - 1
                    )
            else:
                raise Exception("asset should be a tuple or an integer.")
            if isinstance(market, tuple):
                market_log = log(
                    self.tsdf.loc[:, market] / self.tsdf.loc[:, market].iloc[0]
                )
                if self.yearfrac > 1.0:
                    market_cagr = (
                        self.tsdf.loc[:, market].iloc[-1]
                        / self.tsdf.loc[:, market].iloc[0]
                    ) ** (1 / self.yearfrac) - 1
                else:
                    market_cagr = (
                        self.tsdf.loc[:, market].iloc[-1]
                        / self.tsdf.loc[:, market].iloc[0]
                        - 1
                    )
            elif isinstance(market, int):
                market_log = log(self.tsdf.iloc[:, market] / self.tsdf.iloc[0, market])
                if self.yearfrac > 1.0:
                    market_cagr = (
                        self.tsdf.iloc[-1, market] / self.tsdf.iloc[0, market]
                    ) ** (1 / self.yearfrac) - 1
                else:
                    market_cagr = (
                        self.tsdf.iloc[-1, market] / self.tsdf.iloc[0, market] - 1
                    )
            else:
                raise Exception("market should be a tuple or an integer.")

        covariance = cov(asset_log, market_log, ddof=1)
        beta = covariance[0, 1] / covariance[1, 1]

        return float(asset_cagr - riskfree_rate - beta * (market_cagr - riskfree_rate))

    @property
    def sortino_ratio(self: TOpenFrame) -> Series:
        """https://www.investopedia.com/terms/s/sortinoratio.asp

        Returns
        -------
        Pandas.Series
            Sortino ratio calculated as the annualized arithmetic mean of returns
            / downside deviation. The ratio implies that the riskfree asset has zero
            volatility, and a minimum acceptable return of zero.
        """

        sortino = self.arithmetic_ret / self.downside_deviation
        sortino.name = "Sortino ratio"
        sortino = sortino.astype("float64")
        return sortino

    def sortino_ratio_func(
        self: TOpenFrame,
        riskfree_rate: float | None = None,
        riskfree_column: tuple | int = -1,
        months_from_last: int | None = None,
        from_date: dt.date | None = None,
        to_date: dt.date | None = None,
        periods_in_a_year_fixed: int | None = None,
    ) -> Series:
        """The Sortino ratio calculated as ( return - risk free return )
        / downside deviation. The ratio implies that the riskfree asset has zero
        volatility, and a minimum acceptable return of zero. The ratio is
        calculated using the annualized arithmetic mean of returns. \n
        https://www.investopedia.com/terms/s/sortinoratio.asp

        Parameters
        ----------
        riskfree_rate : float, optional
            The return of the zero volatility asset
        riskfree_column : int | None, default: -1
            The return of the zero volatility asset used to calculate Sharpe ratio
        months_from_last : int, optional
            number of months offset as positive integer. Overrides use of from_date
            and to_date
        from_date : datetime.date, optional
            Specific from date
        to_date : datetime.date, optional
            Specific to date
        periods_in_a_year_fixed : int, optional
            Allows locking the periods-in-a-year to simplify test cases and
            comparisons

        Returns
        -------
        Pandas.Series
            Sortino ratio calculated as ( return - riskfree return ) /
            downside deviation
        """

        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        how_many = self.tsdf.loc[earlier:later].iloc[:, 0].count()
        fraction = (later - earlier).days / 365.25

        if periods_in_a_year_fixed:
            time_factor = periods_in_a_year_fixed
        else:
            time_factor = how_many / fraction

        ratios = []
        if riskfree_rate is None:
            if isinstance(riskfree_column, tuple):
                riskfree = self.tsdf.loc[earlier:later].loc[:, riskfree_column]
                riskfree_item = riskfree_column
                riskfree_label = self.tsdf.loc[:, riskfree_column].name[0]
            elif isinstance(riskfree_column, int):
                riskfree = self.tsdf.loc[earlier:later].iloc[:, riskfree_column]
                riskfree_item = self.tsdf.iloc[:, riskfree_column].name
                riskfree_label = self.tsdf.iloc[:, riskfree_column].name[0]
            else:
                raise Exception("base_column should be a tuple or an integer.")

            for item in self.tsdf:
                if item == riskfree_item:
                    ratios.append(0.0)
                else:
                    longdf = self.tsdf.loc[earlier:later].loc[:, item]
                    ret = float(longdf.pct_change().mean() * time_factor)
                    riskfree_ret = float(riskfree.pct_change().mean() * time_factor)
                    dddf = longdf.pct_change()
                    downdev = float(
                        sqrt((dddf[dddf.values < 0.0].values ** 2).sum() / how_many)
                        * sqrt(time_factor)
                    )
                    ratios.append((ret - riskfree_ret) / downdev)

            return Series(
                data=ratios,
                index=self.tsdf.columns,
                name=f"Sortino Ratios vs {riskfree_label}",
                dtype="float64",
            )
        else:
            for item in self.tsdf:
                longdf = self.tsdf.loc[earlier:later].loc[:, item]
                ret = float(longdf.pct_change().mean() * time_factor)
                dddf = longdf.pct_change()
                downdev = float(
                    sqrt((dddf[dddf.values < 0.0].values ** 2).sum() / how_many)
                    * sqrt(time_factor)
                )
                ratios.append((ret - riskfree_rate) / downdev)

            return Series(
                data=ratios,
                index=self.tsdf.columns,
                name=f"Sortino Ratios (rf={riskfree_rate:.2%},mar=0.0%)",
                dtype="float64",
            )

    @property
    def z_score(self: TOpenFrame) -> Series:
        """https://www.investopedia.com/terms/z/zscore.asp

        Returns
        -------
        float
            Z-score as (last return - mean return) / standard deviation of returns.
        """

        zd = self.tsdf.pct_change()
        return Series(
            data=(zd.iloc[-1] - zd.mean()) / zd.std(),
            name="Z-score",
            dtype="float64",
        )

    def z_score_func(
        self: TOpenFrame,
        months_from_last: int | None = None,
        from_date: dt.date | None = None,
        to_date: dt.date | None = None,
    ) -> Series:
        """https://www.investopedia.com/terms/z/zscore.asp

        Parameters
        ----------
        months_from_last : int, optional
            number of months offset as positive integer. Overrides use of from_date
            and to_date
        from_date : datetime.date, optional
            Specific from date
        to_date : datetime.date, optional
            Specific to date

        Returns
        -------
        Pandas.Series
            Z-score as (last return - mean return) / standard deviation of returns
        """

        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        zd = self.tsdf.loc[earlier:later].pct_change()
        return Series(
            data=(zd.iloc[-1] - zd.mean()) / zd.std(),
            name="Subset Z-score",
            dtype="float64",
        )

    @property
    def max_drawdown(self: TOpenFrame) -> Series:
        """https://www.investopedia.com/terms/m/maximum-drawdown-mdd.asp

        Returns
        -------
        Pandas.Series
            Maximum drawdown without any limit on date range
        """

        return Series(
            data=(self.tsdf / self.tsdf.expanding(min_periods=1).max()).min() - 1,
            name="Max drawdown",
            dtype="float64",
        )

    @property
    def max_drawdown_date(self: TOpenFrame) -> Series:
        """https://www.investopedia.com/terms/m/maximum-drawdown-mdd.asp

        Returns
        -------
        Pandas.Series
            Date when the maximum drawdown occurred
        """

        md_dates = [c.max_drawdown_date for c in self.constituents]
        return Series(
            data=md_dates,
            index=self.tsdf.columns,
            name="Max drawdown dates",
        )

    def max_drawdown_func(
        self: TOpenFrame,
        months_from_last: int | None = None,
        from_date: dt.date | None = None,
        to_date: dt.date | None = None,
    ) -> Series:
        """https://www.investopedia.com/terms/m/maximum-drawdown-mdd.asp

        Parameters
        ----------
        months_from_last : int, optional
            number of months offset as positive integer. Overrides use of from_date
            and to_date
        from_date : datetime.date, optional
            Specific from date
        to_date : datetime.date, optional
            Specific to date

        Returns
        -------
        Pandas.Series
            Maximum drawdown without any limit on date range
        """

        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        return Series(
            data=(
                self.tsdf.loc[earlier:later]
                / self.tsdf.loc[earlier:later].expanding(min_periods=1).max()
            ).min()
            - 1,
            name="Subset Max drawdown",
            dtype="float64",
        )

    @property
    def max_drawdown_cal_year(self: TOpenFrame) -> Series:
        """https://www.investopedia.com/terms/m/maximum-drawdown-mdd.asp

        Returns
        -------
        Pandas.Series
            Maximum drawdown in a single calendar year.
        """

        md = (
            self.tsdf.groupby([DatetimeIndex(self.tsdf.index).year])
            .apply(
                lambda prices: (prices / prices.expanding(min_periods=1).max()).min()
                - 1
            )
            .min()
        )
        md.name = "Max drawdown in cal yr"
        md = md.astype("float64")
        return md

    @property
    def worst(self: TOpenFrame) -> Series:
        """
        Returns
        -------
        Pandas.Series
            Most negative percentage change
        """

        return Series(data=self.tsdf.pct_change().min(), name="Worst", dtype="float64")

    @property
    def worst_month(self: TOpenFrame) -> Series:
        """
        Returns
        -------
        Pandas.Series
            Most negative month
        """

        wdf = self.tsdf.copy()
        wdf.index = DatetimeIndex(wdf.index)
        return Series(
            data=wdf.resample("BM").last().pct_change().min(),
            name="Worst month",
            dtype="float64",
        )

    def worst_func(
        self: TOpenFrame,
        observations: int = 1,
        months_from_last: int | None = None,
        from_date: dt.date | None = None,
        to_date: dt.date | None = None,
    ) -> Series:
        """
        Parameters
        ----------
        observations: int, default: 1
        months_from_last : int, optional
            number of months offset as positive integer. Overrides use of from_date
            and to_date
        from_date : datetime.date, optional
            Specific from date
        to_date : datetime.date, optional
            Specific to date

        Returns
        -------
        Pandas.Series
            Most negative percentage change over a rolling number of observations
            within a chosen date range
        """

        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        return Series(
            data=self.tsdf.loc[earlier:later]
            .pct_change()
            .rolling(observations, min_periods=observations)
            .sum()
            .min(),
            name=f"Subset Worst {observations}day period",
            dtype="float64",
        )

    @property
    def positive_share(self: TOpenFrame) -> Series:
        """
        Returns
        -------
        Pandas.Series
            The share of percentage changes that are greater than zero
        """
        pos = self.tsdf.pct_change()[1:][self.tsdf.pct_change()[1:] > 0.0].count()
        tot = self.tsdf.pct_change()[1:].count()
        answer = pos / tot
        answer.name = "Positive share"
        answer = answer.astype("float64")
        return answer

    def positive_share_func(
        self: TOpenFrame,
        months_from_last: int | None = None,
        from_date: dt.date | None = None,
        to_date: dt.date | None = None,
    ) -> Series:
        """
        Parameters
        ----------
        months_from_last : int, optional
            number of months offset as positive integer. Overrides use of from_date
            and to_date
        from_date : datetime.date, optional
            Specific from date
        to_date : datetime.date, optional
            Specific to date

        Returns
        -------
        Pandas.Series
            The share of percentage changes that are greater than zero
        """

        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        pos = (
            self.tsdf.loc[earlier:later]
            .pct_change()[1:][self.tsdf.loc[earlier:later].pct_change()[1:] > 0.0]
            .count()
        )
        tot = self.tsdf.loc[earlier:later].pct_change()[1:].count()
        answer = pos / tot
        answer.name = "Positive share"
        answer = answer.astype("float64")
        return answer

    @property
    def skew(self: TOpenFrame) -> Series:
        """https://www.investopedia.com/terms/s/skewness.asp

        Returns
        -------
        Pandas.Series
            Skew of the return distribution
        """

        return Series(
            data=skew(self.tsdf.pct_change().values, bias=True, nan_policy="omit"),
            index=self.tsdf.columns,
            name="Skew",
            dtype="float64",
        )

    def skew_func(
        self: TOpenFrame,
        months_from_last: int | None = None,
        from_date: dt.date | None = None,
        to_date: dt.date | None = None,
    ) -> Series:
        """https://www.investopedia.com/terms/s/skewness.asp

        Parameters
        ----------
        months_from_last : int, optional
            number of months offset as positive integer. Overrides use of from_date
            and to_date
        from_date : datetime.date, optional
            Specific from date
        to_date : datetime.date, optional
            Specific to date

        Returns
        -------
        Pandas.Series
            Skew of the return distribution
        """

        earlier, later = self.calc_range(months_from_last, from_date, to_date)

        return Series(
            data=skew(
                a=self.tsdf.loc[earlier:later].pct_change(),
                bias=True,
                nan_policy="omit",
            ),
            index=self.tsdf.columns,
            name="Subset Skew",
            dtype="float64",
        )

    @property
    def kurtosis(self: TOpenFrame) -> Series:
        """https://www.investopedia.com/terms/k/kurtosis.asp

        Returns
        -------
        Pandas.Series
            Kurtosis of the return distribution
        """

        return Series(
            data=kurtosis(
                self.tsdf.pct_change(), fisher=True, bias=True, nan_policy="omit"
            ),
            index=self.tsdf.columns,
            name="Kurtosis",
            dtype="float64",
        )

    def kurtosis_func(
        self: TOpenFrame,
        months_from_last: int | None = None,
        from_date: dt.date | None = None,
        to_date: dt.date | None = None,
    ) -> Series:
        """https://www.investopedia.com/terms/k/kurtosis.asp

        Parameters
        ----------
        months_from_last : int, optional
            number of months offset as positive integer. Overrides use of from_date
            and to_date
        from_date : datetime.date, optional
            Specific from date
        to_date : datetime.date, optional
            Specific to date

        Returns
        -------
        Pandas.Series
            Kurtosis of the return distribution
        """

        earlier, later = self.calc_range(months_from_last, from_date, to_date)

        return Series(
            data=kurtosis(
                self.tsdf.loc[earlier:later].pct_change(),
                fisher=True,
                bias=True,
                nan_policy="omit",
            ),
            index=self.tsdf.columns,
            name="Subset Kurtosis",
            dtype="float64",
        )

    @property
    def cvar_down(self: TOpenFrame, level: float = 0.95) -> Series:
        """https://www.investopedia.com/terms/c/conditional_value_at_risk.asp

        Parameters
        ----------
        level: float, default: 0.95
            The sought CVaR level

        Returns
        -------
        Pandas.Series
            Downside Conditional Value At Risk "CVaR"
        """

        cvar_df = self.tsdf.copy(deep=True)
        var_list = [
            cvar_df.loc[:, x]
            .pct_change()
            .sort_values()
            .iloc[: int(ceil((1 - level) * cvar_df.loc[:, x].pct_change().count()))]
            .mean()
            for x in self.tsdf
        ]
        return Series(
            data=var_list,
            index=self.tsdf.columns,
            name=f"CVaR {level:.1%}",
            dtype="float64",
        )

    def cvar_down_func(
        self: TOpenFrame,
        level: float = 0.95,
        months_from_last: int | None = None,
        from_date: dt.date | None = None,
        to_date: dt.date | None = None,
    ) -> Series:
        """https://www.investopedia.com/terms/c/conditional_value_at_risk.asp

        Parameters
        ----------
        level: float, default: 0.95
            The sought CVaR level
        months_from_last : int, optional
            number of months offset as positive integer. Overrides use of from_date
            and to_date
        from_date : datetime.date, optional
            Specific from date
        to_date : datetime.date, optional
            Specific to date

        Returns
        -------
        Pandas.Series
            Downside Conditional Value At Risk "CVaR"
        """

        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        cvar_df = self.tsdf.loc[earlier:later].copy(deep=True)
        var_list = [
            cvar_df.loc[:, x]
            .pct_change()
            .sort_values()
            .iloc[: int(ceil((1 - level) * cvar_df.loc[:, x].pct_change().count()))]
            .mean()
            for x in self.tsdf
        ]
        return Series(
            data=var_list,
            index=self.tsdf.columns,
            name=f"CVaR {level:.1%}",
            dtype="float64",
        )

    @property
    def var_down(
        self: TOpenFrame,
        level: float = 0.95,
        interpolation: Literal[
            "linear", "lower", "higher", "midpoint", "nearest"
        ] = "lower",
    ) -> Series:
        """Downside Value At Risk, "VaR". The equivalent of
        percentile.inc([...], 1-level) over returns in MS Excel \n
        https://www.investopedia.com/terms/v/var.asp

        Parameters
        ----------

        level: float, default: 0.95
            The sought VaR level
        interpolation: Literal["linear", "lower", "higher", "midpoint",
        "nearest"], default: "lower"
            type of interpolation in Pandas.DataFrame.quantile() function.

        Returns
        -------
        Pandas.Series
            Downside Value At Risk
        """

        return Series(
            data=self.tsdf.pct_change().quantile(
                1 - level, interpolation=interpolation
            ),
            name=f"VaR {level:.1%}",
            dtype="float64",
        )

    def var_down_func(
        self: TOpenFrame,
        level: float = 0.95,
        months_from_last: int | None = None,
        from_date: dt.date | None = None,
        to_date: dt.date | None = None,
        interpolation: Literal[
            "linear", "lower", "higher", "midpoint", "nearest"
        ] = "lower",
    ) -> Series:
        """https://www.investopedia.com/terms/v/var.asp
        Downside Value At Risk, "VaR". The equivalent of
        percentile.inc([...], 1-level) over returns in MS Excel.

        Parameters
        ----------

        level: float, default: 0.95
            The sought VaR level
        months_from_last : int, optional
            number of months offset as positive integer. Overrides use of from_date
            and to_date
        from_date : datetime.date, optional
            Specific from date
        to_date : datetime.date, optional
            Specific to date
        interpolation: Literal["linear", "lower", "higher", "midpoint",
        "nearest"], default: "lower"
            Type of interpolation in Pandas.DataFrame.quantile() function.

        Returns
        -------
        Pandas.Series
            Downside Value At Risk
        """

        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        return Series(
            data=self.tsdf.loc[earlier:later]
            .pct_change()
            .quantile(1 - level, interpolation=interpolation),
            name=f"VaR {level:.1%}",
            dtype="float64",
        )

    @property
    def vol_from_var(
        self: TOpenFrame,
        level: float = 0.95,
        interpolation: Literal[
            "linear", "lower", "higher", "midpoint", "nearest"
        ] = "lower",
    ) -> Series:
        """
        Parameters
        ----------

        level: float, default: 0.95
            The sought VaR level
        interpolation: Literal["linear", "lower", "higher", "midpoint",
        "nearest"], default: "lower"
            type of interpolation in Pandas.DataFrame.quantile() function.

        Returns
        -------
        Pandas.Series
            Implied annualized volatility from the Downside VaR using the
            assumption that returns are normally distributed.
        """

        imp_vol = (
            -sqrt(self.periods_in_a_year)
            * self.var_down_func(interpolation=interpolation)
            / norm.ppf(level)
        )
        return Series(
            data=imp_vol, name=f"Imp vol from VaR {level:.0%}", dtype="float64"
        )

    def vol_from_var_func(
        self: TOpenFrame,
        level: float = 0.95,
        months_from_last: int | None = None,
        from_date: dt.date | None = None,
        to_date: dt.date | None = None,
        interpolation: Literal[
            "linear", "lower", "higher", "midpoint", "nearest"
        ] = "lower",
        drift_adjust: bool = False,
        periods_in_a_year_fixed: int | None = None,
    ) -> Series:
        """
        Parameters
        ----------

        level: float, default: 0.95
            The sought VaR level
        months_from_last : int, optional
            number of months offset as positive integer. Overrides use of from_date
            and to_date
        from_date : datetime.date, optional
            Specific from date
        to_date : datetime.date, optional
            Specific to date
        interpolation: Literal["linear", "lower", "higher", "midpoint",
        "nearest"], default: "lower"
            type of interpolation in Pandas.DataFrame.quantile() function.
        drift_adjust: bool, default: False
            An adjustment to remove the bias implied by the average return
        periods_in_a_year_fixed : int, optional
            Allows locking the periods-in-a-year to simplify test cases and
            comparisons

        Returns
        -------
        Pandas.Series
            Implied annualized volatility from the Downside VaR using the
            assumption that returns are normally distributed.
        """

        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        if periods_in_a_year_fixed:
            time_factor = periods_in_a_year_fixed
        else:
            fraction = (later - earlier).days / 365.25
            how_many = int(
                self.tsdf.loc[earlier:later].count(numeric_only=True).iloc[0]
            )
            time_factor = how_many / fraction
        if drift_adjust:
            imp_vol = (-sqrt(time_factor) / norm.ppf(level)) * (
                self.tsdf.loc[earlier:later]
                .pct_change()
                .quantile(1 - level, interpolation=interpolation)
                - self.tsdf.loc[earlier:later].pct_change().sum()
                / len(self.tsdf.loc[earlier:later].pct_change())
            )
        else:
            imp_vol = (
                -sqrt(time_factor)
                * self.tsdf.loc[earlier:later]
                .pct_change()
                .quantile(1 - level, interpolation=interpolation)
                / norm.ppf(level)
            )
        return Series(
            data=imp_vol, name=f"Subset Imp vol from VaR {level:.0%}", dtype="float64"
        )

    def target_weight_from_var(
        self: TOpenFrame,
        target_vol: float = 0.175,
        min_leverage_local: float = 0.0,
        max_leverage_local: float = 99999.0,
        level: float = 0.95,
        months_from_last: int | None = None,
        from_date: dt.date | None = None,
        to_date: dt.date | None = None,
        interpolation: Literal[
            "linear", "lower", "higher", "midpoint", "nearest"
        ] = "lower",
        drift_adjust: bool = False,
        periods_in_a_year_fixed: int | None = None,
    ) -> Series:
        """A position weight multiplier from the ratio between a VaR implied
        volatility and a given target volatility. Multiplier = 1.0 -> target met

        Parameters
        ----------
        target_vol: float, default: 0.175
            Target Volatility
        min_leverage_local: float, default: 0.0
            A minimum adjustment factor
        max_leverage_local: float, default: 99999.0
            A maximum adjustment factor
        level: float, default: 0.95
            The sought VaR level
        months_from_last : int, optional
            number of months offset as positive integer. Overrides use of from_date
            and to_date
        from_date : datetime.date, optional
            Specific from date
        to_date : datetime.date, optional
            Specific to date
        interpolation: Literal["linear", "lower", "higher", "midpoint",
        "nearest"], default: "lower"
            type of interpolation in Pandas.DataFrame.quantile() function.
        drift_adjust: bool, default: False
            An adjustment to remove the bias implied by the average return
        periods_in_a_year_fixed : int, optional
            Allows locking the periods-in-a-year to simplify test cases and
            comparisons

        Returns
        -------
        Pandas.Series
            A position weight multiplier from the ratio between a VaR implied
            volatility and a given target volatility. Multiplier = 1.0 -> target met
        """

        vfv = self.vol_from_var_func(
            level=level,
            months_from_last=months_from_last,
            from_date=from_date,
            to_date=to_date,
            interpolation=interpolation,
            drift_adjust=drift_adjust,
            periods_in_a_year_fixed=periods_in_a_year_fixed,
        )
        vfv = vfv.apply(
            lambda x: max(min_leverage_local, min(target_vol / x, max_leverage_local))
        )
        return Series(
            data=vfv, name=f"Weight from target vol {target_vol:.1%}", dtype="float64"
        )

    def value_to_ret(self: TOpenFrame) -> TOpenFrame:
        """
        Returns
        -------
        OpenFrame
            The returns of the values in the series
        """

        self.tsdf = self.tsdf.pct_change()
        self.tsdf.iloc[0] = 0
        new_labels = ["Return(Total)"] * self.item_count
        arrays = [self.tsdf.columns.get_level_values(0), new_labels]
        self.tsdf.columns = MultiIndex.from_arrays(arrays)
        return self

    def value_to_diff(self: TOpenFrame, periods: int = 1) -> TOpenFrame:
        """Converts valueseries to series of their period differences

        Parameters
        ----------
        periods: int, default: 1
            The number of periods between observations over which difference
            is calculated

        Returns
        -------
        OpenFrame
            An OpenFrame object
        """

        self.tsdf = self.tsdf.diff(periods=periods)
        self.tsdf.iloc[0] = 0
        new_labels = ["Return(Total)"] * self.item_count
        arrays = [self.tsdf.columns.get_level_values(0), new_labels]
        self.tsdf.columns = MultiIndex.from_arrays(arrays)
        return self

    def value_to_log(self: TOpenFrame) -> TOpenFrame:
        """Converts a valueseries into logarithmic return series \n
        Equivalent to LN(value[t] / value[t=0]) in MS Excel

        Returns
        -------
        OpenFrame
            An OpenFrame object
        """

        self.tsdf = log(self.tsdf / self.tsdf.iloc[0])
        return self

    def to_cumret(self: TOpenFrame) -> TOpenFrame:
        """Converts returnseries into cumulative valueseries

        Returns
        -------
        OpenFrame
            An OpenFrame object
        """
        if any(
            [
                True if x == "Price(Close)" else False
                for x in self.tsdf.columns.get_level_values(1).values
            ]
        ):
            self.value_to_ret()

        self.tsdf = self.tsdf.add(1.0)
        self.tsdf = self.tsdf.apply(cumprod, axis="index") / self.tsdf.iloc[0]
        new_labels = ["Price(Close)"] * self.item_count
        arrays = [self.tsdf.columns.get_level_values(0), new_labels]
        self.tsdf.columns = MultiIndex.from_arrays(arrays)
        return self

    def resample(self: TOpenFrame, freq: str = "BM") -> TOpenFrame:
        """Resamples the timeseries frequency

        Parameters
        ----------
        freq: str, default "BM"
            The date offset string that sets the resampled frequency
            Examples are "7D", "B", "M", "BM", "Q", "BQ", "A", "BA"

        Returns
        -------
        OpenFrame
            An OpenFrame object
        """

        self.tsdf.index = DatetimeIndex(self.tsdf.index)
        self.tsdf = self.tsdf.resample(freq).last()
        self.tsdf.index = [d.date() for d in DatetimeIndex(self.tsdf.index)]
        for x in self.constituents:
            x.tsdf.index = DatetimeIndex(x.tsdf.index)
            x.tsdf = x.tsdf.resample(freq).last()
            x.tsdf.index = [d.date() for d in DatetimeIndex(x.tsdf.index)]

        return self

    def resample_to_business_period_ends(
        self: TOpenFrame,
        freq: Literal["BM", "BQ", "BA"] = "BM",
        countries: list | str = "SE",
        convention: Literal["start", "s", "end", "e"] = "end",
        method: Literal[
            None, "pad", "ffill", "backfill", "bfill", "nearest"
        ] = "nearest",
    ) -> TOpenFrame:
        """Resamples timeseries frequency to the business calendar
        month end dates of each period while leaving any stubs
        in place. Stubs will be aligned to the shortest stub

        Parameters
        ----------
        freq: Literal["BM", "BQ", "BA"], default BM
            The date offset string that sets the resampled frequency
        countries: list | str, default: "SE"
            (List of) country code(s) according to ISO 3166-1 alpha-2
            to create a business day calendar used for date adjustments
        convention: Literal["start", "s", "end", "e"], default; end
            Controls whether to use the start or end of `rule`.
        method: Literal[None, "pad", "ffill", "backfill", "bfill",
        "nearest"], default: nearest
            Controls the method used to align values across columns

        Returns
        -------
        OpenFrame
            An OpenFrame object
        """

        head = self.tsdf.loc[self.first_indices.max()].copy()
        head = head.to_frame().T
        tail = self.tsdf.loc[self.last_indices.min()].copy()
        tail = tail.to_frame().T
        self.tsdf.index = DatetimeIndex(self.tsdf.index)
        self.tsdf = self.tsdf.resample(rule=freq, convention=convention).last()
        self.tsdf.drop(index=self.tsdf.index[-1], inplace=True)
        self.tsdf.index = [d.date() for d in DatetimeIndex(self.tsdf.index)]

        if head.index[0] not in self.tsdf.index:
            self.tsdf = concat([self.tsdf, head])

        if tail.index[0] not in self.tsdf.index:
            self.tsdf = concat([self.tsdf, tail])

        self.tsdf.sort_index(inplace=True)

        dates = DatetimeIndex(
            [self.tsdf.index[0]]
            + [
                date_offset_foll(
                    dt.date(d.year, d.month, 1)
                    + relativedelta(months=1)
                    - dt.timedelta(days=1),
                    countries=countries,
                    months_offset=0,
                    adjust=True,
                    following=False,
                )
                for d in self.tsdf.index[1:-1]
            ]
            + [self.tsdf.index[-1]]
        )
        dates = dates.drop_duplicates()
        self.tsdf = self.tsdf.reindex([d.date() for d in dates], method=method)
        for x in self.constituents:
            x.tsdf = x.tsdf.reindex([d.date() for d in dates], method=method)
        return self

    def to_drawdown_series(self: TOpenFrame) -> TOpenFrame:
        """Converts the timeseries into a drawdown series

        Returns
        -------
        OpenFrame
            An OpenFrame object
        """

        for t in self.tsdf:
            self.tsdf.loc[:, t] = drawdown_series(self.tsdf.loc[:, t])
        return self

    def drawdown_details(self: TOpenFrame) -> DataFrame:
        """
        Returns
        -------
        Pandas.DataFrame
            Calculates 'Max Drawdown', 'Start of drawdown', 'Date of bottom',
            'Days from start to bottom', & 'Average fall per day'
        """

        mddf = DataFrame()
        for i in self.constituents:
            tmpdf = i.tsdf.copy()
            tmpdf.index = DatetimeIndex(tmpdf.index)
            dd = drawdown_details(tmpdf)
            dd.name = i.label
            mddf = concat([mddf, dd], axis="columns")
        return mddf

    def ewma_risk(
        self: TOpenFrame,
        lmbda: float = 0.94,
        day_chunk: int = 11,
        dlta_degr_freedms: int = 0,
        first_column: int = 0,
        second_column: int = 1,
        months_from_last: int | None = None,
        from_date: dt.date | None = None,
        to_date: dt.date | None = None,
        periods_in_a_year_fixed: int | None = None,
    ) -> DataFrame:
        """Exponentially Weighted Moving Average Model for Volatilities and
        Correlation.
        https://www.investopedia.com/articles/07/ewma.asp

        Parameters
        ----------
        lmbda: float, default: 0.94
            Scaling factor to determine weighting.
        day_chunk: int, default: 0
            Sampling the data which is assumed to be daily.
        dlta_degr_freedms: int, default: 0
            Variance bias factor taking the value 0 or 1.
        first_column: int, default: 0
            Column of first timeseries.
        second_column: int, default: 1
            Column of second timeseries.
        months_from_last : int, optional
            number of months offset as positive integer. Overrides use of from_date
            and to_date
        from_date : datetime.date, optional
            Specific from date
        to_date : datetime.date, optional
            Specific to date
        periods_in_a_year_fixed : int, optional
            Allows locking the periods-in-a-year to simplify test cases and
            comparisons

        Returns
        -------
        Pandas.DataFrame
            Series volatilities and correlation
        """

        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        if periods_in_a_year_fixed is None:
            fraction = (later - earlier).days / 365.25
            how_many = int(
                self.tsdf.loc[earlier:later].count(numeric_only=True).iloc[0]
            )
            time_factor = how_many / fraction
        else:
            time_factor = periods_in_a_year_fixed
            how_many = int(self.length)

        corr_label = (
            self.tsdf.iloc[:, first_column].name[0]
            + "_VS_"
            + self.tsdf.iloc[:, second_column].name[0]
        )
        cols = [
            self.tsdf.iloc[:, first_column].name[0],
            self.tsdf.iloc[:, second_column].name[0],
        ]

        data = self.tsdf.loc[earlier:later].copy()

        for rtn in cols:
            data[rtn, "Returns"] = log(data.loc[:, (rtn, "Price(Close)")]).diff()
            data[rtn, "EWMA"] = zeros(how_many)
            data.loc[:, (rtn, "EWMA")].iloc[0] = data.loc[:, (rtn, "Returns")].iloc[
                1:day_chunk
            ].std(ddof=dlta_degr_freedms) * sqrt(time_factor)

        data["Cov", "EWMA"] = zeros(how_many)
        data[corr_label, "EWMA"] = zeros(how_many)
        data.loc[:, ("Cov", "EWMA")].iloc[0] = cov(
            m=data.loc[:, (cols[0], "Returns")].iloc[1:day_chunk].to_numpy(),
            y=data.loc[:, (cols[1], "Returns")].iloc[1:day_chunk].to_numpy(),
            ddof=dlta_degr_freedms,
        )[0][1]
        data.loc[:, (corr_label, "EWMA")].iloc[0] = data.loc[:, ("Cov", "EWMA")].iloc[
            0
        ] / (
            2
            * data.loc[:, (cols[0], "EWMA")].iloc[0]
            * data.loc[:, (cols[1], "EWMA")].iloc[0]
        )

        prev = data.loc[self.first_idx]
        for _, row in data.iloc[1:].iterrows():
            row.loc[cols, "EWMA"] = sqrt(
                square(row.loc[cols, "Returns"].to_numpy()) * time_factor * (1 - lmbda)
                + square(prev.loc[cols, "EWMA"].to_numpy()) * lmbda
            )
            row.loc["Cov", "EWMA"] = (
                row.loc[cols[0], "Returns"]
                * row.loc[cols[1], "Returns"]
                * time_factor
                * (1 - lmbda)
                + prev.loc["Cov", "EWMA"] * lmbda
            )
            row.loc[corr_label, "EWMA"] = row.loc["Cov", "EWMA"] / (
                2 * row.loc[cols[0], "EWMA"] * row.loc[cols[1], "EWMA"]
            )
            prev = row.copy()

        ewma_df = data.loc[:, (cols + [corr_label], "EWMA")]
        ewma_df.columns = ewma_df.columns.droplevel(level=1)

        return ewma_df

    def rolling_vol(
        self: TOpenFrame,
        column: int,
        observations: int = 21,
        periods_in_a_year_fixed: int | None = None,
    ) -> DataFrame:
        """
        Parameters
        ----------
        column: int
            Position as integer of column to calculate
        observations: int, default: 21
            Number of observations in the overlapping window.
        periods_in_a_year_fixed : int, optional
            Allows locking the periods-in-a-year to simplify test cases and
            comparisons

        Returns
        -------
        Pandas.DataFrame
            Rolling annualised volatilities
        """

        if periods_in_a_year_fixed:
            time_factor = periods_in_a_year_fixed
        else:
            time_factor = self.periods_in_a_year
        vol_label = self.tsdf.iloc[:, column].name[0]
        df = self.tsdf.iloc[:, column].pct_change()
        voldf = df.rolling(observations, min_periods=observations).std() * sqrt(
            time_factor
        )
        voldf = voldf.dropna().to_frame()
        voldf.columns = [[vol_label], ["Rolling volatility"]]

        return voldf

    def rolling_return(
        self: TOpenFrame, column: int, observations: int = 21
    ) -> DataFrame:
        """
        Parameters
        ----------
        column: int
            Position as integer of column to calculate
        observations: int, default: 21
            Number of observations in the overlapping window.

        Returns
        -------
        Pandas.DataFrame
            Rolling returns
        """

        ret_label = self.tsdf.iloc[:, column].name[0]
        retdf = (
            self.tsdf.iloc[:, column]
            .pct_change()
            .rolling(observations, min_periods=observations)
            .sum()
        )
        retdf = retdf.dropna().to_frame()
        retdf.columns = [[ret_label], ["Rolling returns"]]

        return retdf

    def rolling_cvar_down(
        self: TOpenFrame, column: int, level: float = 0.95, observations: int = 252
    ) -> DataFrame:
        """
        Parameters
        ----------
        column: int
            Position as integer of column to calculate
        level: float, default: 0.95
            The sought Conditional Value At Risk level
        observations: int, default: 252
            Number of observations in the overlapping window.

        Returns
        -------
        Pandas.DataFrame
            Rolling annualized downside CVaR
        """

        cvar_label = self.tsdf.iloc[:, column].name[0]
        cvardf = (
            self.tsdf.iloc[:, column]
            .rolling(observations, min_periods=observations)
            .apply(lambda x: cvar_down(x, level=level))
        )
        cvardf = cvardf.dropna().to_frame()
        cvardf.columns = [[cvar_label], ["Rolling CVaR"]]

        return cvardf

    def rolling_var_down(
        self: TOpenFrame,
        column: int,
        level: float = 0.95,
        interpolation: Literal[
            "linear", "lower", "higher", "midpoint", "nearest"
        ] = "lower",
        observations: int = 252,
    ) -> DataFrame:
        """
        Parameters
        ----------
        column: int
            Position as integer of column to calculate
        level: float, default: 0.95
            The sought Value At Risk level
        observations: int, default: 252
            Number of observations in the overlapping window.
        interpolation: Literal["linear", "lower", "higher", "midpoint",
        "nearest"], default: "lower"
            Type of interpolation in Pandas.DataFrame.quantile() function.

        Returns
        -------
        Pandas.DataFrame
           Rolling annualized downside Value At Risk "VaR"
        """

        var_label = self.tsdf.iloc[:, column].name[0]
        vardf = (
            self.tsdf.iloc[:, column]
            .rolling(observations, min_periods=observations)
            .apply(lambda x: var_down(x, level=level, interpolation=interpolation))
        )
        vardf = vardf.dropna().to_frame()
        vardf.columns = [[var_label], ["Rolling VaR"]]

        return vardf

    def value_nan_handle(
        self: TOpenFrame, method: Literal["fill", "drop"] = "fill"
    ) -> TOpenFrame:
        """Handling of missing values in a valueseries

        Parameters
        ----------
        method: Literal["fill", "drop"], default: "fill"
            Method used to handle NaN. Either fill with last known or drop

        Returns
        -------
        OpenFrame
            An OpenFrame object
        """

        assert method in [
            "fill",
            "drop",
        ], "Method must be either fill or drop passed as string."
        if method == "fill":
            self.tsdf.fillna(method="pad", inplace=True)
        else:
            self.tsdf.dropna(inplace=True)
        return self

    def return_nan_handle(
        self: TOpenFrame, method: Literal["fill", "drop"] = "fill"
    ) -> TOpenFrame:
        """Handling of missing values in a returnseries

        Parameters
        ----------
        method: Literal["fill", "drop"], default: "fill"
            Method used to handle NaN. Either fill with zero or drop

        Returns
        -------
        OpenFrame
            An OpenFrame object
        """

        assert method in [
            "fill",
            "drop",
        ], "Method must be either fill or drop passed as string."
        if method == "fill":
            self.tsdf.fillna(value=0.0, inplace=True)
        else:
            self.tsdf.dropna(inplace=True)
        return self

    @property
    def correl_matrix(self: TOpenFrame) -> DataFrame:
        """
        Returns
        -------
        Pandas.DataFrame
            Correlation matrix
        """
        corr_matrix = self.tsdf.pct_change().corr(method="pearson", min_periods=1)
        corr_matrix.columns = corr_matrix.columns.droplevel(level=1)
        corr_matrix.index = corr_matrix.index.droplevel(level=1)
        corr_matrix.index.name = "Correlation"
        return corr_matrix

    def add_timeseries(self: TOpenFrame, new_series: OpenTimeSeries) -> TOpenFrame:
        """
        Parameters
        ----------
        new_series: OpenTimeSeries
            The timeseries to add

        Returns
        -------
        OpenFrame
            An OpenFrame object
        """

        self.constituents += [new_series]
        self.tsdf = concat([self.tsdf, new_series.tsdf], axis="columns", sort=True)
        return self

    def delete_timeseries(self: TOpenFrame, lvl_zero_item: str) -> TOpenFrame:
        """
        Parameters
        ----------
        lvl_zero_item: str
            The .tsdf column level 0 value of the timeseries to delete

        Returns
        -------
        OpenFrame
            An OpenFrame object
        """

        if self.weights:
            new_c, new_w = [], []
            for cc, ww in zip(self.constituents, self.weights):
                if cc.label != lvl_zero_item:
                    new_c.append(cc)
                    new_w.append(ww)
            self.constituents = new_c
            self.weights = new_w
        else:
            self.constituents = [
                ff for ff in self.constituents if ff.label != lvl_zero_item
            ]
        self.tsdf.drop(lvl_zero_item, axis="columns", level=0, inplace=True)
        return self

    def trunc_frame(
        self: TOpenFrame,
        start_cut: dt.date | None = None,
        end_cut: dt.date | None = None,
        before: bool = True,
        after: bool = True,
    ) -> TOpenFrame:
        """Truncates DataFrame such that all timeseries have the same time span

        Parameters
        ----------
        start_cut: datetime.date, optional
            New first date
        end_cut: datetime.date, optional
            New last date
        before: bool, default: True
            If True method will truncate to the common earliest start date also
            when start_cut = None.
        after: bool, default: True
            If True method will truncate to the common latest end date also
            when end_cut = None.

        Returns
        -------
        OpenFrame
            An OpenFrame object
        """

        if not start_cut and before:
            start_cut = self.first_indices.max()
        if not end_cut and after:
            end_cut = self.last_indices.min()
        self.tsdf.sort_index(inplace=True)
        self.tsdf = self.tsdf.truncate(before=start_cut, after=end_cut, copy=False)

        for x in self.constituents:
            x.tsdf = x.tsdf.truncate(before=start_cut, after=end_cut, copy=False)
        if len(set(self.first_indices)) != 1:
            warning(
                f"One or more constituents still not truncated to same "
                f"start dates.\n"
                f"{self.tsdf.head()}"
            )
        if len(set(self.last_indices)) != 1:
            warning(
                f"One or more constituents still not truncated to same "
                f"end dates.\n"
                f"{self.tsdf.tail()}"
            )
        return self

    def relative(
        self: TOpenFrame,
        long_column: int = 0,
        short_column: int = 1,
        base_zero: bool = True,
    ):
        """Calculates cumulative relative return between two series.
        A new series is added to the frame.

        Parameters
        ----------
        long_column: int, default: 0
            Column # of timeseries bought
        short_column: int, default: 1
            Column # of timeseries sold
        base_zero: bool, default: True
            If set to False 1.0 is added to allow for a capital base and
            to allow a volatility calculation
        """

        rel_label = (
            self.tsdf.iloc[:, long_column].name[0]
            + "_over_"
            + self.tsdf.iloc[:, short_column].name[0]
        )
        if base_zero:
            self.tsdf[rel_label, "Relative return"] = (
                self.tsdf.iloc[:, long_column] - self.tsdf.iloc[:, short_column]
            )
        else:
            self.tsdf[rel_label, "Relative return"] = (
                1.0 + self.tsdf.iloc[:, long_column] - self.tsdf.iloc[:, short_column]
            )

    def tracking_error_func(
        self: TOpenFrame,
        base_column: tuple | int = -1,
        months_from_last: int | None = None,
        from_date: dt.date | None = None,
        to_date: dt.date | None = None,
        periods_in_a_year_fixed: int | None = None,
    ) -> Series:
        """Calculates the Tracking Error which is the standard deviation of the
        difference between the fund and its index returns. \n
        https://www.investopedia.com/terms/t/trackingerror.asp

        Parameters
        ----------
        base_column: int | None, default: -1
            Column of timeseries that is the denominator in the ratio.
        months_from_last : int, optional
            number of months offset as positive integer. Overrides use of from_date
            and to_date
        from_date : datetime.date, optional
            Specific from date
        to_date : datetime.date, optional
            Specific to date
        periods_in_a_year_fixed : int, optional
            Allows locking the periods-in-a-year to simplify test cases and
            comparisons

        Returns
        -------
        Pandas.Series
            Tracking Errors
        """

        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        fraction = (later - earlier).days / 365.25

        if isinstance(base_column, tuple):
            shortdf = self.tsdf.loc[earlier:later].loc[:, base_column]
            short_item = base_column
            short_label = self.tsdf.loc[:, base_column].name[0]
        elif isinstance(base_column, int):
            shortdf = self.tsdf.loc[earlier:later].iloc[:, base_column]
            short_item = self.tsdf.iloc[:, base_column].name
            short_label = self.tsdf.iloc[:, base_column].name[0]
        else:
            raise Exception("base_column should be a tuple or an integer.")

        if periods_in_a_year_fixed:
            time_factor = periods_in_a_year_fixed
        else:
            time_factor = shortdf.count() / fraction

        terrors = []
        for item in self.tsdf:
            if item == short_item:
                terrors.append(0.0)
            else:
                longdf = self.tsdf.loc[earlier:later].loc[:, item]
                relative = 1.0 + longdf - shortdf
                vol = float(relative.pct_change().std() * sqrt(time_factor))
                terrors.append(vol)

        return Series(
            data=terrors,
            index=self.tsdf.columns,
            name=f"Tracking Errors vs {short_label}",
            dtype="float64",
        )

    def info_ratio_func(
        self: TOpenFrame,
        base_column: tuple | int = -1,
        months_from_last: int | None = None,
        from_date: dt.date | None = None,
        to_date: dt.date | None = None,
        periods_in_a_year_fixed: int | None = None,
    ) -> Series:
        """The Information Ratio equals ( fund return less index return ) divided
        by the Tracking Error. And the Tracking Error is the standard deviation of
        the difference between the fund and its index returns.
        The ratio is calculated using the annualized arithmetic mean of returns.

        Parameters
        ----------
        base_column: int | None, default: -1
            Column of timeseries that is the denominator in the ratio.
        months_from_last : int, optional
            number of months offset as positive integer. Overrides use of from_date
            and to_date
        from_date : datetime.date, optional
            Specific from date
        to_date : datetime.date, optional
            Specific to date
        periods_in_a_year_fixed : int, optional
            Allows locking the periods-in-a-year to simplify test cases and
            comparisons

        Returns
        -------
        Pandas.Series
            Information Ratios
        """

        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        fraction = (later - earlier).days / 365.25

        if isinstance(base_column, tuple):
            shortdf = self.tsdf.loc[earlier:later].loc[:, base_column]
            short_item = base_column
            short_label = self.tsdf.loc[:, base_column].name[0]
        elif isinstance(base_column, int):
            shortdf = self.tsdf.loc[earlier:later].iloc[:, base_column]
            short_item = self.tsdf.iloc[:, base_column].name
            short_label = self.tsdf.iloc[:, base_column].name[0]
        else:
            raise Exception("base_column should be a tuple or an integer.")

        if periods_in_a_year_fixed:
            time_factor = periods_in_a_year_fixed
        else:
            time_factor = shortdf.count() / fraction

        ratios = []
        for item in self.tsdf:
            if item == short_item:
                ratios.append(0.0)
            else:
                longdf = self.tsdf.loc[earlier:later].loc[:, item]
                relative = 1.0 + longdf - shortdf
                ret = float(relative.pct_change().mean() * time_factor)
                vol = float(relative.pct_change().std() * sqrt(time_factor))
                ratios.append(ret / vol)

        return Series(
            data=ratios,
            index=self.tsdf.columns,
            name=f"Info Ratios vs {short_label}",
            dtype="float64",
        )

    def capture_ratio_func(
        self: TOpenFrame,
        ratio: Literal["up", "down", "both"],
        base_column: tuple | int = -1,
        months_from_last: int | None = None,
        from_date: dt.date | None = None,
        to_date: dt.date | None = None,
        periods_in_a_year_fixed: int | None = None,
    ) -> Series:
        """The Up (Down) Capture Ratio is calculated by dividing the CAGR
        of the asset during periods that the benchmark returns are positive (negative)
        by the CAGR of the benchmark during the same periods.
        CaptureRatio.BOTH is the Up ratio divided by the Down ratio.
        Source: 'Capture Ratios: A Popular Method of Measuring Portfolio Performance
        in Practice', Don R. Cox and Delbert C. Goff, Journal of Economics and
        Finance Education (Vol 2 Winter 2013).
        https://www.economics-finance.org/jefe/volume12-2/11ArticleCox.pdf

        Parameters
        ----------
        ratio: Literal["up", "down", "both"]
            Either 'up', 'down' or 'both'
        base_column: int | None, default: -1
            Column of timeseries that is the denominator in the ratio.
        months_from_last : int, optional
            number of months offset as positive integer. Overrides use of from_date
            and to_date
        from_date : datetime.date, optional
            Specific from date
        to_date : datetime.date, optional
            Specific to date
        periods_in_a_year_fixed : int, optional
            Allows locking the periods-in-a-year to simplify test cases and
            comparisons

        Returns
        -------
        Pandas.Series
            Capture Ratios
        """

        assert ratio in [
            "up",
            "down",
            "both",
        ], "Ratio must be one of 'up', 'down' or 'both'."

        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        fraction = (later - earlier).days / 365.25

        if isinstance(base_column, tuple):
            shortdf = self.tsdf.loc[earlier:later].loc[:, base_column]
            short_item = base_column
            short_label = self.tsdf.loc[:, base_column].name[0]
        elif isinstance(base_column, int):
            shortdf = self.tsdf.loc[earlier:later].iloc[:, base_column]
            short_item = self.tsdf.iloc[:, base_column].name
            short_label = self.tsdf.iloc[:, base_column].name[0]
        else:
            raise Exception("base_column should be a tuple or an integer.")

        if periods_in_a_year_fixed:
            time_factor = periods_in_a_year_fixed
        else:
            time_factor = shortdf.count() / fraction

        ratios = []
        for item in self.tsdf:
            if item == short_item:
                ratios.append(0.0)
            else:
                longdf = self.tsdf.loc[earlier:later].loc[:, item]
                if ratio == "up":
                    uparray = (
                        longdf.pct_change()[shortdf.pct_change().values > 0.0]
                        .add(1)
                        .values
                    )
                    up_return = uparray.prod() ** (1 / (len(uparray) / time_factor)) - 1
                    upidxarray = (
                        shortdf.pct_change()[shortdf.pct_change().values > 0.0]
                        .add(1)
                        .values
                    )
                    up_idx_return = (
                        upidxarray.prod() ** (1 / (len(upidxarray) / time_factor)) - 1
                    )
                    ratios.append(up_return / up_idx_return)
                elif ratio == "down":
                    downarray = (
                        longdf.pct_change()[shortdf.pct_change().values < 0.0]
                        .add(1)
                        .values
                    )
                    down_return = (
                        downarray.prod() ** (1 / (len(downarray) / time_factor)) - 1
                    )
                    downidxarray = (
                        shortdf.pct_change()[shortdf.pct_change().values < 0.0]
                        .add(1)
                        .values
                    )
                    down_idx_return = (
                        downidxarray.prod() ** (1 / (len(downidxarray) / time_factor))
                        - 1
                    )
                    ratios.append(down_return / down_idx_return)
                elif ratio == "both":
                    uparray = (
                        longdf.pct_change()[shortdf.pct_change().values > 0.0]
                        .add(1)
                        .values
                    )
                    up_return = uparray.prod() ** (1 / (len(uparray) / time_factor)) - 1
                    upidxarray = (
                        shortdf.pct_change()[shortdf.pct_change().values > 0.0]
                        .add(1)
                        .values
                    )
                    up_idx_return = (
                        upidxarray.prod() ** (1 / (len(upidxarray) / time_factor)) - 1
                    )
                    downarray = (
                        longdf.pct_change()[shortdf.pct_change().values < 0.0]
                        .add(1)
                        .values
                    )
                    down_return = (
                        downarray.prod() ** (1 / (len(downarray) / time_factor)) - 1
                    )
                    downidxarray = (
                        shortdf.pct_change()[shortdf.pct_change().values < 0.0]
                        .add(1)
                        .values
                    )
                    down_idx_return = (
                        downidxarray.prod() ** (1 / (len(downidxarray) / time_factor))
                        - 1
                    )
                    ratios.append(
                        (up_return / up_idx_return) / (down_return / down_idx_return)
                    )

        if ratio == "up":
            resultname = f"Up Capture Ratios vs {short_label}"
        elif ratio == "down":
            resultname = f"Down Capture Ratios vs {short_label}"
        else:
            resultname = f"Up-Down Capture Ratios vs {short_label}"

        return Series(
            data=ratios,
            index=self.tsdf.columns,
            name=resultname,
            dtype="float64",
        )

    def beta(self: TOpenFrame, asset: tuple | int, market: tuple | int) -> float:
        """https://www.investopedia.com/terms/b/beta.asp
        Calculates Beta as Co-variance of asset & market divided by Variance of market

        Parameters
        ----------
        asset: tuple | int
            The column of the asset
        market: tuple | int
            The column of the market against which Beta is measured

        Returns
        -------
        float
            Beta as Co-variance of x & y divided by Variance of x
        """
        if all(
            [
                True if x == "Return(Total)" else False
                for x in self.tsdf.columns.get_level_values(1).values
            ]
        ):
            if isinstance(asset, tuple):
                y = self.tsdf.loc[:, asset]
            elif isinstance(asset, int):
                y = self.tsdf.iloc[:, asset]
            else:
                raise Exception("asset should be a tuple or an integer.")
            if isinstance(market, tuple):
                x = self.tsdf.loc[:, market]
            elif isinstance(market, int):
                x = self.tsdf.iloc[:, market]
            else:
                raise Exception("market should be a tuple or an integer.")
        else:
            if isinstance(asset, tuple):
                y = log(self.tsdf.loc[:, asset] / self.tsdf.loc[:, asset].iloc[0])
            elif isinstance(asset, int):
                y = log(self.tsdf.iloc[:, asset] / self.tsdf.iloc[0, asset])
            else:
                raise Exception("asset should be a tuple or an integer.")
            if isinstance(market, tuple):
                x = log(self.tsdf.loc[:, market] / self.tsdf.loc[:, market].iloc[0])
            elif isinstance(market, int):
                x = log(self.tsdf.iloc[:, market] / self.tsdf.iloc[0, market])
            else:
                raise Exception("market should be a tuple or an integer.")

        covariance = cov(y, x, ddof=1)
        beta = covariance[0, 1] / covariance[1, 1]

        return beta

    def ord_least_squares_fit(
        self: TOpenFrame,
        y_column: tuple | int,
        x_column: tuple | int,
        fitted_series: bool = True,
    ) -> RegressionResults:
        """https://www.statsmodels.org/stable/examples/notebooks/generated/ols.html
        Performs a linear regression and adds a new column with a fitted line
        using Ordinary Least Squares fit

        Parameters
        ----------
        y_column: tuple | int
            The column level values of the dependent variable y
        x_column: tuple | int
            The column level values of the exogenous variable x
        fitted_series: bool, default: True
            If True the fit is added as a new column in the .tsdf Pandas.DataFrame

        Returns
        -------
        RegressionResults
            The Statsmodels regression output
        """

        if isinstance(y_column, tuple):
            y = self.tsdf.loc[:, y_column]
            y_label = self.tsdf.loc[:, y_column].name[0]
        elif isinstance(y_column, int):
            y = self.tsdf.iloc[:, y_column]
            y_label = self.tsdf.iloc[:, y_column].name[0]
        else:
            raise Exception("y_column should be a tuple or an integer.")

        if isinstance(x_column, tuple):
            x = self.tsdf.loc[:, x_column]
            x_label = self.tsdf.loc[:, x_column].name[0]
        elif isinstance(x_column, int):
            x = self.tsdf.iloc[:, x_column]
            x_label = self.tsdf.iloc[:, x_column].name[0]
        else:
            raise Exception("x_column should be a tuple or an integer.")

        results = OLS(y, x).fit()
        if fitted_series:
            self.tsdf[y_label, x_label] = results.predict(x)

        return results

    def make_portfolio(self: TOpenFrame, name: str) -> DataFrame:
        """Calculates a basket timeseries based on the supplied weights

        Parameters
        ----------
        name: str
            Name of the basket timeseries

        Returns
        -------
        Pandas.DataFrame
            A basket timeseries
        """
        if self.weights is None:
            raise Exception(
                "OpenFrame weights property must be provided to run the "
                "make_portfolio method."
            )
        df = self.tsdf.copy()
        if not any(
            [
                True if x == "Return(Total)" else False
                for x in self.tsdf.columns.get_level_values(1).values
            ]
        ):
            df = df.pct_change()
            df.iloc[0] = 0
        portfolio = df.dot(self.weights)
        portfolio = portfolio.add(1.0).cumprod().to_frame()
        portfolio.columns = [[name], ["Price(Close)"]]
        return portfolio

    def rolling_info_ratio(
        self: TOpenFrame,
        long_column: int = 0,
        short_column: int = 1,
        observations: int = 21,
        periods_in_a_year_fixed: int | None = None,
    ) -> DataFrame:
        """The Information Ratio equals ( fund return less index return ) divided by the
        Tracking Error. And the Tracking Error is the standard deviation of the
        difference between the fund and its index returns.

        Parameters
        ----------
        long_column: int, default: 0
            Column of timeseries that is the numerator in the ratio.
        short_column: int, default: 1
            Column of timeseries that is the denominator in the ratio.
        observations: int, default: 21
            The length of the rolling window to use is set as number of observations.
        periods_in_a_year_fixed : int, optional
            Allows locking the periods-in-a-year to simplify test cases and comparisons

        Returns
        -------
        Pandas.DataFrame
            Rolling Information Ratios
        """

        ratio_label = (
            f"{self.tsdf.iloc[:, long_column].name[0]}"
            f" / {self.tsdf.iloc[:, short_column].name[0]}"
        )
        if periods_in_a_year_fixed:
            time_factor = periods_in_a_year_fixed
        else:
            time_factor = self.periods_in_a_year

        relative = (
            1.0 + self.tsdf.iloc[:, long_column] - self.tsdf.iloc[:, short_column]
        )

        retdf = (
            relative.pct_change().rolling(observations, min_periods=observations).sum()
        )
        retdf = retdf.dropna().to_frame()

        voldf = relative.pct_change().rolling(
            observations, min_periods=observations
        ).std() * sqrt(time_factor)
        voldf = voldf.dropna().to_frame()

        ratiodf = (retdf.iloc[:, 0] / voldf.iloc[:, 0]).to_frame()
        ratiodf.columns = [[ratio_label], ["Information Ratio"]]

        return ratiodf

    def rolling_beta(
        self: TOpenFrame,
        asset_column: int = 0,
        market_column: int = 1,
        observations: int = 21,
    ) -> DataFrame:
        """https://www.investopedia.com/terms/b/beta.asp
        Calculates Beta as Co-variance of asset & market divided by Variance of market

        Parameters
        ----------
        asset_column: int, default: 0
            Column of timeseries that is the asset.
        market_column: int, default: 1
            Column of timeseries that is the market.
        observations: int, default: 21
            The length of the rolling window to use is set as number of observations.

        Returns
        -------
        Pandas.DataFrame
            Rolling Betas
        """
        market_label = self.tsdf.iloc[:, market_column].name[0]
        beta_label = f"{self.tsdf.iloc[:, asset_column].name[0]}" f" / {market_label}"

        rolling = self.tsdf.copy()
        rolling = rolling.pct_change().rolling(observations, min_periods=observations)

        rcov = rolling.cov()
        rcov.dropna(inplace=True)

        rollbeta = rcov.iloc[:, asset_column].xs(market_label, level=1) / rcov.iloc[
            :, market_column
        ].xs(market_label, level=1)
        rollbeta = rollbeta.to_frame()
        rollbeta.index = rollbeta.index.droplevel(level=1)
        rollbeta.columns = [[beta_label], ["Beta"]]

        return rollbeta

    def rolling_corr(
        self: TOpenFrame,
        first_column: int = 0,
        second_column: int = 1,
        observations: int = 21,
    ) -> DataFrame:
        """Calculates correlation between two series. The period with
        at least the given number of observations is the first period calculated.

        Parameters
        ----------
        first_column: int, default: 0
            The position as integer of the first timeseries to compare
        second_column: int, default: 1
            The position as integer of the second timeseries to compare
        observations: int, default: 21
            The length of the rolling window to use is set as number of observations

        Returns
        -------
        Pandas.DataFrame
            Rolling Correlations
        """

        corr_label = (
            self.tsdf.iloc[:, first_column].name[0]
            + "_VS_"
            + self.tsdf.iloc[:, second_column].name[0]
        )
        corrdf = (
            self.tsdf.iloc[:, first_column]
            .pct_change()[1:]
            .rolling(observations, min_periods=observations)
            .corr(self.tsdf.iloc[:, second_column].pct_change()[1:])
        )
        corrdf = corrdf.dropna().to_frame()
        corrdf.columns = [[corr_label], ["Rolling correlation"]]

        return corrdf

    def plot_series(
        self: TOpenFrame,
        mode: Literal["lines", "markers", "lines+markers"] = "lines",
        tick_fmt: str | None = None,
        filename: str | None = None,
        directory: str | None = None,
        labels: list | None = None,
        auto_open: bool = True,
        add_logo: bool = True,
        show_last: bool = False,
        output_type: Literal["file", "div"] = "file",
    ) -> (Figure, str):
        """Creates a Plotly Figure

        To scale the bubble size, use the attribute sizeref.
        We recommend using the following formula to calculate a sizeref value:
        sizeref = 2. * max(array of size values) / (desired maximum marker size ** 2)

        Parameters
        ----------
        mode: Literal["lines", "markers", "lines+markers"], default: "lines"
            The type of scatter to use
        tick_fmt: str, optional
            None, '%', '.1%' depending on number of decimals to show
        filename: str, optional
            Name of the Plotly html file
        directory: str, optional
            Directory where Plotly html file is saved
        labels: list, optional
            A list of labels to manually override using the names of the input data
        auto_open: bool, default: True
            Determines whether to open a browser window with the plot
        add_logo: bool, default: True
            If True a Captor logo is added to the plot
        show_last: bool, default: False
            If True the last data point is highlighted as red dot with a label
        output_type: str, default: "file"
            file or div

        Returns
        -------
        (plotly.go.Figure, str)
            Plotly Figure and html filename with location
        """

        if labels:
            assert (
                len(labels) == self.item_count
            ), "Must provide same number of labels as items in frame."
        else:
            labels = self.columns_lvl_zero
        if not directory:
            directory = path.join(str(Path.home()), "Documents")
        if not filename:
            filename = "".join(choices(ascii_letters, k=6)) + ".html"
        plotfile = path.join(path.abspath(directory), filename)

        fig, logo = load_plotly_dict()
        figure = Figure(fig)
        for item in range(self.item_count):
            figure.add_scatter(
                x=self.tsdf.index,
                y=self.tsdf.iloc[:, item],
                hovertemplate="%{y}<br>%{x|%Y-%m-%d}",
                line=dict(width=2.5, dash="solid"),
                mode=mode,
                name=labels[item],
            )
        figure.update_layout(yaxis=dict(tickformat=tick_fmt))

        if add_logo:
            figure.add_layout_image(logo)

        if show_last is True:
            if tick_fmt:
                txt = "Last " + "{:" + "{}".format(tick_fmt) + "}"
            else:
                txt = "Last {}"

            for item in range(self.item_count):
                figure.add_scatter(
                    x=[self.tsdf.iloc[:, item].index[-1]],
                    y=[self.tsdf.iloc[-1, item]],
                    mode="markers + text",
                    marker={"color": "red", "size": 12},
                    hovertemplate="%{y}<br>%{x|%Y-%m-%d}",
                    showlegend=False,
                    name=labels[item],
                    text=[txt.format(self.tsdf.iloc[-1, item])],
                    textposition="top center",
                )

        plot(
            figure,
            filename=plotfile,
            auto_open=auto_open,
            link_text="",
            include_plotlyjs="cdn",
            config=fig["config"],
            output_type=output_type,
        )

        return figure, plotfile

    def plot_bars(
        self: TOpenFrame,
        mode: Literal["stack", "group", "overlay", "relative"] = "group",
        tick_fmt: str | None = None,
        filename: str | None = None,
        directory: str | None = None,
        labels: list | None = None,
        auto_open: bool = True,
        add_logo: bool = True,
        output_type: Literal["file", "div"] = "file",
    ) -> (Figure, str):
        """Creates a Plotly Bar Figure

        Parameters
        ----------
        mode: Literal["stack", "group", "overlay", "relative"], default: "group"
            The type of bar to use
        tick_fmt: str, optional
            None, '%', '.1%' depending on number of decimals to show
        filename: str, optional
            Name of the Plotly html file
        directory: str, optional
            Directory where Plotly html file is saved
        labels: list, optional
            A list of labels to manually override using the names of the input data
        auto_open: bool, default: True
            Determines whether to open a browser window with the plot
        add_logo: bool, default: True
            If True a Captor logo is added to the plot
        output_type: str, default: "file"
            file or div

        Returns
        -------
        (plotly.go.Figure, str)
            Plotly Figure and html filename with location
        """
        if labels:
            assert (
                len(labels) == self.item_count
            ), "Must provide same number of labels as items in frame."
        else:
            labels = self.columns_lvl_zero
        if not directory:
            directory = path.join(str(Path.home()), "Documents")
        if not filename:
            filename = "".join(choices(ascii_letters, k=6)) + ".html"
        plotfile = path.join(path.abspath(directory), filename)

        if mode == "overlay":
            opacity = 0.7
        else:
            opacity = None

        fig, logo = load_plotly_dict()
        figure = Figure(fig)
        for item in range(self.item_count):
            figure.add_bar(
                x=self.tsdf.index,
                y=self.tsdf.iloc[:, item],
                hovertemplate="%{y}<br>%{x|%Y-%m-%d}",
                name=labels[item],
                opacity=opacity,
            )
        figure.update_layout(barmode=mode, yaxis=dict(tickformat=tick_fmt))

        if add_logo:
            figure.add_layout_image(logo)

        plot(
            figure,
            filename=plotfile,
            auto_open=auto_open,
            link_text="",
            include_plotlyjs="cdn",
            config=fig["config"],
            output_type=output_type,
        )

        return figure, plotfile
