import base64
import grpc
from concurrent import futures
import time
from PIL import Image
import io
from io import BytesIO

import lab6_pb2
import lab6_pb2_grpc

class addServicer(lab6_pb2_grpc.addServicer):
    def add(self, request, context):
        response = lab6_pb2.addReply()
        response.sum = request.a + request.b
        return response

class dotProductServicer(lab6_pb2_grpc.dotProductServicer):
    def dotProduct(self, request, context):
        response = lab6_pb2.dotProductReply()
        list_1 = request.a
        list_2 = request.b
        response.dotproduct = sum(x*y for x, y in zip(list_1, list_2))
        return response        

class rawImageServicer(lab6_pb2_grpc.rawImageServicer):
    def rawImage(self, request, context):
        response = lab6_pb2.imageReply()
        ioBuffer = io.BytesIO(request.img)
        img = Image.open(ioBuffer)
        response.width = img.size[0]
        response.height = img.size[1] 
        return response


class jsonImageServicer(lab6_pb2_grpc.jsonImageServicer):
    def jsonImage(self, request, context):
        response = lab6_pb2.imageReply()
        imgData = base64.b64decode(request.img)
        img = Image.open(BytesIO(imgData))
        response.width = img.size[0]
        response.height = img.size[1] 
        return response


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

lab6_pb2_grpc.add_addServicer_to_server(addServicer(), server)

lab6_pb2_grpc.add_rawImageServicer_to_server(rawImageServicer(), server)

lab6_pb2_grpc.add_jsonImageServicer_to_server(jsonImageServicer(), server)

lab6_pb2_grpc.add_dotProductServicer_to_server(dotProductServicer(), server)


print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()
server.wait_for_termination()