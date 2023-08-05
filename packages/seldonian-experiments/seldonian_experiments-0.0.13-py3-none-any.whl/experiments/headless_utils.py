""" Utilities used in the rest of the library """

import os
import pickle
import numpy as np
import math

from seldonian.RL.RL_runner import (create_agent,
	run_trial_given_agent_and_env)
from seldonian.utils.stats_utils import weighted_sum_gamma
from seldonian.dataset import SupervisedDataSet


import numpy as np
from torch.utils.data import DataLoader
import torch
import torch.nn as nn
from torchvision.transforms import ToTensor
from torch import optim
from torch.autograd import Variable

from seldonian.utils.io_utils import load_pickle,save_pickle

def train_pytorch_model(
	pytorch_model,
	num_epochs,
	data_loaders, 
	optimizer, 
	loss_func):
	""" Train a pytorch model 

	:param pytorch_model: The PyTorch model object. Must have a .forward() method

	:param num_epochs: Number of epochs to train for
	:type num_epochs: int

	:param data_loaders: Dictionary containing data loaders, with keys:
		'candidate' and 'safety', each pointing to torch dataloaders.
		Each data loader should only have features and labels in them.

	:param optimizer: The PyTorch optimizer to use

	:param loss_func: The PyTorch loss function 
	"""
	pytorch_model.train()
		
	# Train the pytorch_model
	total_step = len(data_loaders['candidate'])
		
	for epoch in range(num_epochs):
		for i, (features, labels) in enumerate(data_loaders['candidate']):

			features = features.to(device)
			labels = labels.to(device)
			b_x = Variable(features)   # batch x
			output = pytorch_model(b_x)
			b_y = Variable(labels)   # batch y
			loss = loss_func(output, b_y)
			
			# clear gradients for this training step   
			optimizer.zero_grad()           
			
			# backpropagation, compute gradients 
			loss.backward()    
			# apply gradients             
			optimizer.step()                
			
			if (i+1) % 100 == 0:
				print ('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}' 
					   .format(epoch + 1, num_epochs, i + 1, total_step, loss.item()))

def make_data_loaders(
	features,
	labels,
	frac_data_in_safety,
	candidate_batch_size,
	safety_batch_size):
	"""
	Create PyTorch data loaders for candidate and safety datasets  
	"""
	features = load_pickle(feat_f)
	labels = load_pickle(label_f)
	n_points_tot = len(features)
	n_candidate = int(round(n_points_tot*(1.0-frac_data_in_safety)))
	n_safety = n_points_tot - n_candidate

	F_c = features[:n_candidate] 
	F_s = features[n_candidate:] 
	# Split labels - must be numpy array
	L_c = labels[:n_candidate] 
	L_s = labels[n_candidate:]

	F_c_tensor = torch.from_numpy(F_c)
	F_s_tensor = torch.from_numpy(F_s)
	L_c_tensor = torch.from_numpy(L_c)
	L_s_tensor = torch.from_numpy(L_s)
	
	dataset_c=torch.utils.data.TensorDataset(
		F_c_tensor,
		L_c_tensor) 

	dataloader_c=torch.utils.data.DataLoader(
		dataset_c,
		batch_size=candidate_batch_size,
		shuffle=False) 

	dataset_s=torch.utils.data.TensorDataset(
		F_s_tensor,
		L_s_tensor) 
	
	dataloader_s=torch.utils.data.DataLoader(
		dataset_s,
		batch_size=safety_batch_size,
		shuffle=False) 

	data_loaders = {
		'candidate' : dataloader_c,
		'safety'  : dataloader_s
	}
	return data_loaders


def to_complete():

	cnn = CNNModelNoSoftmax()
	cnn.to(device)
	print("done")

	learning_rate=0.001

	# Loss and optimizer
	loss_func = nn.CrossEntropyLoss()
	optimizer = torch.optim.Adam(cnn.parameters(), lr=learning_rate)

	print("Check state dict before training so we can compare to after training")
	sd_before_training = cnn.state_dict()
	print(sd_before_training['cnn1.weight'][0])
	print("done.\n")

	print(f"Training model on full CNN with {num_epochs} epochs")
	train(num_epochs, cnn, loaders)
	print("done.\n")

	print("Evaluating model:")
	test(cnn)

	print("Compare state dict after training to verify parameters were changed")
	sd_after_training = cnn.state_dict()
	print(sd_after_training['cnn1.weight'][0])

	print("Putting headless model on GPU")
	cnn_headless = CNNHeadlessModel().to(device)
	print("done")

	print("Loading state dictionary into headless model...")
	del sd_after_training['fc3.weight']
	del sd_after_training['fc3.bias']
	cnn_headless.load_state_dict(sd_after_training)
	print("done.")

	print("Verify that the weights were copied over to the headless model:")
	sd_headless = cnn_headless.state_dict()
	print(sd_headless['cnn1.weight'][0])

	print("passing all train and test images through the headless model to create latent features...")
	new_features = np.zeros((23700,256))
	new_labels = np.zeros(23700)
	for i,(images, labels) in enumerate(loaders['candidate']):
		start_index = i*batch_size
		end_index = start_index + len(images)
		images = images.to(device)
		new_labels[start_index:end_index] = labels.numpy()
		new_features[start_index:end_index] = cnn_headless(images).cpu().detach().numpy()
	for j,(images, labels) in enumerate(loaders['safety']):
		start_index = end_index
		end_index = start_index + len(images)
		images = images.to(device)
		new_labels[start_index:end_index] = labels.numpy()
		new_features[start_index:end_index] = cnn_headless(images).cpu().detach().numpy()
	print("done.")

	print("Make sure there are some non-zero values in features. ")
	print(new_features[1001])

	print("Saving latent features and labels")
	save_pickle('facial_gender_latent_features.pkl',new_features)
	save_pickle('facial_gender_labels.pkl',new_labels)
	print("done.")