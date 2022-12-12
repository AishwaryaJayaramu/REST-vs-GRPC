import base64
import random
import grpc
import struct
import sys
import time

import lab6_pb2
import lab6_pb2_grpc

if len(sys.argv) != 5:
    print("\npython grpc-client.py <server address> <endpoint> <iterations> <debug>")
    exit()

addr = sys.argv[1] + ':50051'

cmd = sys.argv[2]
itr = sys.argv[3]
debug = sys.argv[4].lower() == 'true'
reps = int(itr)

img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
encoded_img = base64.b64encode(img)

#Open gRPC channel
channel = grpc.insecure_channel(addr)

if(cmd == 'rawImage'):
    stub = lab6_pb2_grpc.rawImageStub(channel)
    start = time.perf_counter()

    for x in range(reps):
        data = lab6_pb2.rawImageMsg(img=img)
        response = stub.rawImage(data)
        if debug:
           print(response.width, response.height)

    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")

elif(cmd == 'jsonImage'):
    stub = lab6_pb2_grpc.jsonImageStub(channel)
    start = time.perf_counter()

    for x in range(reps):
        data = lab6_pb2.jsonImageMsg(img=encoded_img)
        response = stub.jsonImage(data)
        if debug:
           print(response.width, response.height)

    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")

elif(cmd == 'add') :
    stub = lab6_pb2_grpc.addStub(channel)
    start = time.perf_counter()

    for x in range(reps):
        data = lab6_pb2.addMsg(a=2, b=3)
        response = stub.add(data)
        if debug:
           print(response.sum)

    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")    

elif(cmd == 'dotProduct') :
    stub = lab6_pb2_grpc.dotProductStub(channel)
    start = time.perf_counter()

    for x in range(reps):
        list1 = []
        list2 = []
        for i in range(0,100):
            num = random.random()
            list1.append(num)
        for i in range(0,100):
            num = random.random()
            list2.append(num)  
        data = lab6_pb2.dotProductMsg(a=list1, b=list2)
        response = stub.dotProduct(data)
        if debug:
           print(response.dotproduct)  

    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")

else:
    print("Unknown option", cmd)