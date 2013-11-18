screen -S workers -X quit
screen -AdmS workers

screen -S workers -X screen -t queue python queueing_service.py
screen -S workers -X screen -t webapp python webapp.py

for i in {1..3}
do
    screen -S workers -X screen -t worker$i rqworker
done
