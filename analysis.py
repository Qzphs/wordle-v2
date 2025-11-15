"""Local script to perform analysis command without discord bot."""

from domain.analysis import analysis


words = input("enter words: ").split()
print(analysis(words))
