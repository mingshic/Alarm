for i in `ps -ef|grep supervisord | grep -v grep | awk -F " " '{print $2}'`
do
    kill $i 
done
