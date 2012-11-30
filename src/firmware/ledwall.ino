#include <SPI.h>

void setup()
{
	Serial.begin(1000000);
	SPI.begin();
	SPI.setBitOrder(MSBFIRST);
	SPI.setDataMode(SPI_MODE0);
	SPI.setClockDivider(SPI_CLOCK_DIV16);
}

void loop()
{
	uint8_t c;

	for(;;)
	{
		while (!Serial.available()) {}

		if ( (c = Serial.read()) == 254 )
			delay(1);
		else
			SPI.transfer(c);
	}
}
