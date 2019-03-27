#!/usr/bin/env python3
import argparse
import csv

# get arguments
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--periodic_table_csv', required=True,
  help="provided CSV file of atomic info")
parser.add_argument('-w', '--wordlist_csv', required=True,
  help="provided CSV file of words")
args = parser.parse_args()

# create hash-set of element symbols
pt_set = set()
with open(args.periodic_table_csv, newline='') as pt_csv:
  reader = csv.DictReader(pt_csv)
  for row in reader:
    pt_set.add(row['Symbol'])

# period set's complete, right?
assert (len(pt_set) == 118), \
  "Wrong number of elements; found {} but require 118".format(len(pt_set))

# get word list
word_list = []
with open(args.wordlist_csv, newline='') as wl_csv:
  word_list = wl_csv.read().splitlines() 

class Periodicize:
  # take word fragment, check for symbols, add to result, tail-recurse
  def process(self, remains, so_far=""):
    pt = Periodicize.pt
    if not remains:
      self.solutions.append(so_far)
    else:
      frag1 = remains[0].capitalize()
      if frag1 in pt:
        self.process(remains[1:], so_far + frag1)
      if len(remains) > 1:
        frag2 = remains[:2].capitalize()
        if frag2 in pt:
          self.two = self.process(remains[2:], so_far + frag2)

  def __init__(self, word, pt):
    Periodicize.pt = pt
    self.solutions = []
    self.process(word)
  
  # default heuristic for picking from possibilities
  @staticmethod
  def fewest_elements(solns):
    # https://en.wikipedia.org/wiki/Longest_word_in_English)
    min = 200000
    minword = "HEY THIS IS WRONG"
    for word in solns:
      count = 0
      for i in range(len(word)):
        if word[i].isupper():
          count += 1
      if count < min:
        min = count
        minword = word
    return minword

  def solution(self, heuristic=None):
    if not heuristic:
      heuristic = Periodicize.fewest_elements
    return heuristic(self.solutions)

for word in word_list:
  print("Word: {}\tPeriodicized: {}".format(word, Periodicize(word, pt_set).solution()))
