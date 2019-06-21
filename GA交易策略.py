import pickle
import numpy as np

def _fitness(ind):
    K_threshold,D_threshold,RSI_threshold,V,E = ind
    _10VOL = list(data['10VOL'])
    _10EMA = list(data['10EMA'])
    VOL = list(data['成交量'])
    P = list(data['收盤價'])
    RSI = list(data['RSI6'])
    K = list(data['K'])
    D = list(data['D'])

    #獲利初始為0
    profit = 0
    buy_index = 0

    
    while buy_index < len(data):
        if RSI[buy_index] > RSI_threshold and K[buy_index] > K_threshold and D[buy_index] > D_threshold and P[buy_index] > E*_10EMA[buy_index] and VOL[buy_index] > V*_10VOL[buy_index]:
            for sell_index in range(buy_index+1,len(data)):
                if RSI[sell_index] < RSI_threshold and K[sell_index] < K_threshold and D[sell_index] < D_threshold:
                    profit += 0.999*P[sell_index] - 1.001*P[buy_index]
                    buy_index = sell_index  
                    break
            if sell_index == len(data)-1: break
        buy_index+=1
    
    return profit
  
    
def select(pop, fitness):
    idx = np.random.choice(np.argsort(fitness)[-20:], size=POP_SIZE)
    return pop[idx]


# mating process (genes crossover)
def crossover(parent, pop):     
    if np.random.rand() < CROSS_RATE:
        #從母體中任選一條染色體                               
        i_ = np.random.randint(0, POP_SIZE, size=1)       
        #產生交配點                      
        cross_points = np.random.randint(0, 2, size=DNA_SIZE).astype(np.bool)
        #交配點上數值互換
        parent[cross_points] = pop[i_, cross_points]
    
    #回傳交配完之染色體
    return parent


def mutate(parent):
    for point in range(DNA_SIZE):
        if np.random.rand() < MUTATION_RATE :
            if point <= 2:
                #K、D、RSI突變
                parent[point] = round(np.random.uniform(0,100),2)
            elif point == 3:
                #VMA突變
                parent[point] = round(np.random.uniform(1,10),5)
            else:
                #MA突變
                parent[point] = round(np.random.uniform(1,1.1),5)
                
    #回傳突變完之染色體
    return parent

def train(file_name):
    global data
    with open(r'{}.pickle'.format(file_name),'rb') as file:
        data = pickle.load(file)
    pop = np.random.uniform(0,100,(POP_SIZE,DNA_SIZE)).round(2)
    pop[:,3] = np.random.uniform(1,10,POP_SIZE).round(5)
    pop[:,4] = np.random.uniform(1,1.1,POP_SIZE).round(5)
    
    fitness = np.array([_fitness(ind)for ind in pop])
    
    for _ in range(N_GENERATIONS):
    #GA part (evolution)

        pop_copy = pop.copy()
        for parent in pop:
            child = crossover(parent, pop_copy)
            child = mutate(child)
            parent[:] = child       # parent is replaced by its child
            
        pop = select(pop, fitness) #從pop中挑適應值好的個體 取代pop
        
        fitness = np.array([_fitness(ind)for ind in pop])

        print("Generation  %d: "%(_+1), pop[np.argmax(fitness), :],fitness[np.argmax(fitness)])            

    return pop[np.argmax(fitness), :]
          
def test(solution,file_name):
    global data
    with open(r'{}.pickle'.format(file_name),'rb') as file:
        data = pickle.load(file)
    
    print('-------------------------------------')
    print('測資：',file_name)
    print('策略：',solution)
    print('獲利USDT：',_fitness(solution))
    print('-------------------------------------')
    with open(r'{}.txt'.format(exp_name),'a') as file:
        file.write('測資：{}\t策略：{}\t獲利USDT：{}\n'.format(file_name,solution,_fitness(solution)))
    return _fitness(solution)
        
date = ['2017-9','2017-10','2017-11','2017-12',
           '2018-1','2018-2','2018-3','2018-4','2018-5','2018-6','2018-7','2018-8','2018-9','2018-10','2018-11','2018-12',
           '2019-1']

#產生實驗文件txt
exp_name = 'GA交易策略'
#實驗內容
exp ='''
------------------------------------
訓練2017-9~2018-12 測試2017-10~2019-1
------------------------------------
'''


DNA_SIZE = 5             # DNA length
POP_SIZE = 100      # population size
CROSS_RATE = 0.5        # mating probability (DNA crossover)
MUTATION_RATE = 0.2    # mutation probability
N_GENERATIONS = 50
np.set_printoptions(suppress=True) #array不顯示科學記號

with open(r'{}.txt'.format(exp_name),'a') as file:
    file.write(exp)

#針對單一月份進行訓練
'''
profit = test(train('2017-9'),'2017-10') #訓練2017/9 --> 產生交易策略 --> 2017/10進行模擬交易
profit = test(train('2017-10'),'2017-11') #訓練2017/10 --> 產生交易策略 --> 2017/11進行模擬交易
print(profit)
'''

#訓練2017-9~2018-12 測試2017-10~2019-1
total_profit = 0
for t in range(1,len(date)):
    total_profit += test(train(date[t-1]),date[t])
with open(r'/Users/rex/Desktop/Binance/{}.txt'.format(exp_name),'a') as file:
    file.write('總獲利:{}\n----------------------------------------------------------------\n'.format(total_profit))
    

