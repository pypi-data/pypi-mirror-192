from abc import abstractmethod
from ..sql.generator import singlecol
from ._utils import (
    _is_valid_str_percentile,
    _is_valid_str_top,
    _get_val_statistics,
)

class Preprocessor:
    """
    Abstract base class for data preprocessing operations. Subclasses should implement
    the abstract methods `define_necessary_statistics()` and `generate_sql_column()`.

    Methods
    -------
    define_necessary_statistics()
        Abstract method to define necessary statistics for preprocessing.

    generate_sql_column(previous_str: str, column_name: str, statistics_num: str, statistics_varchar: str) -> str
        Abstract method to generate SQL column for preprocessing.

    needs_subquery() -> bool
        Returns False as preprocessing does generally not require a subquery. Needs to be overwritten by Subclass
        if necessary.
    """

    @abstractmethod
    def define_necessary_statistics(self):
        pass

    @abstractmethod
    def generate_sql_column(self, previous_str, column_name, statistics_num, statistics_varchar):
        pass

    def needs_subquery(self):
        return False

class Impute(Preprocessor):
    """
    Imputes missing values in numerical columns using different strategies.

    Parameters
    ----------
    kind : str, optional
        The imputation strategy to use. The following values are possible:

        - 'mean': Replace missing values using the mean of the column.
        - 'mode': Replace missing values using the mode of the column.
        - 'min': Replace missing values using the minimum value of the column.
        - 'max': Replace missing values using the maximum value of the column.
        - 'median': Replace missing values using the median of the column.
        - 'custom': Replace missing values using a custom value or percentile.

        The default value is 'mean'.

    value : int, float, str, optional
        The value to use for the 'custom' imputation strategy. If the 'kind' parameter
        is not 'custom', this value is ignored. If 'value' is a string, it must be a
        percentile string of the form 'P[0-100]'. If 'value' is a number, it will be used
        as the constant value for imputation. The default value is 0.

    Raises
    ------
    AssertionError
        If kind is not one of the allowed values, or if the value parameter is not valid.

    Notes
    -----
    This class inherits from the Preprocessor abstract class and implements its abstract methods.
    """

    def __init__(self, kind="mean", value=0):
        assert kind in ["mean","mode","min","max","median","custom"]
        if kind == "custom":
            assert (isinstance(value,(int,float) )
                    or (isinstance(value,str) & _is_valid_str_percentile(value)))
        self.kind = kind
        self.value = value
        self.necessary_statistics = self.define_necessary_statistics()

    def define_necessary_statistics(self):
        if self.kind in ["mean","mode","min","max"]:
            return ["standard"]
        elif self.kind in ["median"]:
            return ["median"]
        elif self.kind in ["custom"]:
            if isinstance(self.value,str):
                return [("P", int(self.value[1:]))]
            else:
                return []
        else:
            return []

    def generate_sql_column(self, previous_str, column_name, statistics_num, statistics_varchar):
        # 1. read relevant values from statistics
        if self.kind in ["mean", "mode", "min", "max", "median"]:
            new_val = _get_val_statistics(statistics_num, column_name, self.kind.upper())
        elif self.kind in ["custom"]:
            if isinstance(self.value,str):
                # Percentile
                new_val = _get_val_statistics(statistics_num, column_name, "PERCENTILE"+self.value[1:])
            else:
                # constant number
                new_val = self.value
        # 2. call sql generate function
        return singlecol.impute_num(previous_str, new_val=new_val)


class ImputeText(Preprocessor):
    """
    Imputes missing values in text columns using different strategies.

    Parameters
    ----------
    kind : str, optional
        The type of imputation to perform, default is "mode". "mode" takes the most-frequent not-Null value.
        Valid options are "mode" and "custom".
    value : str, optional
        The custom value to use for imputation if kind is set to "custom".

    Raises
    ------
    AssertionError
        If kind is not one of the allowed values, or if the value parameter is not valid.

    Notes
    -----
    This class inherits from the Preprocessor abstract class and implements its abstract methods.
    """

    def __init__(self, kind="mode", value=""):
        assert kind in ["mode", "custom"]
        if kind == "custom":
            assert (isinstance(value,str))
        self.kind = kind
        self.value = value
        self.necessary_statistics = self.define_necessary_statistics()

    def define_necessary_statistics(self):
        if self.kind in ["mode"]:
            return [("TOP",1)]
        elif self.kind in ["custom"]:
            return []
        else:
            return []

    def generate_sql_column(self, previous_str, column_name, statistics_num, statistics_varchar):
        # 1. read relevant values from statistics
        if self.kind in ["mode"]:
            new_val = statistics_varchar[column_name][0]
        elif self.kind in ["custom"]:
            new_val = self.value
        # 2. call sql generate function
        return singlecol.impute_str(previous_str, new_val=new_val)

