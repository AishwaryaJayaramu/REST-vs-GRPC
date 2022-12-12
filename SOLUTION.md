
![image](https://user-images.githubusercontent.com/111898538/198393063-d392233b-35c6-47d3-a404-486fb9eb7567.png)



I've created 4 endpoints ie add, image, json image and dotProduct and I've run the REST service and the GRPC service on both add and image for an iteration count of 1000 for the first test and second test.

For the third test( different regions) I ran the endpoints for a count of 100 iterations.

Results:

Local - Test 1

The GRPC service was roughly 5 times faster than the REST service while executing the add service. This could be mainly due to the tight packing of the protocol buffers and the use of HTTP/2 by GRPC which is more significant than HTTP. Also GRPC is designed for low latency and high throughput communication and it suitable for low-weight services such as the add function.

However GRPC was significantly poorer than REST in terms of sending streaming data such as images. Since both the client and server are running on the same host, REST communication is faster since the data doesn't have to be serialised. However GRPC serialises data even on the local network, hence takes more time in this case.

Same-Zone - Test 2

While testing on two difference hosts that are within the same zone, the REST add services takes around 3.6 ms and the GRPC add service surpasses the former by roughly 5 times in terms of performance which is similar to the results obtained in test 1. However the time per query of the REST add/image service is much more than in the first case. This could be due to the fact that the client and server are running on two different machines and Network latency depends on the pysical distance between the server and client.

Similary, the REST image and the GRPC image services take similar time for the queries. GRPCs are poor when it comes to streaming large data but the REST doesn't significantly perform better. Again this could resonate to the physical distance the packet needs to travel from source to destination.

Different-Zone - Test 3

While placing the server on the entirely different zone as that of the client, the REST services for both add and image perform very badly. This is due to the fact the REST service creates a new TCP connection for every request made and this request might need to make several hops before reaching the europe-west 3 server. Network latency is directly dependent on the number of network devices which have to be crossed by a packet and this is inherent in terms of the REST.

Again the GRPC also takes significant amounts of time per query while in different zones but is significantly better when compared to the REST service. The REST and the GRPC are closer in time for the add service but for the image service, REST is off-point by around 1000ms. GRPC makes just a single TCP connection from client to server which is used for all its queries which can make better use of server resources. GRPC is very fast owing to the protocol buffers and the information comes on/off the wire much faster.

From these experiments, I feel that GRPC is definitely faster and a better alternative to REST.

Ping Results:

The average round trip time for the local machine is 0.54 milliseconds The average round trip time for two hosts on the same zone is 0.981 milliseconds

The average round trip time for two hosts on different zones is 141 ms.

In the first two cases, the latency is similar and isn't much but for the third case, since the hosts are in two different regions, the latency is so much more.
