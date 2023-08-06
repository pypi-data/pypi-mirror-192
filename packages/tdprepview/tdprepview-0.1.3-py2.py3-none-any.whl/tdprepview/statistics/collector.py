import pandas as pd
import teradataml as tdml
from numpy import dtype

def get_numeric_statistics(DF:tdml.DataFrame, cols_standard, cols_median_percentile, centiles)  -> pd.DataFrame:
    #print(cols_standard, cols_median_percentile, centiles)
    res_df = pd.DataFrame({'ATTRIBUTE': pd.Series(dtype=dtype('O')),
                       'StatName': pd.Series(dtype=dtype('O')),
                       'StatValue': pd.Series(dtype=dtype('float64'))})

    if (cols_standard is not None) and len(cols_standard)>0:
        df_stats1 = tdml.UnivariateStatistics(
            newdata = DF,
            target_columns=cols_standard,
            stats=["MEAN","MAX","MIN","MODE","STD"]
            ).result.to_pandas()
        res_df = pd.concat([res_df, df_stats1])

    if (cols_median_percentile is not None) and len(cols_median_percentile)>0:
        if centiles == []:
            centiles = [50]
        df_stats2 = tdml.UnivariateStatistics(
            newdata=DF,
            target_columns=cols_median_percentile,
            stats=["MEAN","MAX","MIN","MODE","STD", "MEDIAN", "PERCENTILES"],
            centiles=centiles,
            ).result.to_pandas()
        res_df = pd.concat([res_df, df_stats2])

    return res_df


def get_varchar_statistics(DF:tdml.DataFrame, col_maxtop_dict:dict)  -> dict:

    if col_maxtop_dict == {}:
        # no statistics needed
        return {}

    DF._DataFrame__execute_node_and_set_table_name(DF._nodeid, DF._metaexpr)
    view_name = DF._table_name

    where_ = "\t\n\tOR\n\t".join([
        f"((ColumnName = '{colname}') AND DistinctValueCountRank <= {colcount})"
        for colname, colcount in col_maxtop_dict.items()
    ])
    target_cols = ",".join("'"+c+"'" for c in col_maxtop_dict.keys())

    query = f"""
    SELECT
        dt.*,
        RANK() OVER ( PARTITION BY ColumnName ORDER BY DistinctValueCount DESC) AS DistinctValueCountRank
    FROM ( SELECT * 
           FROM
                TD_CategoricalSummary (
                  ON {view_name} AS InputTable
                  USING
                  TargetColumns ({target_cols})
                ) AS dt
           WHERE DistinctValue IS NOT NULL
        ) AS dt
    QUALIFY
     (
        {where_}
     )
    """
    #print(query)
    df_res = tdml.DataFrame.from_query(query).to_pandas()

    return df_res.groupby('ColumnName')['DistinctValue'].apply(list).to_dict()