class TryCast(Preprocessor):
    """
    A preprocessor that attempts to convert a text column to a new data type using SQL TRYCAST function.

    Parameters
    ----------
    new_type : str
        The new data type to attempt to cast the column to. Must be one of the following: 'BYTEINT', 'SMALLINT', 'INT',
        'BIGINT', 'FLOAT', 'DATE', 'TIME', 'TIMESTAMP(6)'.

    Raises
    ------
    AssertionError
        If new_type is not one of the allowed values.

    Notes
    -----
    This class inherits from the Preprocessor abstract class and implements its abstract methods.
    """
    def __init__(self, new_type="FLOAT"):
        assert(new_type in ["BYTEINT","SMALLINT", "INT", "BIGINT", "FLOAT", "DATE", "TIME", "TIMESTAMP(6)"])
        self.new_type = new_type
        self.necessary_statistics = self.define_necessary_statistics()

    def define_necessary_statistics(self):
        return []

    def generate_sql_column(self, previous_str, column_name, statistics_num, statistics_varchar):
        # call sql generate function
        return singlecol.trycast(previous_str, new_type = self.new_type)


class Scale(Preprocessor):
    """
    Scales numerical values using a chosen method (MinMax, Z-Score, RobustScaling) and parameters.

    Parameters
    ----------
    kind : str
        The scaling method to use. Supported values are "minmax", "zscore", "robust", and "custom". Formulas:

        - 'minmax': (X - MIN(X)) / (MAX(X) - MIN(X)).
        - 'zscore': (X - MEAN(X)) / STD(X).
        - 'robust': (X - P25(X)) / (P75(X) - P25(X)).
        - 'custom': (X - numerator_subtr) / denominator.

    numerator_subtr : int or float or str
        The value to subtract from each element of the data before scaling. If a string, it must be one of
        "mean", "std", "median", "mode", "max", "min", or a string formatted as "P[0-100]" for percentiles.

    denominator : int or float or str
        The value to divide each element of the data by after subtracting numerator_subtr. If a string, it must
        be a formula composed of one or two of the following: "mean", "std", "median", "mode", "max", "min",
        or a string formatted as "P[0-100]" for percentiles (e.g. "MAX-P33"). If it's a single value, it must not be 0.

    Raises
    ------
    AssertionError
        If any of the input values is invalid.

    Notes
    -----
    This class inherits from the Preprocessor abstract class and implements its abstract methods.
    """
    def __init__(self, kind="minmax", numerator_subtr=0, denominator=1):
        assert kind in ["minmax","zscore","robust","custom"]
        if kind == "custom":
            assert(isinstance(denominator,(int,float,str)))
            if isinstance(denominator,(int,float)):
                assert (denominator != 0)
            elif isinstance(denominator,str):
                denom_formula_comp = denominator.split("-")
                assert( (len(denom_formula_comp)  in [1,2] ) and
                        (all([(c in ["mean","std","median","mode","max","min"]) or _is_valid_str_percentile(c)
                              for c
                              in denom_formula_comp])))

            assert (isinstance(numerator_subtr, (int, float, str)))
            if isinstance(numerator_subtr,str):
                assert (numerator_subtr in ["mean","std","median","mode","max","min"]) or _is_valid_str_percentile(numerator_subtr)

        self.kind = kind
        self.numerator_subtr = numerator_subtr
        self.denominator = denominator
        self.necessary_statistics = self.define_necessary_statistics()

    def define_necessary_statistics(self):
        if self.kind in ["minmax","zscore"]:
            return ["standard"]
        elif self.kind in ["robust"]:
            return ["median",("P",25), ("P",75) ]
        elif self.kind in ["custom"]:
            stats = []
            if isinstance(self.numerator_subtr, str):
                if _is_valid_str_percentile(self.numerator_subtr):
                    stats += [("P",int(self.numerator_subtr[1:]))]
                elif self.numerator_subtr in ["median"]:
                    stats += ["median"]
            if isinstance(self.denominator, str):
                denom_formula_comp = self.denominator.split("-")
                for comp in denom_formula_comp:
                    if _is_valid_str_percentile(comp):
                        stats += [("P",int(comp[1:]))]
                    elif comp in ["median"]:
                        stats += ["median"]
            return stats
        else:
            return []

    def generate_sql_column(self, previous_str, column_name, statistics_num, statistics_varchar):
        ["minmax", "zscore", "robust", "custom"]

        # 1. read relevant values from statistics
        if self.kind in ["minmax"]:
            numerator_subtr = _get_val_statistics(statistics_num, column_name, "min")
            denominator = _get_val_statistics(statistics_num, column_name, "max") - numerator_subtr
        elif self.kind in ["zscore"]:
            numerator_subtr = _get_val_statistics(statistics_num, column_name, "mean")
            denominator = _get_val_statistics(statistics_num, column_name, "std")
        elif self.kind in ["robust"]:
            numerator_subtr = _get_val_statistics(statistics_num, column_name, "PERCENTILE25") # TODO check how column is named in output
            denominator = _get_val_statistics(statistics_num, column_name, "PERCENTILE75") - numerator_subtr # TODO check how column is named in output
        elif self.kind in ["custom"]:
            if isinstance(self.numerator_subtr, str):
                if _is_valid_str_percentile(self.numerator_subtr):
                    numerator_subtr = _get_val_statistics(statistics_num, column_name, "PERCENTILE"+self.numerator_subtr[1:]) # TODO check how column is named in output
                elif self.numerator_subtr in ["median"]:
                    numerator_subtr = _get_val_statistics(statistics_num, column_name, "median")
            else:
                numerator_subtr = self.numerator_subtr

            if isinstance(self.denominator, str):
                denom_formula_comp = self.denominator.split("-")
                comp_values = []
                for comp in denom_formula_comp:
                    if comp in ["median"]:
                        comp_values += [_get_val_statistics(statistics_num, column_name, "median")]
                    elif _is_valid_str_percentile(comp):
                        comp_values += [_get_val_statistics(statistics_num, column_name, "PERCENTILE"+comp[1:])] # TODO check how column is named in output
                if len(comp_values) == 2:
                    denominator = comp_values[1] - comp_values[0]
                else:
                    denominator = comp_values[0]
            else:
                denominator = self.denominator
        # 2. call sql generate function
        return singlecol.scale(previous_str, numerator_subtr, denominator)



