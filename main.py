import numpy as np
import random
%tensorflow_version 1.14.0
import tensorflow as tf
import os
import keras
from keras.callbacks import LearningRateScheduler
from tensorflow.keras.models import load_model
from keras.models import Sequential, Model
from keras.layers import Dense, Lambda, Input, Concatenate
from keras.optimizers import *
from keras import backend as K
from past.builtins import xrange
from matplotlib import pyplot as plt
from google.colab import drive
drive.mount('/content/drive')
#import pygame
import operator
import time
import pandas as pd 
from tensorflow.python.client import device_lib
from collections import deque
import datetime, os
from copy import deepcopy
start_time = time.time()
#np.random.seed(0)
MAX_EPSILON=1
MIN_EPSILON=0
MIN_EPSILON_STEADY=0.01
MIN_BETA = 0.4
MAX_BETA = 1.0
HUBER_LOSS_DELTA = 1.0

test=0
expl_finished=1

mem_model = 'PER'

grid_size=50
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
STAY = 4
A = [UP, DOWN, LEFT, RIGHT, STAY]
A_DIFF = [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]
agents_number=4
number_of_walls=grid_size+1
depth=3
DIMENSIONS=2

def  ConnectButton():
    console.log("Connect pushed"); 
    document.querySelector("#top-toolbar > colab-connect-button").shadowRoot.querySelector("#connect").click() 

