POST_RESPONSE=$(curl -s -X POST http://localhost:5000/api/timeline_post -d "name=Sakshyam&email=sakshyamsigdel@gmail.com&content=Running this test script's endpoint with curl&")
echo $POST_RESPONSE

TESTID=$(echo $POST_RESPONSE | jq -r '.id') # strip and get testid
echo $TESTID

GET_RESPONSE=$(curl -s -X GET http://localhost:5000/api/timeline_post?id=$TESTID) #test the thing that was just created
echo $GET_RESPONSE

DELETE_RESPONSE=$(curl -s -X DELETE http://localhost:5000/api/timeline_post?id=$TESTID) # delete the thing that was just curled to get
echo $DELETE_RESPONSE
