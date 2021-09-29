#!/bin/bash

experiment_name='individual_demo'

while [ ! -f $experiment_name"/neuroended" ]
do 
	python GA_1.py
done

exit 0
	
