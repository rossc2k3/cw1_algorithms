
# File:     timsort.py
# Author:   John Longley
# Date:     October 2022

# Template file for Inf2-IADS (2022-23) Coursework 1, Part A
# Simplified version of Timsort sorting algorithm




# Provided code for splitting list into suitable segments

# Tags for segment types:

Inc, Dec, Unsorted = +1, -1, 0

# Representing segments (L[start],...,L[end-1]):

class Segment:
    def __init__(self,start,end,tag):
        self.start = start
        self.end = end
        self.tag = tag
    def len(self):
        return self.end - self.start
    def __repr__(self):
        return ('Segment('+str(self.start)+','+str(self.end)+','
                +str(self.tag)+')')

# Stage 1: Split entire list into Inc and Dec segments (possibly very short).

class IncDecRuns:
    def __init__(self,L,key=lambda x:x):
        self.L = L
        self.key = key
        self.m = len(L)-1
        self.dir = Inc if key(L[1]) >= key(L[0]) else Dec
        self.i = 0  # most recent segment boundary
        self.j = 0  # position reached
    def next(self):
        # returns tuple for next segment, or None if end reached
        if self.j == self.m:
            return None
        else:
            self.i = self.j
            # scan for next change of direction
            while (self.j < self.m and
                   ((self.dir == Inc and
                     self.key(self.L[self.j]) <= self.key(self.L[self.j+1])) or
                    (self.dir == Dec and
                     self.key(self.L[self.j]) >= self.key(self.L[self.j+1])))):
                self.j+=1
            if self.j == self.m:
                # no change of direction at final step: include last list entry
                return Segment(self.i, self.m+1, self.dir)
            else:
                # change of direction
                self.dir = -self.dir
                return Segment(self.i, self.j, -self.dir)
    def finished(self):
        return (self.j == self.m)
            
# Stage 2: Fuse consecutive short segments into longer (unsorted) ones.

# Preserve all Inc or Dec runs of at least this size:
runThreshold = 32

class FuseSegments:
    def __init__(self,IncDecRuns):
        self.IDR = IncDecRuns
        self.next1 = self.IDR.next()
        self.next2 = self.IDR.next()
    def next(self):
        if self.next2 == None:
            curr = self.next1
            self.next1 = None
            return curr
        elif self.next1.len() < runThreshold and self.next2.len() < runThreshold:
            # two short segments: fusing required
            start = self.next1.start
            # find end of run of short segments
            while self.next2.len() < runThreshold and not self.IDR.finished():
                self.next2 = self.IDR.next()
            if self.next2.len() < runThreshold:
                # next2 is last segment and is short: include in fused segment
                end = self.next2.end
                self.next1, self.next2 = None, None
            else:
                # next2 is long: exclude from fused segment
                end = self.next2.start
                self.next1 = self.next2
                self.next2 = self.IDR.next()
            return Segment(start, end, Unsorted)
        else:
            # long or isolated short segment: return unchanged
            curr = self.next1
            self.next1 = self.next2
            self.next2 = self.IDR.next()
            return curr
    def finished(self):
        return (self.next1 == None)

# Stage 3: Split long unsorted segments into ones of length in range
# blockMin,...,blockMax (suitable for InsertSort).
# Return a list of all segments.

blockMin = 32
blockMax = 63  # require blockMax >= blockMin*2+1

def segments(L):
    FS = FuseSegments(IncDecRuns(L))
    S = []
    curr = FS.next()
    while curr != None:
        if curr.len() == 1 and len(S) >= 1 and not FS.finished():
            # drop this segment, just tag extra element onto previous one
            S[-1].end += 1
        elif curr.tag != Unsorted or curr.len() <= blockMax:
            # keep segment as is
            S.append(curr)
        else:
            # split long unsorted segment into blocks
            start = curr.start
            n = curr.len()
            k = n // blockMin
            divs = [start+(n*i)//k for i in range(k+1)]
            for i in range(k):
                S.append(Segment(divs[i],divs[i+1],0))
        curr = FS.next()
    return S

# TODO: Task 1.
def insertSort(L,start,end,key=lambda x:x):
    for listPos in range(start, end):    #cookie cutter insertsort taken from slides
        swap = L[listPos]
        prev = listPos - 1
        while(prev >= start and key(L[prev]) > key(swap)):
            L[prev + 1] = L[prev]
            prev = prev - 1
        L[prev + 1] = swap

def reverse(L,start,end):
    while(start < end):  #we only want to run for 1/2 the length of the list, simulataneously increment and decrement start and end respectively
        end -= 1
        L[start], L[end] = L[end], L[start] #swap start with end, start+1 with end-1, etc
        start += 1

def processSegments(L,segs,key=lambda x:x):
    for listPos in range(len(segs)):  #runs for amount of segments there are
        if segs[listPos].tag == 0:    #if unsorted, insert sort
            insertSort(L, segs[listPos].start, segs[listPos].end, key)
        elif segs[listPos].tag == -1: #if in reverse order, reverse it
            reverse(L, segs[listPos].start, segs[listPos].end)
                                      #don't need to do anything if sorted

# TODO: Task 2.
def mergeSegments(L,seg1,seg2,M,start,key=lambda x:x):
   processSegments(L, [seg1, seg2])         #saves some runtime if either of the segments need sorted
   insertSort(L, seg1.start, seg2.end, key) #this works since we're working with adjacent segments, but wouldn't work if we were sorting nonadjacent segments
   for listPos in range(seg1.start, seg2.end):
       M[start + listPos] = L[seg1.start + listPos] #standard code for transplanting one list's content to another using inplace
   return (seg2.end - seg1.start)



def copySegment(L,seg,M,start):
    for listPos in range(seg.start, seg.end):
        M[start + listPos] = L[seg.start + listPos] #standard code for transplanting one list's content to another using inplace
    return (seg.end - seg.start)



# TODO: Task 3.
def mergeRound(L,segs,M,key=lambda x:x):
    for listPos in range(len(segs) // 2):
        mergeSegments(L, segs[listPos], segs[listPos + 1], M, segs[listPos].start, key)
    if len(segs) // 2 == 1:
        copySegment(L, segs[-1], M, segs[-1].start)
    segs = segments(M)
    return segs
        
def mergeRounds(L,segs,M,key=lambda x:x):
    if len(segs) > 1: #inital run, meaning if only two segments, only have to run once - if more than 2, move into while loop
        segs = mergeRound(L, segs, M, key)
    while len(segs) > 1:
        segs = mergeRound(M, segs, L, key) #if still more than 1 segment, run again
        if len(segs) > 1:
            segs = mergeRound(L, segs, M, key)

    return L
        


# Provided code:

def SimpleTimSort(L,key=lambda x:x):
    if len(L) <= 1:
        return L
    else:
        segs = segments(L)
        processSegments(L,segs,key)
        M = [None] * len(L)
        return mergeRound(L,segs,M,key)

# End of file
