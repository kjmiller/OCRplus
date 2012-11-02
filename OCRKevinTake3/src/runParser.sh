rm *.dat *.o
g++ -c *.cpp
g++ -o parser *.o
./parser
