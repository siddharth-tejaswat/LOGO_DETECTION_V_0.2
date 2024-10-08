#!/bin/bash
#to run node
cd /home/truedatasoft/Haier_TV/app_2/ && npm run dev &
#sleep 5
#to run AI
cd /home/truedatasoft/Haier_TV/modules/ && source ./venv/bin/activate 
python main.py &