class CutOff(Preprocessor):
    """
    Clips numeric values that fall outside a given range.

    Parameters
    ----------
    cutoff_min : int, float, str or None, optional
        The minimum value for the range. If None, no lower bound will be applied.
        If a string, it must be in the format 'P[0-100]' or one of the values 'mean',
        'mode', 'median' or 'min', representing a percentile or summary statistic.
    cutoff_max : int, float, str or None, optional
        The maximum value for the range. If None, no upper bound will be applied.
        If a string, it must be in the format 'P[0-100]' or one of the values 'mean',
        'mode', 'median' or 'max', representing a percentile or summary statistic.

    Raises
    ------
    AssertionError
        If both `cutoff_min` and `cutoff_max` are None, or if they are equal.
        If `cutoff_min` or `cutoff_max` is not None and is not a valid type or value.

    Notes
    -----
    Values falling outside the range will be replaced by the closest value within the range.
    If a percentile is used for `cutoff_min` or `cutoff_max`, the value will be determined
    based on the corresponding percentile in the data set.
    """

    def __init__(self, cutoff_min=None, cutoff_max=None):
        assert not((cutoff_min is None) and (cutoff_max is None))
        assert cutoff_min != cutoff_max
        if cutoff_min is not None:
            assert (isinstance(cutoff_min,(int,float) )
                    or (isinstance(cutoff_min,str) & (_is_valid_str_percentile(cutoff_min) or
                                                      (cutoff_min in ["mean","mode","median","min"])
                                                      )))
        if cutoff_max is not None:
            assert (isinstance(cutoff_max,(int,float) )
                    or (isinstance(cutoff_max,str) & (_is_valid_str_percentile(cutoff_max) or
                                                      (cutoff_max in ["mean","mode","median","max"])
                                                      )))

        self.cutoff_min = cutoff_min
        self.cutoff_max = cutoff_max
        self.necessary_statistics = self.define_necessary_statistics()

    def needs_subquery(self):
        return True

    def define_necessary_statistics(self):
        stats_ = []
        def get_stats_cutoff(cutoff_val):
            stats = []
            if cutoff_val is None:
                return []
            elif isinstance(cutoff_val,(int,float)):
                stats += []
            elif cutoff_val in ["mean","mode","min","max"]:
                stats += ["standard"]
            elif cutoff_val in ["median"]:
                stats += ["median"]
            elif _is_valid_str_percentile(cutoff_val):
                if isinstance(cutoff_val,str):
                    stats += [("P", int(cutoff_val[1:]))]
            return stats

        stats = get_stats_cutoff(self.cutoff_min) + get_stats_cutoff(self.cutoff_max)

        return stats

    def generate_sql_column(self, previous_str, column_name, statistics_num, statistics_varchar):

        # 1. read relevant values from statistics
        def get_cutoff_val(cuttof_variable,column_name, statistics_num):
            if (cuttof_variable is None) or isinstance(cuttof_variable, (float, int)):
                return cuttof_variable
            elif cuttof_variable in ["mean","mode","min","max", "median"]:
                return _get_val_statistics(statistics_num, column_name, cuttof_variable)
            elif _is_valid_str_percentile(cuttof_variable):
                return _get_val_statistics(statistics_num, column_name, "PERCENTILE"+cuttof_variable[1:])

        cutoff_min = get_cutoff_val(self.cutoff_min, column_name, statistics_num)
        cutoff_max = get_cutoff_val(self.cutoff_max, column_name, statistics_num)
        #print(previous_str, column_name, self.cutoff_min, self.cutoff_max,  cutoff_min, cutoff_max)
        # 2. call sql generate function
        return singlecol.cutoff(previous_str, cutoff_min, cutoff_max)

