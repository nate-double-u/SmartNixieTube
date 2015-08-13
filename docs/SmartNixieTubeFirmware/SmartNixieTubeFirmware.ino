/*********************************************************************
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*********************************************************************/

/* nixie digits */
#define ZERO   A0
#define ONE    A1
#define TWO    A2
#define THREE  A3
#define FOUR   A4
#define FIVE   A5
#define SIX    2
#define SEVEN  4
#define EIGHT  7
#define NINE   8

/* nixie anode */
#define ANODE  9

/* nixie decimal points */
#define RDP   10
#define LDP   11

/* RGB LED */
#define RED    5
#define GREEN  6
#define BLUE   3

/* error LED */
#define ERR_LED 13

/* $DIGIT,LDP,RDP,ANODE,RED,GREEN,BLUE */
/* example: $8,N,N,128,255,000,255! */
unsigned char fifoBuffer[22];
unsigned char bufferIndex = 0x00;

void setup()
{
	/* set all outputs low */
	digitalWrite(ZERO, LOW);
	digitalWrite(ONE, LOW);
	digitalWrite(TWO, LOW);
	digitalWrite(THREE, LOW);
	digitalWrite(FOUR, LOW);
	digitalWrite(FIVE, LOW);
	digitalWrite(SIX, LOW);
	digitalWrite(SEVEN, LOW);
	digitalWrite(EIGHT, LOW);
	digitalWrite(NINE, LOW);
	digitalWrite(LDP, LOW);
	digitalWrite(RDP, LOW);
	digitalWrite(ANODE, LOW);
	digitalWrite(RED, LOW);
	digitalWrite(GREEN, LOW);
	digitalWrite(BLUE, LOW);
	digitalWrite(ERR_LED, LOW);

	/* set all pins as outputs */
	pinMode(ZERO, OUTPUT); 
	pinMode(ONE, OUTPUT); 
	pinMode(TWO, OUTPUT); 
	pinMode(THREE, OUTPUT); 
	pinMode(FOUR, OUTPUT); 
	pinMode(FIVE, OUTPUT); 
	pinMode(SIX, OUTPUT); 
	pinMode(SEVEN, OUTPUT); 
	pinMode(EIGHT, OUTPUT); 
	pinMode(NINE, OUTPUT); 
	pinMode(LDP, OUTPUT); 
	pinMode(RDP, OUTPUT); 
	pinMode(ANODE, OUTPUT); 
	pinMode(RED, OUTPUT); 
	pinMode(GREEN, OUTPUT); 
	pinMode(BLUE, OUTPUT); 
	pinMode(ERR_LED, OUTPUT);

	/* start serial port */
	Serial.begin(115200);
}

void loop()
{
	/* is there serial data available? */
	if (Serial.available() > 0)
	{
		/* read the received byte */
		unsigned char incomingByte = Serial.read();

		/* throw away line feeds and carriage returns */
		if ((incomingByte != 0x0A) && (incomingByte != 0x0D))
		{
			switch (incomingByte)
			{
				/* latch command */
				case '!':
					parseFifoBuffer();
					break;

				/* clear command */
				case '@':
					clearFifoBuffer();
					break;

				/* all other data */
				default:
					updateFifoBuffer(incomingByte);
					break;
			}
		}
	}
}

/* saves incoming byte to buffer and transmits oldest byte if full */
void updateFifoBuffer(unsigned char incomingByte)
{
	/* do we have empty space? */
	if (bufferIndex < (sizeof(fifoBuffer)))
	{
		/* yep, save the incoming byte */
		fifoBuffer[bufferIndex++] = incomingByte;
	}

	/* buffer is full, need to tx oldest byte */
	else
	{
		/* tx oldest byte */
		Serial.write(fifoBuffer[0]);

		/* shift all bytes up one spot in buffer */
		for (unsigned char i = 1; i < sizeof(fifoBuffer); i++)
		{
			fifoBuffer[i - 1] = fifoBuffer[i];
		}

		/* save incoming byte to end of buffer */
		fifoBuffer[bufferIndex - 1] = incomingByte;
	}
}

