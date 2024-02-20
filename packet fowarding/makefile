CC = g++
CFLAGS = -std=c++11
TARGET = pktforward

all: $(TARGET)

$(TARGET): pktforward.cpp
	$(CC) $(CFLAGS) -o $@ $^

clean:
	rm -f $(TARGET)