class FixedWidthBinning(Preprocessor):
    """
    Performs fixed-width binning on a numerical column.

    Parameters
    ----------
    n_bins: int
        The number of bins to divide the data into. Must be greater than 1. bins range from 0 to n_bins-1
    lower_bound: float or None, default=None
        The lower bound of the binning range. If None, the minimum value in the data is used.
    upper_bound: float or None, default=None
        The upper bound of the binning range. If None, the maximum value in the data is used.

    Raises
    ------
    AssertionError:
        If n_bins is not an integer or is not greater than 1.
        If lower_bound is not None or a float/int.
        If upper_bound is not None or a float/int.

    Notes
    -----
    This preprocessor creates bins of fixed width for numerical data. The data is divided into n_bins
    equally sized intervals in the range defined by lower_bound and upper_bound. If these values are not
    provided, the minimum and maximum values of the data are used as bounds.
    """

    def __init__(self, n_bins=5, lower_bound=None, upper_bound=None):
        assert isinstance(n_bins, int)
        assert n_bins > 1
        assert (lower_bound is None) or isinstance(lower_bound, (float,int))
        assert (upper_bound is None) or isinstance(upper_bound, (float, int))

        self.n_bins = n_bins
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.necessary_statistics = self.define_necessary_statistics()

    def define_necessary_statistics(self):
        if isinstance(self.lower_bound, (float,int)) & isinstance(self.upper_bound, (float,int)):
            return []
        else:
            return ["standard"]

    def generate_sql_column(self, previous_str, column_name, statistics_num, statistics_varchar):
        # 1. read relevant values from statistics
        if self.lower_bound is None:
            c_min = _get_val_statistics(statistics_num, column_name, "min")
        else:
            c_min = self.lower_bound

        if self.upper_bound is None:
            c_max = _get_val_statistics(statistics_num, column_name, "max")
        else:
            c_max = self.upper_bound

        # 2. call sql generate function
        return singlecol.fixed_width_binning(previous_str, self.n_bins, c_max, c_min)