def localization(pos,array_map):    
    locality_map=np.zeros([agents_number,3,3])
    array=np.zeros([agents_number,DIMENSIONS*2+9])
    #print("initial",locality_map) 
    #print("pos",pos)
    counter=-1
    #print("pos!",pos)
    # for j in range(0,1):
    for i in pos:
        counter=counter+1
        flag=0 
        #print("iiiiii",i)
        #print("1",i[0])
        a=i[0]
        b=i[1]
        #print("2",i[1])
        #print(counter)                  ######### checking corners     ##########
        
        if((a==0 and b==0)  or (a==0 and b==grid_size-1)  or (a==grid_size-1 and b==0)  
           or (a==grid_size-1 and b==grid_size-1)):
            flag=1
            if(a==0 and b==0):
                locality_map[counter][0]=1
                locality_map[counter][:,0]=1
                locality_map[counter][1][1]=array_map[i[0]][i[1]]
                locality_map[counter][1][2]=array_map[0][1]
                locality_map[counter][2][1]=array_map[1][0]
                locality_map[counter][2][2]=array_map[1][1]
            if(a==0 and b==grid_size-1):
                locality_map[counter][0]=1
                locality_map[counter][:,2]=1
                locality_map[counter][1][1]=array_map[i[0]][i[1]]
                locality_map[counter][1][0]=array_map[0][grid_size-2]
                locality_map[counter][2][1]=array_map[1][grid_size-1]
                locality_map[counter][2][0]=array_map[1][grid_size-2]
            if(a==grid_size-1 and b==0):
                locality_map[counter][2]=1
                locality_map[counter][:,0]=1
                locality_map[counter][1][1]=array_map[i[0]][i[1]]
                locality_map[counter][0][1]=array_map[grid_size-2][0]
                locality_map[counter][1][2]=array_map[grid_size-1][1]
                locality_map[counter][0][2]=array_map[grid_size-2][1]
            if(a==grid_size-1 and b==grid_size-1):
                locality_map[counter][2]=1
                locality_map[counter][:,2]=1
                locality_map[counter][1][1]=array_map[i[0]][i[1]]
                locality_map[counter][1][1]=array_map[i[0]][i[1]]
                locality_map[counter][0][0]=array_map[grid_size-2][grid_size-2]
                locality_map[counter][1][0]=array_map[grid_size-1][grid_size-2]
                locality_map[counter][0][1]=array_map[grid_size-2][grid_size-1]

                
                
        else:
            #print("no corners!")    
            if (a==0 ):
                flag=1
                locality_map[counter][0]=1
                locality_map[counter][1][1]=array_map[i[0]][i[1]]
                locality_map[counter][1][0]=array_map[i[0]][i[1]-1]
                locality_map[counter][1][2]=array_map[i[0]][i[1]+1]
                locality_map[counter][2][0]=array_map[i[0]+1][i[1]-1]
                locality_map[counter][2][1]=array_map[i[0]+1][i[1]]
                locality_map[counter][2][2]=array_map[i[0]+1][i[1]+1]
                
            if(a==grid_size-1):
                flag=1
                locality_map[counter][2]=1
                locality_map[counter][1][1]=array_map[i[0]][i[1]]
                locality_map[counter][1][0]=array_map[i[0]][i[1]-1]
                locality_map[counter][1][2]=array_map[i[0]][i[1]+1]
                locality_map[counter][0][0]=array_map[i[0]-1][i[1]-1]
                locality_map[counter][0][1]=array_map[i[0]-1][i[1]]
                locality_map[counter][0][2]=array_map[i[0]-1][i[1]+1]
                
            if(b==0):
                flag=1
                locality_map[counter][:,0]=1
                locality_map[counter][1][1]=array_map[i[0]][i[1]]
                locality_map[counter][0][1]=array_map[i[0]-1][i[1]]
                locality_map[counter][2][1]=array_map[i[0]+1][i[1]]
                locality_map[counter][0][2]=array_map[i[0]-1][i[1]+1]
                locality_map[counter][1][2]=array_map[i[0]][i[1]+1]
            
                
            if(b==grid_size-1):
                flag=1
                locality_map[counter][:,2]=1
                locality_map[counter][:,0]=1
                locality_map[counter][1][1]=array_map[i[0]][i[1]]
                locality_map[counter][0][1]=array_map[i[0]-1][i[1]]
                locality_map[counter][2][1]=array_map[i[0]+1][i[1]]
                locality_map[counter][0][0]=array_map[i[0]-1][i[1]-1]
                locality_map[counter][1][0]=array_map[i[0]][i[1]-1]
                locality_map[counter][2][0]=array_map[i[0]+1][i[1]-1]
        if(flag==0):
            locality_map[counter][1][1]=array_map[i[0]][i[1]]
            locality_map[counter][0][0]=array_map[i[0]-1][i[1]-1]
            locality_map[counter][0][1]=array_map[i[0]-1][i[1]]
            locality_map[counter][0][2]=array_map[i[0]-1][i[1]+1]
            locality_map[counter][1][0]=array_map[i[0]][i[1]-1]
            locality_map[counter][1][2]=array_map[i[0]][i[1]+1]
            locality_map[counter][2][0]=array_map[i[0]+1][i[1]-1]
            locality_map[counter][2][1]=array_map[i[0]+1][i[1]]
            locality_map[counter][2][2]=array_map[i[0]+1][i[1]+1]
            
        # state=locality_map[counterx]
        #state.flatten()         
   # print(locality_map)
    #print(pos)
    #temp=locality_map.flatten()
    #pos=np.array(pos)
    #print(pos.flatten())
    #temp2=pos.flatten()
    #state=np.append(temp,temp2)
    #state=locality_map
    
    for i in range(0,agents_number):
        temp=[]
        if(i!=agents_number-1):
            temp.append(pos[i])
            temp.append(pos[i+1])
        else:
            temp.append(pos[i])
            temp.append(pos[0])
        #print("temp",temp)
        array[i]=np.append(locality_map[i].flatten(),temp)
        #print("locality_map!!!!",array[i])
    #print("array",array)
    state=array
    #print("loc_state",state)
    return state



def initializer():
    identify_map=np.zeros([grid_size,grid_size])-1

    array_map=np.zeros([grid_size,grid_size])-1
    positions = np.random.choice(grid_size, size=(number_of_walls,2),)
    #print("positions",positions)
    for i in positions:
        identify_map[i[0]][i[1]]=0
        array_map[i[0]][i[1]]=1

    t1=grid_size*grid_size-abs(np.sum(identify_map))
    #print("t1",t1)
    #array_map=deepcopy(identify_map)
    
    #print("identify_map",identify_map)
    #print("array_map",array_map)
    return array_map, identify_map,t1


def lr_scheduler(epoch, lr):
    
    if epoch>5:
        lr=0.00005
    else:
        lr=0.00005
    
    
    return lr




def huber_loss(y_true, y_predict):
    err = y_true - y_predict

    cond = K.abs(err) < HUBER_LOSS_DELTA
    L2 = 0.5 * K.square(err)
    L1 = HUBER_LOSS_DELTA * (K.abs(err) - 0.5 * HUBER_LOSS_DELTA)
    loss = tf.where(cond, L2, L1)

    return K.mean(loss)

