# BTC_TradeStrategy.ga

Source code “On the generation of Bitcoin trading strategies by using genetic algorithms”.


## 程式環境

Windows 10 + Python3 + Spyder (官方Python3 IDLE也行)


## Required Libraries

1. numpy
2. pandas
3. pickle


## 檔案說明及使用方法

#### GA交易策略.py: 本研究 GA 訓練及測試代碼

1. 打開 Command Prompt
2. 輸入
> python GA交易策略.py
3. 程式將會開始訓練並進行模擬交易，待程式執行完畢後即完成一次實驗
4. 實驗結果將產生於同目錄下，檔名: **GA交易策略.txt**

※ 本研究 GA 獲利是以 30 次實驗平均值作為交易策略的整體績效<br />
※ 理想交易策略實驗也是透過此代碼實現，差別僅在於測試期及訓練期需調整為同一時間


#### 常用交易策略 (以 K 為例)

1. 打開 Command Prompt
2. 輸入
> python 常用交易策略-K指標.py
3. 實驗結果將產生於同目錄下，檔名: **常用交易策略-K指標.txt**

#### 歷史交易資料

.pickle 檔案為比特幣歷史交易資料