class ThresholdBinarizer(Preprocessor):
    """
    Binarizes numeric data using a threshold value.

    Parameters
    ----------
    threshold : int, float or str, optional
        The threshold used for binarization. If a string, it can be one of "mean", "mode", "median" or a percentile
        string in the format of "P[1-100]", e.g "P33". Default is "mean".

    Notes
    -----
    If a value is greater than the threshold, the output is 1, else 0.
    """
    def __init__(self, threshold="mean"):
        if isinstance(threshold,str):
            assert (threshold in ["mean","mode","median"]) or _is_valid_str_percentile(threshold)
        else:
            assert isinstance(threshold,(int,float))
        self.threshold = threshold
        self.necessary_statistics = self.define_necessary_statistics()

    def define_necessary_statistics(self):
        if isinstance(self.threshold,(int,float)):
            return []
        elif self.threshold in ["median"]:
            return ["median"]
        elif self.threshold in ["mean", "mode"]:
            return ["standard"]
        elif _is_valid_str_percentile(self.threshold):
            return [("P", int(self.threshold[1:]))]
        else:
            return []

    def generate_sql_column(self, previous_str, column_name, statistics_num, statistics_varchar):
        # 1. read relevant values from statistics
        if isinstance(self.threshold,(int,float)):
            threshold = self.threshold
        elif self.threshold in ["mean","mode","median"]:
            threshold = _get_val_statistics(statistics_num, column_name, self.threshold)
        elif _is_valid_str_percentile(self.threshold):
            threshold = _get_val_statistics(statistics_num, column_name, "PERCENTILE"+self.threshold[1:])

        # 2. call sql generate function
        return singlecol.threshold_binarizer(previous_str, threshold)



class ListBinarizer(Preprocessor):
    """
    Preprocessor for text columns that outputs 1 if the value is in a given list or among the K most frequent values.

    Parameters
    ----------
    elements1 : str or list of str
        The list of elements to binarize or the top K most frequent values, indicated by "TOPK", e.g. "TOP3" or "TOP10".

    """

    def __init__(self, elements1="TOP3"):
        if isinstance(elements1,list):
            assert(all([isinstance(c, str) for c in elements1]))
        else:
            assert _is_valid_str_top(elements1)

        self.elements1 = elements1
        self.necessary_statistics = self.define_necessary_statistics()

    def define_necessary_statistics(self):
        if isinstance(self.elements1,list):
            return []
        elif _is_valid_str_top(self.elements1):
            return [("TOP", int(self.elements1[3:]))]
        else:
            return []

    def generate_sql_column(self, previous_str, column_name, statistics_num, statistics_varchar):

        # 1. read relevant values from statistics
        if isinstance(self.elements1,list):
            classes_1 = self.elements1
        else:
            classes_1 = statistics_varchar[column_name][:int(self.elements1[3:])]

        # 2. call sql generate function
        return singlecol.list_binarizer(previous_str, classes_1)