class SumTree(object):

    def __init__(self, capacity):
        self.write = 0
        self.capacity = capacity
        self.tree = np.zeros(2*capacity - 1)
        self.data = np.zeros(capacity, dtype=object)

    def _propagate(self, idx, change):
        parent = (idx - 1) // 2

        self.tree[parent] += change

        if parent != 0:
            self._propagate(parent, change)

    def _retrieve(self, idx, s):
        left = 2 * idx + 1
        right = left + 1

        if left >= len(self.tree):
            return idx

        if s <= self.tree[left]:
            return self._retrieve(left, s)
        else:
            return self._retrieve(right, s-self.tree[left])

    def total(self):
        return self.tree[0]

    def add(self, p, data):
        idx = self.write + self.capacity - 1

        self.data[self.write] = data
        self.update(idx, p)

        self.write += 1
        if self.write >= self.capacity:
            self.write = 0

    def update(self, idx, p):
        change = p - self.tree[idx]

        self.tree[idx] = p
        self._propagate(idx, change)

    # def get_real_idx(self, data_idx):
    #
    #     tempIdx = data_idx - self.write
    #     if tempIdx >= 0:
    #         return tempIdx
    #     else:
    #         return tempIdx + self.capacity

    def get(self, s):
        idx = self._retrieve(0, s)
        dataIdx = idx - self.capacity + 1
        # realIdx = self.get_real_idx(dataIdx)

        return idx, self.tree[idx], self.data[dataIdx]

class Memory(object):
    e = 0.05

    def __init__(self, capacity, pr_scale):
        self.capacity = capacity
        self.memory = SumTree(self.capacity)
        self.pr_scale = pr_scale
        self.max_pr = 0

    def get_priority(self, error):
        return (error + self.e) ** self.pr_scale

    def remember(self, sample, error):
        p = self.get_priority(error)

        self_max = max(self.max_pr, p)
        self.memory.add(self_max, sample)

    def sample(self, n):
        sample_batch = []
        sample_batch_indices = []
        sample_batch_priorities = []
        num_segments = self.memory.total() / n

        for i in xrange(n):
            left = num_segments * i
            right = num_segments * (i + 1)

            s = random.uniform(left, right)
            idx, pr, data = self.memory.get(s)
            sample_batch.append((idx, data))
            sample_batch_indices.append(idx)
            sample_batch_priorities.append(pr)

        return [sample_batch, sample_batch_indices, sample_batch_priorities]

    def update(self, batch_indices, errors):
        for i in xrange(len(batch_indices)):
            p = self.get_priority(errors[i])
            self.memory.update(batch_indices[i], p)


# keras model,prediction update and save weights(for target nn)        
        
        
class Brain(object): 

    def __init__(self, state_size, action_size,  batch_size,learning_rate,number_nodes):
                                           
        self.state_size = state_size
        self.action_size = action_size
        #self.weight_backup = brain_name
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.test = test
        self.num_nodes = number_nodes
        self.optimizer_model='RMSProp'
        self.model = self._build_model()
        self.model_ = self._build_model()
        
        
        self.counter=0
      

    def _build_model(self):
         
        x = Input(shape=(self.state_size,))
        y1 = Dense(self.num_nodes, activation='relu')(x)
        y2 = Dense(self.num_nodes, activation='relu')(y1)
        y3 = Dense(self.num_nodes, activation='relu')(y2)
        y4 = Dense(self.num_nodes, activation='relu')(y3)
        y5 = Dense(self.num_nodes, activation='relu')(y4)
        y6 = Dense(self.num_nodes, activation='relu')(y5)
        z = Dense(self.action_size, activation="linear")(y6)
        model = Model(inputs=x, outputs=z)

       # optimizer = Adam(lr=self.learning_rate, clipnorm=1.)
        
       
        if self.optimizer_model == 'Adam':
            optimizer = Adam(lr=self.learning_rate, clipnorm=1.)
        elif self.optimizer_model == 'RMSProp':
            optimizer = RMSprop(lr=self.learning_rate, clipnorm=1.)
        else:
            print("smth is wrong")
        model.compile(loss=huber_loss, optimizer=optimizer)
        
    
        if self.test: 
       
            print("load!")
          
            model.load_weights('./drive/MyDrive/diplwmatikh/local_state_20x20.h5')
            model.load_weights('./drive/MyDrive/diplwmatikh/local_state_20x20.h5')
            #for layer in model.layers: print(layer.get_config(), layer.get_weights())
   
        return model
                
                

            
    def train(self, x, y,sample_weight,flag):  # x is the input to the network and y is the output
        if(flag==0):
            epochs=1
            
        if(flag==1):
            epochs=7
                
        elif(flag==2):
            epochs=8

        else:
            epochs=1
            #callbacks = [LearningRateScheduler(lr_scheduler, verbose=0)]
            self.model.fit(x, y, batch_size=len(x), sample_weight=sample_weight, epochs=epochs, verbose=0)
        


    def predict(self, state, target=False):
        if target:  # get prediction from target network
            return self.model_.predict(state)
        else:  # get prediction from local network
            return self.model.predict(state)

    def update_target_model(self):
        self.model_.set_weights(self.model.get_weights())
        #print("update")
        
        
    def predict_one_sample(self, state, target=False):                
        return self.predict(state.reshape(1,self.state_size), target=target).flatten()

    def save_model(self):
        self.model.save_weights('./drive/MyDrive/diplwmatikh/test_new')
        #print("save!")
        








