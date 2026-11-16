// Lecture 10: Recursion – Slide 14: Roman Numbers with Recursion
// match on the list of chars, recurse on the tail

def romanToNumber(roman: List[Char]): Int = roman match
  case 'I' :: 'V' :: tail => 4 + romanToNumber(tail)
  case 'I' :: 'X' :: tail => 9 + romanToNumber(tail)
  case 'X' :: 'L' :: tail => 40 + romanToNumber(tail)
  case 'X' :: 'C' :: tail => 90 + romanToNumber(tail)
  case 'C' :: 'D' :: tail => 400 + romanToNumber(tail)
  case 'C' :: 'M' :: tail => 900 + romanToNumber(tail)
  case 'I' :: tail => 1 + romanToNumber(tail)
  case 'V' :: tail => 5 + romanToNumber(tail)
  case 'X' :: tail => 10 + romanToNumber(tail)
  case 'L' :: tail => 50 + romanToNumber(tail)
  case 'C' :: tail => 100 + romanToNumber(tail)
  case 'D' :: tail => 500 + romanToNumber(tail)
  case 'M' :: tail => 1000 + romanToNumber(tail)
  case Nil => 0

romanToNumber("XVI".toList)     // 16
romanToNumber("MCMXCIV".toList) // 1994
