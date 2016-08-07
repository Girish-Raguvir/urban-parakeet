"""
   Testing module to evaluate the performance of the implemented hangman-bot
   against a given list of words.
"""

from hangman import play, getWords

words = getWords('words.txt')
score,i = 0,0
n = len(words)

for word in words[0:n]:
    score += play(word,True)
    i += 1
    if i % 1000 == 0: print "Completed %d words" % (i)

print "\nNumber of games won: %d" % (score)
print "Number of games lost: %d" % (n - score)
print "Success percentage: %.4f\n"%((score/float(n))*100)