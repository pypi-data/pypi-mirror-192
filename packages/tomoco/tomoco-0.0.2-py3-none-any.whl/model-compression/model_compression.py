import timm
from torchsummary import summary
import numpy as np
from datetime import datetime 

import torch
import torch.nn as nn 
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import torch.nn.functional as F
import matplotlib.pyplot as plt
import collections
from collections import defaultdict
import os

import ipdb
import timm
from torchvision.datasets import CIFAR10
import torch_pruning as tp
import torchvision.models as models
import torch
import time




def training(model, config, train_loader, valid_loader):
    
    model.train()
    
    ########### Train  ###############
    for ep in range(config.epochs):
        running_loss = 0
        running_acc = 0
        for batch_idx, data in enumerate(train_loader):
            config.optim.zero_grad()
            image, label = data
            image, label = image.to(config.device), label.to(config.device)
            out = model(image)
            loss = config.criterion(out, label)
            acc = torch.argmax(out, 1) - label
            running_acc+= len(acc[acc==0])
            running_loss+= loss.item() * label.size(0)
            loss.backward()
            config.optim.step()
        epoch_loss = running_loss/ len(train_loader.dataset)
        train_epoch_acc = running_acc/ len(train_loader.dataset)
        
        
        ########### Validate #############


        print(f'{datetime.now().time().replace(microsecond=0)} --- '
                  f'Epoch: {ep+1}\t'
                  f'Train loss: {epoch_loss:.4f}\t'
                  f'Train accuracy: {100 * train_epoch_acc:.2f}\t')
        validate(model, valid_loader)

    return model

def validate(model, valid_loader):
    val_running_acc = 0
    model.eval()
    for batch_idx, data in enumerate(valid_loader):

        image, label = data
        image, label = image.to(config.device), label.to(config.device)
        out = model(image)
        acc = torch.argmax(out, 1) - label
        val_running_acc+= len(acc[acc==0])
    val_epoch_acc = val_running_acc/ len(valid_loader.dataset)


    print(f'{datetime.now().time().replace(microsecond=0)} --- '
              f'Valid accuracy: {100 * val_epoch_acc:.2f}')
        

    




def universal_layer_identifier(identification, module, module_name):
    if(identification == None):
        if isinstance(module, nn.Conv2d):
            return True
    else:
        if (identification in module_name):
            return True
def universal_get_layer_id_pruning(model, pruning_type, pruning_percent, identification=None): #identification = none
    if(pruning_type == 'L1'):
        strategy  = tp.strategy.L1Strategy()
    elif(pruning_type == 'L2'):
        strategy  = tp.strategy.L2Strategy()
    channels_pruned = []

    def find_instance(obj):
        if isinstance(obj, nn.Conv2d):
            # ipdb.set_trace()
            pruning_idx = strategy(obj.weight, amount = pruning_percent)
            channels_pruned.append(pruning_idx)
            return None
        elif isinstance(obj, list):
            for internal_obj in obj:
                find_instance(internal_obj)
        elif (hasattr(obj, '__class__')):
            for internal_obj in obj.children():
                find_instance(internal_obj)
        elif isinstance(obj, OrderedDict):
            for key, value in obj.items():
                find_instance(value)

    find_instance(model)

    channels_pruned = np.asarray(channels_pruned, dtype=object)
    return channels_pruned


def universal_filter_pruning(model, input_shape, config, channels_pruned, identification=None):
    DG = tp.DependencyGraph()
    DG.build_dependency(model, example_inputs= torch.randn(input_shape).to(config.device))

    layer_id = 0

    def find_instance(obj):
        if isinstance(obj, nn.Conv2d):
            pruning_plan = DG.get_pruning_plan(obj, tp.prune_conv_out_channel, idxs=channels_pruned[layer_id])
            pruning_plan.exec()
            return None
        elif isinstance(obj, list):
            for internal_obj in obj:
                find_instance(internal_obj)
        elif (hasattr(obj, '__class__')):
            for internal_obj in obj.children():
                find_instance(internal_obj)
        elif isinstance(obj, OrderedDict):
            for key, value in obj.items():
                find_instance(value)

    find_instance(model)
    return model



def pruner(model,experiment_name, config, input_dims, pruning_stratergy, pruning_percent,  train_loader, valid_loader):
    path = './weights/'
    if(not os.path.exists(path)):
        os.mkdir(path)
    

    validate(model, valid_loader)
    print("\n\n \n*********** Model Before Pruning **********")
    torch.save(model,'./weights/'+experiment_name+'_original.pth')
    # print(summary(model,input_dims))

    channels_pruned = universal_get_layer_id_pruning(model, pruning_stratergy, pruning_percent)
    # print(channels_pruned)
    # print(len(channels_pruned))
    pruned_model = universal_filter_pruning(res50, (config.batch_size,)+input_dims,config, channels_pruned).to(config.device)
    if(config.training):
        pruned_model = training(pruned_model, config, train_loader, valid_loader)
        torch.save(pruned_model,'./weights/'+experiment_name+'_pruned.pth')


    model = torch.load('./weights/'+experiment_name+'_original.pth')
    pruned_model = torch.load('./weights/'+experiment_name+'_pruned.pth')
    print("*********** Model Comparison **********")
    print("*********** Original Model **********")
    print(summary(model,input_dims))
    print("*********** Pruned Model **********")
    print(summary(pruned_model,input_dims))

    print("*********** Validation Accuracy **********")

    validate(model, valid_loader)
    validate(pruned_model, valid_loader)



class config:
    lr = 0.001
    n_classes = 10
    epochs = 5
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    batch_size = 64
    optim = 0
    training =1
    criterion = nn.CrossEntropyLoss()


#
# # TODO:
# # * Fix Accuracy Metric
#
# train_dataset = CIFAR10(root='data/', download=True, transform=transforms.ToTensor())
# valid_dataset = CIFAR10(root='data/',  download=True,train=False, transform=transforms.ToTensor())
#
# # define the data loaders
# train_loader = DataLoader(dataset=train_dataset, batch_size=config.batch_size, shuffle=True)
# valid_loader = DataLoader(dataset=valid_dataset, batch_size=config.batch_size, shuffle=False)
#
#
#
#
#
#
#
# res50 = timm.create_model("resnet50", pretrained=True).to(config.device)
# config.optim =  torch.optim.Adam(res50.parameters(), lr=0.001,  amsgrad=True)
#
# pruner(res50,"res50", config, (3,64,64), "L1", 0.15,  train_loader, valid_loader)
