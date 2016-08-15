#!/bin/bash

ping -c 5 192.168.2.255
arp -a
ssh roomba@192.168.2.2
