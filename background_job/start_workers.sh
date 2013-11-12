screen -S workers -X quit
screen -AdmS workers

screen -S workers -X screen -t tab0 python queueing_service.py

for i in {1..3}
do
    screen -S workers -X screen -t tab$i rqworker
done
