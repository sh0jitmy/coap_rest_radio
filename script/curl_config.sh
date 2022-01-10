JSON=$1
URL=http://localhost:28081/control
curl -H 'Content-Type:application/json'  -d @./control.json $URL -X PUT
#curl -X PUT -H 'Content-Type: application/json'  -d '{"frequency":"225"}' $URL
#curl -X PUT -H 'Content-Type: application/json'  -d @$JSON $URL
echo
