"""分析の前処理で必ずと言っていいほど行う
「フォルダをglobで括る > forで一個ずつread_csvしていく > concatですべてのDataFrameを結合する > 変数の選択とリネーム」
を行う関数。
引数にはデータが格納されているフォルダの絶対パスと使用する変数と変更後の変数名との辞書が必須。
"""
import glob
import pandas as pd


def get_file_path_list(folder_path: str, extension=None) -> list:
    """指定されたフォルダから、ファイルのパスをまとめて取得する。
    extensionで拡張子を指定できる（現在はcsvのみに対応）。

    Returns:
        list: fileパスが要素のリスト
    """
    file_path_list = glob.glob(f"{folder_path}\\*{extension}")
    return file_path_list


def choose_var_to_use(df: pd.DataFrame, dict_var_to_use: dict) -> pd.DataFrame:
    """使用する変数を選択する。

    Args:
        df (pd.DataFrame): 読み込んだDataFrame
        dict_var_to_use (dict): 使用する変数と変換する名前を含んだ辞書

    Returns:
        pd.DataFrame: 使用する変数のみを抽出したDataFrame
    """
    df = df[dict_var_to_use.keys()]
    return df


def rename_var_to_use(df: pd.DataFrame, dict_var_to_use: dict) -> pd.DataFrame:
    """変数名を辞書で指定したものに変換する。

    Args:
        df (pd.DataFrame): 読み込んだDataFrame
        dict_var_to_use (dict): 使用する変数と変換する名前を含んだ辞書

    Returns:
        pd.DataFrame: 変数名を変更したDataFrame
    """
    df.rename(columns=dict_var_to_use, inplace=True)
    return df


def main(folder_path: str, dict_var_to_use: dict, extension: str=".csv", encoding: str="cp932") -> pd.DataFrame:
    """フォルダ内のcsvファイルを読み込み、それらを結合する。
    また、変数の選択と変数名の変換も行う。

    Args:
        folder_path (str): データが格納されているフォルダのパス
        dict_var_to_use (dict): 使用する変数と変換する名前を含んだ辞書
        extension (str): データの拡張子. Defaults to ".csv".
        encoding (str): pd.read_csvのエンコードタイプ. Defaults to "cp932".

    Returns:
        pd.DataFrame: 処理済みのDataFrame
    """
    df_01 = pd.concat(pd.read_csv(file_path, encoding=encoding) for file_path in get_file_path_list(folder_path, extension=extension))
    df_02 = choose_var_to_use(df_01, dict_var_to_use)
    df_03 = rename_var_to_use(df_02, dict_var_to_use)
    df_04 = df_03.reset_index(drop=True)
    return df_04