# This is a make file to compile gr code

gr : main.o functions.o
	g++ -O3 -g -Wall -o gr main.o functions.o

main.o: particle.h bincontainer.h
functions.o: functions.h bincontainer.h

clean: 
	rm -f *.o
