#!/bin/bash

function loopTest() {
	arg="0"
	if [[ $1 == -* ]]; then
		arg=$1
		shift
	fi
	echo -e "Press enter to start: \033[0;34m$1\033[m"
	read
	shift
	inputs=("$@")
	for input in "${inputs[@]}"
	do
		if [ $arg == "0" ]; then
			echo -e "Test:" "\033[0;32m" "\"$input\"" "\033[m"
			python3 main.py "$input"
		else
			echo -e "Test:" "\033[0;32m" $arg "\"$input\"" "\033[m"
			python3 main.py $arg "$input"
		fi
		echo 
	done
}

subject=(
	'5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0'
	'5 * X^0 + 4 * X^1 = 4 * X^0'
	'8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 3 * X^0'
)

degree0=(
	'42 * X^0 = 42 * X^0'
	'0 * X^0 = 0 * X^0'
	'1 * X^0 = - 2 * X^0'
)

degree1=(
	"2 * X^0 + 4 * X^1 = 0"
	"2 * X^0 + 4 * X^1 = 10 * X^0 + 2 * X^1"
	"0 * X^0 - 2 * X^1 = 0 * X^0 + 2 * X^1"
)

degree2Positive=(
	"0 = 2 * X^0 - 2 * X^1 - 4 * X^2"
	"2 * X^0 - 2 * X^1 - 4 * X^2 = 1 * X^0 + 1 * X^1"
	"0 * X^0 - 3 * X^1 - 0 * X^2 = 1 * X^0 + 1 * X^1 - 3 * X^2"
)

degree2Null=(
	"0 = 1 * X^0 + 2 * X^1 + 1 * X^2"
	"0.5 * X^0 - 1  * X^1 + 0 * X^2 = 0 * X^0 + 0 * X^1 - 0.5 * X^2"
	"4 * X^0 + 4 * X^1 + 1 * X^2 = 0"
)

degree2Negative=(
	"0 * X^0 - 0.5  * X^1 + 0 * X^2 = - 0.5 * X^0 + 0 * X^1 - 0.25 * X^2"
	"10 * X^0 - 0.5  * X^1 + 1 * X^2 = 0"
	"1 * X^0 - 1  * X^1 + 1 * X^2 = 0 * X^0 - 1 * X^1"
)

degreeAboveTwo=(
	"1 * X^0 + 1 * X^1 + 1 * X^2 + 1 * X^3 = 0"
	"- 1 * X^0 + 7 * X^1 + 1.5 * X^2 - 1 * X^3 + 10 * X^4 - 5 * X^5 - 1.5 * X^6 + 3 * X^7 = 0"
	"- 1 * X^0 + 7 * X^1 + 1.5 * X^2 = - 1 * X^0 + 7 * X^1 + 1.5 * X^2 - 1 * X^3 + 10 * X^4"
)

syntaxLexical=(
	'1 X^1 = 1'
	'1 * X1 = 1'
	'1 * X^1.2 = 1'
	'1 = 1 X^1'
	'1 = 1 * X1'
	'1 = 1 * X^1.2'
	'1. + 1 * x^1 = 1'
	'1 * X^1'
	'1'
	'1 ='
	'= 1'
	'1 + = 1'
	'1 = 1 -'
	'1 = 1 = 1'
	'1 = 1 + 1 = 1'
	'1 = = 1'
	'1 + - 1 = 1'
	'1 * X^2 * 2 * X^1 = 1'
	'1a + 1 * X^2 = 1'
)

powerCoef=(
	"1 + X - X^2 = -2"
	"1 + X + 2 * X^2 = - 4 + X - X^2"
	"2 + X - X^2 + X^3 = 2 + X - X^2 + X^3 - X^4 + X^5 + X^6 - X^7 + X^8 - X^9 + X^10"
)

syntaxCorrection=(
	"1+x-X^2  =-3"
	"+0+ 2*x-x^2 = -3+4*x  - 5* X^2"
	"-7+ 2*x =-3+4*x  - 5      *X^2"
)