class VariableWidthBinning(Preprocessor):
    """
    Binning numerical data into variable-width bins.

    Binning can be performed in two ways:
        - 'quantiles': bin data into no_quantiles number of bins based on percentiles.
        - 'custom': bin data based on custom boundaries provided by the user.

    Parameters:
    -----------
    kind : str, default 'quantiles'
        Method of binning. Valid options: 'quantiles', 'custom'.
    no_quantiles : int, default 5
        Number of bins to use when kind='quantiles'.
        Valid values are between 2 and 100.
    boundaries : list of floats or ints, default None
        Boundaries to use when kind='custom'. Must be sorted in ascending order.

    Raises:
    -------
    ValueError:
        If kind is not 'quantiles' or 'custom', or if no_quantiles is not an integer
        between 2 and 100, or if boundaries is not a list of floats or ints sorted
        in ascending order.

    """
    def __init__(self, kind="quantiles", no_quantiles=5, boundaries=None):
        assert kind in ["quantiles","custom"]
        if kind == "quantiles":
            assert isinstance(no_quantiles,int)
            assert 2 <= no_quantiles <= 100
        if kind == "custom":
            assert isinstance(boundaries, list)
            assert all(isinstance(val, (int,float)) for val in boundaries)
            #check if list is sorted

            assert all(boundaries[i] < boundaries[i+1] for i in range(len(boundaries) - 1)), "boundaries list not sorted"

        self.kind = kind
        self.no_quantiles = no_quantiles
        self.boundaries = boundaries
        self.necessary_statistics = self.define_necessary_statistics()

    def define_necessary_statistics(self):
        if self.kind in ["custom"]:
            return []
        elif self.kind in ["quantiles"]:
            step = 100.0/self.no_quantiles
            quantiles = [int(step*i) for i in range(1,self.no_quantiles)]
            return [("P", q) for q in quantiles]
        else:
            return []

    def needs_subquery(self):
        return True

    def generate_sql_column(self, previous_str, column_name, statistics_num, statistics_varchar):
        bin_boundaries = []
        # 1. read relevant values from statistics
        if self.kind in ["custom"]:
            bin_boundaries = self.boundaries
        elif self.kind in ["quantiles"]:
            step = 100.0/self.no_quantiles
            quantiles = [int(step*i) for i in range(1,self.no_quantiles)]
            for qu in quantiles:
                bin_boundaries.append(_get_val_statistics(statistics_num, column_name, "PERCENTILE" + str(qu)))

        # 2. call sql generate function
        return singlecol.variable_width_binning(previous_str, bin_boundaries)

class LabelEncoder(Preprocessor):
    """
    Encodes a text column into numerical values using a label encoding scheme.

    The encoding can be based on the K most frequent values, as defined by a TOPK value,
    or on a custom list of elements.

    Parameters:
    -----------
    elements: list or str
        If a list, contains the custom elements to use for encoding the column. If a string, should be a valid TOPK
        specifier, indicating that the K most frequent elements should be used. E.g. "TOP20"

    Raises:
    -------
    AssertionError:
        If the `elements` parameter is not a list or a valid TOPK specifier. If `elements` is a list, raises an
        AssertionError if it contains non-string elements.
    """
    def __init__(self, elements="TOP100"):
        assert isinstance(elements, list) or isinstance(elements, str)
        if isinstance(elements, list):
            assert (all([isinstance(val, str) for val in elements]))
        if isinstance(elements, str):
            assert(_is_valid_str_top(elements))

        self.elements = elements
        self.necessary_statistics = self.define_necessary_statistics()

    def define_necessary_statistics(self):
        if isinstance(self.elements, list):
            return []
        elif isinstance(self.elements, str):
            return [("TOP", int(self.elements[3:]))]
        else:
            return []

    def generate_sql_column(self, previous_str, column_name, statistics_num, statistics_varchar):
        classes = []
        # 1. read relevant values from statistics
        if isinstance(self.elements,list):
            classes = self.elements
        elif _is_valid_str_top(self.elements):
            classes = statistics_varchar[column_name][:int(self.elements[3:])]

        # 2. call sql generate function
        return singlecol.label_encoder(previous_str, classes)

class CustomTransformer(Preprocessor):
    """
    A custom transformer that applies a custom SQL expression to a column.

    Parameters:
    -----------
        custom_str (str): A custom SQL expression that contains the string "%%COL%%"
            where the column name should be inserted.
            For example: " 2 * POWER(%%COL%%) + 3 * %%COL%% "

    Raises:
    -------
        AssertionError: If `custom_str` is not a string or does not contain "%%COL%%".

    """

    def __init__(self, custom_str):
        assert isinstance(custom_str,str)
        assert "%%COL%%" in custom_str

        self.custom_str = custom_str
        self.necessary_statistics = self.define_necessary_statistics()

    def define_necessary_statistics(self):
        return []

    def needs_subquery(self):
        return True


    def generate_sql_column(self, previous_str, column_name, statistics_num, statistics_varchar):
        # 2. call sql generate function
        return singlecol.custom_transformation(previous_str,
                                               self.custom_str)
