# Distance Between Strings
# 
# Let's define the 'distance' between 2 strings as the number of changes required to turn the first string into the second string.
# A change could be the insertion of a character, the deletion of a character, or changing the value of some position.
# Write a function (in the least number of characters possible)that returns the distance between 2 strings a and b.
# 
# Sample Case
# 
# Input: "codegolf", "cmdgoleef"
# 
# Output: 4

import functools
@functools.cache
def solve(a,b):
 if len(a)==0:return len(b)
 if len(b)==0:return len(a)
 if a[0]==b[0]:return solve(a[1:],b[1:])
 return min(1+solve(a,b[1:]),1+solve(a[1:],b),1+solve(a[1:],b[1:]))

214

import functools as f
@f.cache
def s(a,b,l=len):
 if l(a)<1:return l(b)
 if l(b)<1:return l(a)
 if a[0]==b[0]:return s(a[1:],b[1:])
 return min(1+s(a,b[1:]),1+s(a[1:],b),1+s(a[1:],b[1:]))
solve=s

import functools as f
def s(a,b,l=len):
 if l(a)<1:return l(b)
 if l(b)<1:return l(a)
 if a[0]==b[0]:return s(a[1:],b[1:])
 return min(1+s(a,b[1:]),1+s(a[1:],b),1+s(a[1:],b[1:]))
solve=f.cache(s)


195

import functools as f
@f.cache
def s(a,b,l=len):return l(a)if l(b)<1 else l(b)if l(a)<1 else[s(a[1:],b[1:]),min(1+s(a,b[1:]),1+s(a[1:],b),1+s(a[1:],b[1:]))][a[0]!=b[0]]
solve=s

177

import functools as f
@f.cache
def s(a,b,l=len):return l(a)if l(b)<1 else l(b)if l(a)<1 else[s(a[1:],b[1:]),min(1+s(a,b[1:]),1+s(a[1:],b),1+s(a[1:],b[1:]))][a[0]!=b[0]]
solve=s

