import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.metrics import log_loss
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

# [その他のimport文]
MODEL_PATH = 'OVF_model.json'  # モデルの保存先・読み込み先のパス

def train_and_save_model():
    df = pd.read_excel(r'C:\Users\takah\OneDrive\PythonFile\Sample\OVF_ML.xlsx')
    
    # 前処理
    df["BMI"] = df["Weight"] / (df["Height"] / 100 * df["Height"] / 100)
    df["Anteratio0"] = 200 * df["AnteFra0"] / (df["AnteUp0"] + df["AnteDown0"])
    
    df.dropna(subset=["Nonunion"], inplace=True)

    df.loc[(df["LevelN"] > 0) & (df["LevelN"] <= 10), "Level3"] = 1
    df.loc[(df["LevelN"] > 10) & (df["LevelN"] <= 14), "Level3"] = 2
    df.loc[df["LevelN"] > 14, "Level3"] = 3
    
    df.loc[(df["T20"] >= 2) & (df["T20"] <= 3), "T203"] = 1
    df.loc[df["T20"] == 1, "T203"] = 2
    df.loc[df["T20"] == 4, "T203"] = 3
    
    df.loc[df["Poste0"] == 0, "Poste02"] = 0
    df.loc[(df["Poste0"] >= 1) & (df["Poste0"] <= 5), "Poste02"] = 1

    df["Nonunion2"] = np.where(df["Nonunion"] >= 1, "1", "0")

    # 不要な列を削除
    columns_to_drop = ["T20", "Study", "iid", "LevelN", "Nonunion", "KypExt0", "MedicOP10",
                       "AdjVF", "AnteFra0", "AnteUp0", "AnteDown0", "T1PostRis0", "Height",
                       "Weight", "Smoke", "steroid", "T10", "OldVF", "Poste0", "YAM", "BMI", "Anteratio0"]
    df.drop(columns=columns_to_drop, inplace=True)

    df["Nonunion2"] = df["Nonunion2"].astype(str).replace({'1': 1, '0': 0})


    # カテゴリ変数のOne Hot Encoding
    df = pd.get_dummies(df, columns=['sex', 'Level3', 'T203', 'Poste02'], drop_first=True)
    
    X = df.drop('Nonunion2', axis=1)
    y = df['Nonunion2']
    
    # データの分割
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # モデルの訓練
    model = XGBClassifier()
    model.fit(X_train, y_train)
    
    # モデルの評価（Log Loss）
    y_pred_proba = model.predict_proba(X_test)
    loss = log_loss(y_test, y_pred_proba)
    print(f"Log Loss: {loss:.4f}")
    
    # モデルの保存
    model.save_model(MODEL_PATH)

def predict(data):
    # モデルのロード
    model = XGBClassifier()
    model.load_model(MODEL_PATH)
    
    # 予測の実行
    pred_proba = model.predict_proba(np.array(data).reshape(1, -1))
    print(pred_proba[0][1]) 
    return pred_proba[0][1]  # クラス1の予測確率を返す

# スクリプトとして実行された場合のみ、モデルの訓練と保存を実行
if __name__ == '__main__':
    train_and_save_model()