#!/usr/bin/env python

import string

class MyIO:
    headers = []
    hasWritten = False
 
    def readCSV(self, stream):
        self.headers = [h.strip() for h in string.split(next(stream), ",")]
        
        for line in stream:
            line = line.strip()
            #mac = "or ".join(func(line))
            #yield [line, mac]
            yield [line.strip()]

    def escapeRecords(self, records):
        return [ "" if record is None else
                "\"%s\"" % record if "," in record else
                record for record in records]

    def writeCSV(self, records):
        if records is not None:
            if not self.hasWritten:
                self.hasWritten = True
                self.writeCSV(self.headers)
            escapedRecords = self.escapeRecords(records) 
            if escapedRecords is not None:
                print ",".join(escapedRecords)
