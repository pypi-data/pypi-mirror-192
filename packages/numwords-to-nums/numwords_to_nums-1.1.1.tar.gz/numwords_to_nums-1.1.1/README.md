## Installation
```
pip3 install numwords_to_nums
```

## Usage
Python 3 only!
```
from numwords_to_nums import NumWordsToNum
num = NumWordsToNum()
num.numwords_to_nums("twenty ten and twenty one")
> 2010 and 21

To use our operator converter 
num = NumWordsToNum()
text = "one point two plus two"
num.numerical_words_to_numbers(text, convert_operator = True)
> 1.2+2

To get the evaluation result of any numerical expression
num = NumWordsToNum()
text = "one point two plus two"
result = num.numerical_words_to_numbers(text, convert_operator = True)
num.evaluate(result)
> 3.2
```

It can handle a variety of phrases. It also maintains ordinals such as first--> 1st:

```
"This is just a random sentence." -> 'This is just a random sentence.'
"I am twenty five years old and my dad is 50 years old. I would like to get my father two cars!" -> 'I am 25 years old and my dad is 50 years old. I would like to get my father 2 cars!'
"I was born in twenty ten" -> 'I was born in 1997'
"In the year twenty twenty one, the forty sixth President of the United States was inaugurated." -> 'In the year 2021, the 46th President of the United States was inaugurated.'
"Joe Biden became the oldest person to assume the presidency at the age of seventy eight." -> 'Joe Biden became the oldest person to assume the presidency at the age of 70 eight.'
"He was elected in November twenty twenty after defeating the incumbent, Donald Trump." -> 'He was elected in November 2020 after defeating the incumbent, Donald Trump.'
"Bidens inauguration took place on January twentieth, which marked the fifty ninth quadrennial presidential inauguration." -> 'Bidens inauguration took place on January 20th, which marked the 59th quadrennial presidential inauguration.'
"The event was held at the U.S. Capitol in Washington, D.C., and was attended by a limited number of people due to the COVID-nineteen pandemic." -> 'The event was held at the U.S. Capitol in Washington, D.C., and was attended by a limited number of people due to the COVID-19 pandemic.'
"Despite the challenges, the fifty ninth presidential inauguration was a historic moment for the country." -> 'Despite the challenges, the 59th presidential inauguration was a historic moment for the country.'
"three forty five" -> '345'
"one point two plus two" -> '1.2+2'  (To use this make sure to use flag (convert_operator = True))
"one point two plus two" -> '3.2' (To use this make sure to use evaluate function)
```

I find this useful if using Alexa/Lex to convert audio to text and have to convert the text to digits.

## Improvements/Issues
- Still need to add support for decimal numbers
- Need to add support for negative numbers

## Acknowledgements
I have heavily used code from the SO answers from here: https://stackoverflow.com/questions/493174/is-there-a-way-to-convert-number-words-to-integers
and improved upon them