#(self, state_size, action_size,  batch_size,learning_rate,test,number_nodes):


class Agent(object):
    #epsilon = MAX_EPSILON
    #beta = MIN_BETA
    
    def __init__(self, state_size, action_size, bee_index,learning_rate,memory_capacity,prioritization_scale,
                 target_frequency,
                 maximum_exploration,batch_size ): #brain_name,memory
        self.state_size = state_size
        self.action_size = action_size
        self.bee_index = bee_index
        self.memory_capacity=memory_capacity
        self.learning_rate = learning_rate
        self.gamma = 0.95
        self.brain = Brain(state_size=self.state_size, action_size=self.action_size,batch_size=64,
                           learning_rate=self.learning_rate,number_nodes=512)
        self.memory_model = mem_model 

        if mem_model == 'UER':
            self.memory = Memory(capacity=memory_capacity)
            
        elif mem_model == 'PER':
            self.memory = Memory(capacity=memory_capacity,pr_scale=prioritization_scale)

        else:
            print('Invalid memory model!')
        
        
        #self.target_type = arguments['target_type']          # wtf
        self.update_target_frequency = target_frequency
        self.max_exploration_step = maximum_exploration
        self.batch_size = batch_size
        self.step = 0
        self.test = test
        self.epsilon=MAX_EPSILON
        if self.test and expl_finished==1:
            self.epsilon = MIN_EPSILON
        

    def greedy_actor(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        else:
            return np.argmax(self.brain.predict_one_sample(state))
        
        
        


        
    def decay_epsilon(self):                          # decay epsilon algorithm
        # slowly decrease Epsilon based on our experience
        self.step += 1

        if self.test and expl_finished==1:
            self.epsilon = MIN_EPSILON
            self.beta = MAX_BETA
        else:
            if self.step < self.max_exploration_step:         
                self.epsilon = MIN_EPSILON_STEADY + (MAX_EPSILON - MIN_EPSILON_STEADY) * (self.max_exploration_step - self.step)/self.max_exploration_step
                self.beta = MAX_BETA + (MIN_BETA - MAX_BETA) * (self.max_exploration_step - self.step)/self.max_exploration_step
            else:
                self.epsilon = MIN_EPSILON
        #if(self.epsilon<0.3):
            #print(self.epsilon)
                
    def find_targets_uer(self, batch):
        batch_len = len(batch)

        states = np.array([o[0] for o in batch])
        states_ = np.array([o[3] for o in batch])

        p = self.brain.predict(states)
        p_ = self.brain.predict(states_)
        pTarget_ = self.brain.predict(states_, target=True)

        x = np.zeros((batch_len, self.state_size))
        y = np.zeros((batch_len, self.action_size))
        errors = np.zeros(batch_len)

        for i in range(batch_len):
            o = batch[i]
            s = o[0]
            a = o[1][self.bee_index]
            r = o[2]
            s_ = o[3]
            done = o[4]

            t = p[i]
            old_value = t[a]
            if done:
                t[a] = r
            else:
               
                t[a] = r + self.gamma * pTarget_[i][np.argmax(p_[i])]
               

            x[i] = s
            y[i] = t
            errors[i] = np.abs(t[a] - old_value)

        return [x, y]
    def find_targets_per(self, batch):
        batch_len = len(batch)

        states = np.array([o[1][0] for o in batch])
        states_ = np.array([o[1][3] for o in batch])

        p = self.brain.predict(states)
        p_ = self.brain.predict(states_)
        pTarget_ = self.brain.predict(states_, target=True)

        x = np.zeros((batch_len, self.state_size))
        y = np.zeros((batch_len, self.action_size))
        errors = np.zeros(batch_len)

        for i in range(batch_len):
            o = batch[i][1]
            s = o[0]
            a = o[1][self.bee_index]
            r = o[2]
            s_ = o[3]
            done = o[4]

            t = p[i]
            old_value = t[a]
            if done:
                t[a] = r
            else:
                t[a] = r + self.gamma * pTarget_[i][np.argmax(p_[i])]

            x[i] = s
            y[i] = t
            errors[i] = np.abs(t[a] - old_value)

        return [x, y, errors]
    def observe(self, sample):              
        
        if mem_model == 'UER':
            self.memory.remember(sample)

        elif mem_model == 'PER':
            _, _, errors = self.find_targets_per([[0, sample]])
            self.memory.remember(sample, errors[0])

        else:
            print('Invalid memory model!')               
                
                
    def replay(self,flag):
        
         if mem_model == 'UER':
            batch = self.memory.sample(self.batch_size)
            x, y = self.find_targets_uer(batch)
            self.brain.train(x, y,flag)
        
         else:
            [batch, batch_indices, batch_priorities] = self.memory.sample(self.batch_size)
            x, y, errors = self.find_targets_per(batch)

            normalized_batch_priorities = [float(i) / sum(batch_priorities) for i in batch_priorities]
            importance_sampling_weights = [(self.batch_size * i) ** (-1 * self.beta)
                                            for i in normalized_batch_priorities]
            normalized_importance_sampling_weights = [float(i) / max(importance_sampling_weights)
                                                        for i in importance_sampling_weights]
            sample_weights = [errors[i] * normalized_importance_sampling_weights[i] for i in xrange(len(errors))]

            self.brain.train(x, y, np.array(sample_weights),flag)

            self.memory.update(batch_indices, errors)        
        
        
    
        
    def update_target_model(self):
        if self.step % self.update_target_frequency == 0:
            self.brain.update_target_model()  
        
        
        
        
###################################################################################################################
        

class agentslandmarks:
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    STAY = 4
    A = [UP, DOWN, LEFT, RIGHT, STAY]
    A_DIFF = [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]
    
    def __init__(self, agents_number,num_landmarks,grid_size,current_path):
        self.array_map,self.wall_check,self.t1=initializer()
        #print("number of empty spaces",int(abs(np.sum(self.wall_check))))
        self.grid_size=grid_size
        
        #self.reward_mode = args['reward_mode']
        self.num_agents = agents_number
        
       
        #self.state_size = (self.num_agents + self.num_landmarks) * 2           # *3 gia 3d
        
        
        self.agents_positions = []
        self.terminal = False
        self.local=np.zeros([agents_number,3,3])
        self.test_test=5
        self.state_size=9+DIMENSIONS*2
        #self.local_state=np.zeros(self.state_size)
        self.empty_spaces=int(abs(np.sum(self.wall_check))) 
        print("state size",self.state_size)

    def reset(self):  # initialize the world
        self.array_map,self.wall_check,self.t1=initializer()
        
        #print("walls",self.wall_check)
        
       # print("starting self array",self.array_map)
        self.terminal = False
        
        self.agents_positions=[]

        for i in range(0,self.num_agents):
            flag=0
            while(flag==0):

                x=np.random.randint(self.grid_size)
                y=np.random.randint(self.grid_size)
                if(self.array_map[x][y]!=1 and self.array_map[x][y]!=0):
                    flag=1
                    self.array_map[x][y]=0
                    self.agents_positions.append([x,y])
                   # print("new position of agent to:",[x,y])
                else:
                    pass
                   # print("collision on position \n",[x,y])
        #print("\n")
        self.local_state=localization(self.agents_positions,self.array_map) 
        #print("starting_positions of agents :",self.agents_positions)
        #print("local",self.local_state)
        
        return self.local_state


    def step(self, agents_actions,current_step):
        counter=0
        counter2=0
        self.terminal=False
        # update the position of agents
        self.agents_positions,counter_wall = self.update_positions(self.agents_positions, agents_actions)
        
        for i in self.agents_positions:
            
            if(self.array_map[i]==-1 and self.wall_check[i]==-1):
                counter2=counter2+1
            self.array_map[i]=0
     
        self.local_state=localization(self.agents_positions,self.array_map)
        reward= 5* counter2-counter_wall*10-1
        

        #new_state = list(sum(self.landmarks_positions + self.agents_positions, ()))
        new_state=list(self.local_state)
        
        #print(current_step)
        #print("self.array_map",self.array_map)
        
        #print("counter wall:",counter_wall)
       # if(current_step>=74):
            #print("np.sum:",np.sum(self.array_map))
          
        return [new_state, reward, self.terminal,counter_wall,np.sum(self.array_map)]

    def update_positions(self,agents_pos,actions):
        counter=0
        positions_action_applied=[]
        pos_act_appled=[]
        #print("agents_pos before",agents_pos)
        #print("len",len(agents_pos))
        #print("actions",actions)
        agents_pos_test=np.array(agents_pos) 
        counter2=0
        for idx in xrange (len(agents_pos)):
 
            
            #print("idx",idx)
            flag=0
            
            if(actions[idx]!=4):                                                                    # allagh gia 3d case !!!
                pos_act_applied=agents_pos_test[idx]+A_DIFF[actions[idx]]
                temp=tuple(pos_act_applied)
                if(temp==agents_pos[0] or temp==agents_pos[1]):
                    #print("same spot!")
                    pos_act_applied=agents_pos[idx]
                else:
                    for i in range(0,DIMENSIONS):
                        if(pos_act_applied[i]<0):
                            pos_act_applied[i]=0
                            counter=counter+1
                        if(pos_act_applied[i]>=grid_size):
                            pos_act_applied[i]=grid_size-1
                            counter=counter+1
                    counter2=-1
                    for i in agents_pos:
                        counter2=counter+1
                        #print("iiiiiiiii",i)
                        if(i==np.array(pos_act_applied).tolist() ):
                           # print("agent collide on position",agents_pos[idx])
                            #print("np.array(pos_act_applied).tolist()",np.array(pos_act_applied).tolist())   # same position agents  
                            pos_act_applied=agents_pos[idx]
      
                    #print("aaaaa",pos_act_applied)
                    if(self.wall_check[pos_act_applied[0],pos_act_applied[1]]==0 ):                     # wall hit into the map
                        #print("wall hit on position:",agents_pos[idx])
                        counter=counter+1   
                        pos_act_applied=agents_pos[idx]
                        flag=1
                
                

                #print(type(agents_pos))


                positions_action_applied.append(tuple(pos_act_applied))
       
            else:
                positions_action_applied.append(tuple(agents_pos[idx]))
            
        
        #print(" final_pos:\n",positions_action_applied)
        #for i in positions_action_applied:
           # if()
        
        return positions_action_applied,counter
        
        
        
    def action_space(self):
        return len(self.A)
          
    def number_t1(self):
        print("dself_t1",self.t1)
        return self.t1
        
        
        
    
 #self, agents_number,grid_size, current_path):

class Environment(object):

    def __init__(self, episodes_number,episodes_testing,render,recorder,max_timestep,test,replay_steps,
                 max_random_moves,agents_number,num_landmarks,grid_size):
        current_path = os.path.abspath('')  # Where your .py file is located
        self.env = agentslandmarks(agents_number=agents_number,num_landmarks=num_landmarks, grid_size=grid_size,current_path=current_path)
        self.episodes_number = episodes_number
        self.episodes_testing=episodes_testing
        self.render = render
        self.recorder =  recorder
        self.max_ts = max_timestep
        self.test = test
        self.filling_steps = 0
        self.steps_b_updates = replay_steps
        self.max_random_moves = max_random_moves
        self.number_of_walls_t1=self.env.number_t1()
        #print("inside t1",self.number_of_walls_t1)

        self.num_agents = agents_number
        self.num_landmarks = num_landmarks
        
        self.grid_size =  grid_size
        self.max=0
        self.pos=0
        self.maxt=100
    def run(self,agents):
        

        total_step = 0
        rewards_list = []
        timesteps_list = []
        max_score = -10000
        flag2=0
        test2=1
        counter_max=0
        counter_neg=0
        counter_positive=0
        for episode_num in xrange(self.episodes_number):
            flag=0


            #if(episode_num % 100):
            #print("episode:",episode_num)
            state = self.env.reset()
            state = np.array(state)
            #state = state.ravel()

            done = False
            reward_all = 0
            time_step = 0
            
                
            while not done and time_step < self.max_ts:

                # if self.render:
                #     self.env.render()
                actions = []
                counterx=0
                for agent in agents:
                    #state_temp=locality_map
                    actions.append(agent.greedy_actor(state[counterx]))
                    counterx=counterx+1
                next_state, reward, done,wall_counter,sum_finale = self.env.step(actions,time_step)
                
                #print("actions",actions)
                
                # converting list of positions to an array
                next_state = np.array(next_state)
                #next_state = next_state.ravel()
                counterx=0
                for agent in agents:
                        
                    agent.observe((state[counterx], actions, reward, next_state[counterx], done))
                    #print("state",state[counterx])
                    if total_step >= self.filling_steps:
                        agent.decay_epsilon()
                        if time_step % self.steps_b_updates  == 0:
                            agent.replay(flag)
                        agent.update_target_model()
                    counterx=counterx+1
                total_step += 1
                time_step += 1
                state = next_state
                reward_all += reward
                #if(reward_all>0):
                    #flag=1
                    #agent.replay(flag)
            if(reward_all>0 and reward_all<self.max and episode_num!=0):
                flag=1
                agent.replay(flag)
            elif(reward_all>0 and reward_all>=self.max and episode_num!=0):
                flag=2
                agent.replay(flag)
            else:
                flag=-1
                    
                                    

            if episode_num % 100 == 0:    
                print("Episode {p}, Score: {s}, Final Step: {t}, Goal: {g}".format(p=episode_num, s=reward_all,
                                                                               t=time_step, g=done))
          
            if (self.max<=reward_all):
                self.max=reward_all
                self.pos=episode_num
                self.maxt=time_step
              
            if(reward_all<0):
                counter_neg=counter_neg+1
            if  reward_all>0:
                counter_positive=counter_positive+1
                
            if episode_num % 1 == 0:
                    
                if total_step >= self.filling_steps:
                    if reward_all >= max_score  or reward_all>0:
                        for agent in agents:
                            agent.brain.save_model()
                        max_score = reward_all
                            #print("max score",max_score)
                           # print("rewards_all",reward_all)
            if episode_num % 1000==0:
                print("max_score {m}, Best Episode: {e} , Best Final Step: {t} ".format(m=self.max,e=self.pos,t=self.maxt))
                print(" number of negative rewards {n},number of positive: {u}:".format(n=counter_neg,u=counter_positive))
                                                                                        



        ########################################## testing on the same run ############################################    
        total_step = 0
        rewards_list = []
        timesteps_list = []
        best_steps_list=[]
        cover_list=[]
        max_score = -10000
        counter_max=0
        counter_neg=0
        counter_positive=0  
        counter=0
        wall_list=[]
        available=grid_size*grid_size-self.number_of_walls_t1-agents_number
        for episode_num in xrange(self.episodes_testing):
            timesteps_list.append(episode_num)
            flag=0
            
            
    
            state = self.env.reset()
            state = np.array(state)
            #state = state.ravel()

            done = False
            reward_all = 0
            time_step = 0
            
            sum_wall=0    
            while not done and time_step < self.max_ts:
                # if self.render:
                #     self.env.render()
                actions = []
                counterx=0
                for agent in agents:
                    actions.append(agent.greedy_actor(state[counterx]))
                    counterx=counterx+1
                #actions[1]=4
                next_state, reward, done,wall_counter,sum_finale = self.env.step(actions,time_step)
                sum_wall=sum_wall+wall_counter
                #print("actions",actions)
                #print(actions[0])
                #print(actions[1])
                # converting list of positions to an array
                next_state = np.array(next_state)
                #next_state = next_state.ravel()

                

                total_step += 1
                time_step += 1
                state = next_state
                
                reward_all += reward
            
                    
                                    
            wall_list.append(sum_wall)
            if episode_num % 1 == 0:    
                print("Episode {p}, Score: {s}, Final Step: {t}, Goal: {g}".format(p=episode_num, s=reward_all,
                                                                               t=time_step, g=done))
            rewards_list.append(reward_all)
            best_steps_list.append(time_step)

            if (self.max<=reward_all):
                self.max=reward_all
                self.pos=episode_num
                self.maxt=time_step
            if(reward_all<0):
                counter_neg=counter_neg+1
            if reward_all>=0 :
                counter_positive=counter_positive+1
            #print("sum finale ", sum_finale)
            if(sum_finale>=0):
                undiscovered=self.number_of_walls_t1-sum_finale
                print("positive sum_finale")
            else:
                undiscovered=abs(sum_finale)+self.number_of_walls_t1
            #    print("negative sum_finale")
            temp=(available/(available-undiscovered))
           # print("undiscovered",undiscovered)
            #print("available",available)
            #print("no of walls",self.number_of_walls_t1)
            #print("temp",temp)
            coverage=100/temp
           # print("coverage",coverage)
            cover_list.append(coverage)
            #print("coverage",coverage)    


            
            print("wall hit total {w}, for episode :{e}".format(w=sum_wall,e=episode_num))
            if episode_num % 1==0:
                print("max_score {m}, Best Episode: {e} , Best Final Step: {t} ".format(m=self.max,e=self.pos,t=self.maxt))
                print(" number of negative rewards {n},number of positive: {u}:".format(n=counter_neg,u=counter_positive)) 
                                                                                               
        #print(rewards_list)
        #plt.plot(timesteps_list,rewards_list)
        #fig = plt.figure()
        #ax1 = fig.add_subplot(1, 2, 1)
        #ax2 = fig.add_subplot(1, 2, 2)
        #ax3=fig.add_subplot(2, 1, 1)
        #ax1.plot(timesteps_list, rewards_list, label='reward-time')
        #ax2.plot(timesteps_list, cover_list, label='steps-episodes')
        #ax3.plot(timesteps_list,wall_list,label='wall hit numbers')
        #ax1.set_xlabel('episodes_test')
        #ax1.set_ylabel('reward')
        #ax1.set_title('first data set')
        #ax1.legend()
        #ax2.set_xlabel('episodes_test')
        #ax2.set_ylabel('% coverage')
        #ax3.set_xlabel('episodes_test')
        #ax3.set_ylabel('wall hit number')
        temp2=sum(cover_list)
        
        median=temp2/self.episodes_testing
        print("median of coverage %s %%\n" % median)
        fig, (ax1, ax2,ax3) = plt.subplots(3,sharex=True)
        ax1.plot(timesteps_list, rewards_list)
        ax2.plot(timesteps_list , cover_list)
        ax3.plot(timesteps_list , wall_list)
        ax1.set_xlabel('episodes_test')
        ax1.set_ylabel('reward')
        ax1.set_title('MAX_TIMESTEP=100')
        #ax1.legend()
        ax2.set_xlabel('episodes_test')
        ax2.set_ylabel('% coverage')
        ax3.set_xlabel('episodes_test')
        ax3.set_ylabel('wall hit number')





if __name__ =="__main__":
    #setInterval(ConnectButton,60000);
    
    gpu_info = !nvidia-smi
    gpu_info = '\n'.join(gpu_info)
    if gpu_info.find('failed') >= 0:
      print('Select the Runtime > "Change runtime type" menu to enable a GPU accelerator, ')
      print('and then re-execute this cell.')
    else:
      print(gpu_info)
    #with tf.Session() as sess:
      #  devices = sess.list_devices()
    print(tf.__version__)
    #print(currentDirectory)
    #sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))

    if tf.test.gpu_device_name():
        print('Default GPU Device: {}'.format(tf.test.gpu_device_name()))
    else:
        print("Please install GPU version of TF")

    lr=0.000005
    env=Environment(episodes_number=100000,episodes_testing=10,render=1,recorder=1,max_timestep=1000,test=test,replay_steps=16,
                    max_random_moves=0,agents_number=2,num_landmarks=3,grid_size=50)
    
    
    state_sizee = env.env.state_size
    action_space = env.env.action_space()
    all_agents = []
    for b_idx in xrange(env.num_agents):
       # brain_file = get_name_brain(args, b_idx)
        all_agents.append(Agent(state_size=state_sizee, action_size=action_space, bee_index=b_idx, learning_rate=lr,
                                target_frequency=10000,memory_capacity=100000,prioritization_scale=0.8,maximum_exploration=25000,batch_size=64))
        
    #rewards_file = get_name_rewards(args)
    #timesteps_file = get_name_timesteps(args)
     
    env.run(all_agents)
    print("--- %s seconds ---" % (time.time() - start_time))




 
