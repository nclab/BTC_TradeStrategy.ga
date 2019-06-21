
import pickle

def _fitness():
    P = list(data['收盤價'])
    RSI = list(data['RSI6'])
    profit = 0
    buy_index = 0

    
    while buy_index < len(data):
        if RSI[buy_index] < 20:
            for sell_index in range(buy_index+1,len(data)):
                if RSI[sell_index] > 80:
                    profit += 0.999*P[sell_index] - 1.001*P[buy_index]
                    buy_index = sell_index  
                    break
            if sell_index == len(data)-1: break
        buy_index+=1
    
    return profit
  
    

def test(file_name):
    global data
    with open(r'{}.pickle'.format(file_name),'rb') as file:
        data = pickle.load(file)
    
    print('-------------------------------------')
    print('測資：',file_name)
    print('獲利USDT：',_fitness())
    print('-------------------------------------')
    with open(r'{}.txt'.format(exp_name),'a') as file:
        file.write('測資：{}\t獲利USDT：{}\n'.format(file_name,_fitness()))
    return _fitness()
        
date = ['2017-9','2017-10','2017-11','2017-12',
           '2018-1','2018-2','2018-3','2018-4','2018-5','2018-6','2018-7','2018-8','2018-9','2018-10','2018-11','2018-12',
           '2019-1']

exp_name = '常用交易策略RSI'
exp ='''
--------------
BUY : RSI < 20
SELL: RSI > 80
--------------
'''
with open(r'{}.txt'.format(exp_name),'a') as file:
    file.write(exp)
        
total_profit = 0

for t in range(1,len(date)):
    total_profit += test(date[t])
with open(r'{}.txt'.format(exp_name),'a') as file:
    file.write('總獲利:{}\n----------------------------------------------------------------\n'.format(total_profit))
    