/* parses buffer once the latch command is received */
void parseFifoBuffer()
{
	/* pass the command down the line */
	Serial.write('!');

	/* buffer must start with $ */
	if (fifoBuffer[0] != '$')
	{
		blinkErrorLED();
		return;
	}

	/* make sure commas are in correct spots */
	if ((fifoBuffer[2]  != ',') || (fifoBuffer[4]  != ',') || (fifoBuffer[6] != ',') ||
		(fifoBuffer[10] != ',') || (fifoBuffer[14] != ',') || (fifoBuffer[18] != ','))
	{
		blinkErrorLED();
		return;
	}

	/* check nixie digit value */
	if (((fifoBuffer[1] < '0') || (fifoBuffer[1] > '9')) && (fifoBuffer[1] != '-'))
	{
		blinkErrorLED();
		return;
	}

	/* check ANODE PWM value */
	if (((fifoBuffer[7] < '0') || (fifoBuffer[7] > '9')) ||
		((fifoBuffer[8] < '0') || (fifoBuffer[8] > '9')) ||
		((fifoBuffer[9] < '0') || (fifoBuffer[9] > '9')))
	{
		blinkErrorLED();
		return;
	}

	/* check RED LED PWM value */
	if (((fifoBuffer[11] < '0') || (fifoBuffer[11] > '9')) ||
		((fifoBuffer[12] < '0') || (fifoBuffer[12] > '9')) ||
		((fifoBuffer[13] < '0') || (fifoBuffer[13] > '9')))
	{
		blinkErrorLED();
		return;
	}

	/* check GREEN LED PWM value */
	if (((fifoBuffer[15] < '0') || (fifoBuffer[15] > '9')) ||
		((fifoBuffer[16] < '0') || (fifoBuffer[16] > '9')) ||
		((fifoBuffer[17] < '0') || (fifoBuffer[17] > '9')))
	{
		blinkErrorLED();
		return;
	}

	/* check BLUE LED PWM value */
	if (((fifoBuffer[19] < '0') || (fifoBuffer[19] > '9')) ||
		((fifoBuffer[20] < '0') || (fifoBuffer[20] > '9')) ||
		((fifoBuffer[21] < '0') || (fifoBuffer[21] > '9')))
	{
		blinkErrorLED();
		return;
	}

	/* check decimal point values */
	if (((fifoBuffer[3] != 'Y') && (fifoBuffer[3] != 'N')) || 
		((fifoBuffer[5] != 'Y') && (fifoBuffer[5] != 'N')))
	{
		blinkErrorLED();
		return;
	}

	/* turn off all of the digits */
	digitalWrite(ZERO, LOW);
	digitalWrite(ONE, LOW);
	digitalWrite(TWO, LOW);
	digitalWrite(THREE, LOW);
	digitalWrite(FOUR, LOW);
	digitalWrite(FIVE, LOW);
	digitalWrite(SIX, LOW);
	digitalWrite(SEVEN, LOW);
	digitalWrite(EIGHT, LOW);
	digitalWrite(NINE, LOW);

	/* turn on nixie digit */
	switch (fifoBuffer[1])
	{
		case '0':
			digitalWrite(ZERO, HIGH);
			break;
		case '1':
			digitalWrite(ONE, HIGH);
			break;
		case '2':
			digitalWrite(TWO, HIGH);
			break;
		case '3':
			digitalWrite(THREE, HIGH);
			break;
		case '4':
			digitalWrite(FOUR, HIGH);
			break;
		case '5':
			digitalWrite(FIVE, HIGH);
			break;
		case '6':
			digitalWrite(SIX, HIGH);
			break;
		case '7':
			digitalWrite(SEVEN, HIGH);
			break;
		case '8':
			digitalWrite(EIGHT, HIGH);
			break;
		case '9':
			digitalWrite(NINE, HIGH);
			break;
		default:
			break;
	}

	/* turn left decimal point on or off? */
	if (fifoBuffer[3] == 'Y') 	digitalWrite(LDP, HIGH);
	else 						digitalWrite(LDP, LOW);

	/* turn right decimal point on or off? */
	if (fifoBuffer[5] == 'Y') 	digitalWrite(RDP, HIGH);
	else 						digitalWrite(RDP, LOW);

	/* convert ascii to decimal values */
	unsigned int anodeVal = ((fifoBuffer[7]  - 0x30) * 100) + ((fifoBuffer[8]  - 0x30) * 10) + (fifoBuffer[9]  - 0x30);
	unsigned int redVal   = ((fifoBuffer[11] - 0x30) * 100) + ((fifoBuffer[12] - 0x30) * 10) + (fifoBuffer[13] - 0x30);
	unsigned int greenVal = ((fifoBuffer[15] - 0x30) * 100) + ((fifoBuffer[16] - 0x30) * 10) + (fifoBuffer[17] - 0x30);
	unsigned int blueVal  = ((fifoBuffer[19] - 0x30) * 100) + ((fifoBuffer[20] - 0x30) * 10) + (fifoBuffer[21] - 0x30);

	/* max value is 255 */
	if (anodeVal > 255) anodeVal = 255;
	if (redVal > 255) redVal = 255;
	if (greenVal > 255) greenVal = 255;
	if (blueVal > 255) blueVal = 255;

	/* update PWM registers */
	analogWrite(ANODE, anodeVal);
	analogWrite(RED, redVal);
	analogWrite(GREEN, greenVal);
	analogWrite(BLUE, blueVal);
}

/* clears the FIFO buffer */
void clearFifoBuffer()
{
	/* pass the command down the line */
	Serial.write('@');

	digitalWrite(ZERO, LOW);
	digitalWrite(ONE, LOW);
	digitalWrite(TWO, LOW);
	digitalWrite(THREE, LOW);
	digitalWrite(FOUR, LOW);
	digitalWrite(FIVE, LOW);
	digitalWrite(SIX, LOW);
	digitalWrite(SEVEN, LOW);
	digitalWrite(EIGHT, LOW);
	digitalWrite(NINE, LOW);
	digitalWrite(LDP, LOW);
	digitalWrite(RDP, LOW);
	digitalWrite(ANODE, LOW);
	digitalWrite(RED, LOW);
	digitalWrite(GREEN, LOW);
	digitalWrite(BLUE, LOW);
	digitalWrite(ERR_LED, LOW);

	/* reset the index */
	bufferIndex = 0x00;

	/* clear all bytes of buffer to zero */
	for (unsigned char i = 0; i < sizeof(fifoBuffer); i++)
	{
		fifoBuffer[i] = 0x00;
	}
}

/* blinks the error LED for command error */
void blinkErrorLED()
{
	digitalWrite(ERR_LED, HIGH);
	delay(100);
	digitalWrite(ERR_LED, LOW);
}
