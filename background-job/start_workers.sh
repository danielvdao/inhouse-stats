screen -S workers -X quit
screen -AdmS workers

for i in {1..5}
do
    screen -S workers -X screen -t tab$i rqworker
done