powerOrder=(
	"x^2 - 1 + X =0"
	"x^2 = 2*x"
	"x^2-1 = 2*x - 1*x^0"
)

powerRepeated=(
	"x+x+x+x+x + 1+1+1+1 = x^2+x^2"	
	"1+ x+ x^3-x^3 +x +1 = x^2 +1+ x^2"	
	"x^2+x+1 + x^2+x+1 + x^2+x+1 + x^2+x+1 + x^2+x+1 = 0"	
)

rationalCoef=(
	"1 + 1.5*x -0.5*x^2 = 1.5"
	"10.125 = 0 + x + 1.5*x^2 - 0.5*x - 1.5*x^2"
	"0.3333333333*x = 0 + 0.3333333333*x"
)

division=(
	"1/2 + 1/2*x + 1/2*x^2 = 0"
	"1/3 + 1000/2*x - 10/5*x^2 = 998/2*x"
	"1 - 100/2*x - 10/5*x^2 = - 998/2*x"
)

coefPosition=(
	"x*2 + x^2*3 - x^0*1 = 0"
	"x*2 + x^2*3 + x^1*1/2 - x^0*1 = x^2*3 - 1"
	"x*2*2/1 + x^2*2/1 + x^1*1/2 - x^0*1 = x^2*3"
)

programOption=(
	"1 + 2*x + 2*X^2 = 2*x^2 + 3*x^2"
)

fraction1=(
	"5 + 2 * X + X^2= X^2"
	"2 * X^0 - 2 * X^1 - 4 * X^2 = 1 * X^0 + 1 * X^1"
	"0 * X^0 - 3 * X^1 - 0 * X^2 = 1 * X^0 + 1 * X^1 - 3 * X^2"
)

fraction2=(
	"0 = 2 * X^0 - 2 * X^1 - 4 * X^2"
	"10.125 = 0 + x + 1.5*x^2 - 0.5*x - 1.5*x^2"
)

fractionVerbose=(
	"x^2*2 +10/2*x = 3"
	"2*x^2 + 1*x -6*x^0 = 0"
)

parsingPrecedence=(
	"2*3*x*2 = 36"
	"2*2*2* x^2 *1/2*1/2*1/2 = 4*4*4* x *0.25*0.25*0.25"
	"1*1*2*10/10 +2*2*2* x^2 *1/2*1/2*1/2 = 4*4*4* x *0.25*0.25*0.25"
)

echo
loopTest "Equations from subject" "${subject[@]}"
loopTest "Equations degree 0" "${degree0[@]}"
loopTest "Equations degree 1" "${degree1[@]}"
loopTest "Equations degree 2 - discriminant > 0" "${degree2Positive[@]}"
loopTest "Equations degree 2 - discriminant = 0" "${degree2Null[@]}"
loopTest "Equations degree 2 - discriminant < 0" "${degree2Negative[@]}"
loopTest "Equations degree > 2" "${degreeAboveTwo[@]}"
echo -e "\033[1;31mBONUS\033[m\n"
loopTest "Syntax and lexical errors" "${syntaxLexical[@]}"
loopTest "Powers and coefficients deduction" "${powerCoef[@]}"
loopTest "Syntax correction" "${syntaxCorrection[@]}"
loopTest "Power order" "${powerOrder[@]}"
loopTest "Power repeated" "${powerRepeated[@]}"
loopTest "Rational coefficients" "${rationalCoef[@]}"
loopTest "Division" "${division[@]}"
loopTest "Coefficient position" "${coefPosition[@]}"
loopTest "-h" "Option -h" "${programOption[@]}"
loopTest "--help" "Option --help" "${programOption[@]}"
loopTest "-v" "Option -v" "${programOption[@]}"
loopTest "--verbose" "Option --verbose" "${programOption[@]}"
loopTest "-f" "Options -f" "${fraction1[@]}"
loopTest "--fraction" "Options --fraction" "${fraction2[@]}"
loopTest "-vf" "Options -vf" "${fractionVerbose[@]}"
loopTest "-v" "Parsing precedence" "${parsingPrecedence[@]}"
