#!/usr/bin/env python

class AppendRecord:
    lookup = lambda x: x
    gen = None
    
    def __init__(self, generator, lookupFunction):
        self.gen = generator
        self.lookup=lookupFunction

    def process(self):
        for record in self.gen():
            record.append(self.lookup(record[0]))
            yield record
