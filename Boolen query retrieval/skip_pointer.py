from timeit import default_timer as timer
import math
def read_index(text):
    global d1
    d1=dict()
    with open(text,"rb") as f:
        for line in f:
            line=line.decode('utf-8')
            line=line.split()
            if line[0] not in d1:
                d1[line[0]]=list()
                d1[line[0]].append(int(line[1]))
            else:
                d1[line[0]].append(int(line[1]))
    sum_len_post=sum([len(d1[term]) for term in d1])
    return len(d1),sum_len_post

#read_index("index.txt")

def size_without_stopword(text):
    l2=list()
    a = sorted(d1.items(),key=lambda x:len(x[1]),reverse=True)
    original=0
    for i,item in enumerate(a):
        if i<10:
            l2.append(item[1])
            original+=len(item[1])
        else:
            break
    return read_index(text)[1]-original+len(set(sum(l2,[])))

def retrieval(term):
    return d1[term] 

def intersection(p1,p2):
    answer,i,j,comparison=[],0,0,0
    start=timer()
    while i< len(p1) and j< len(p2):
        if p1[i] == p2[j]:
            answer.append(p1[i])
            i,j=i+1,j+1
        elif p1[i] < p2[j]:
            i += 1
        else:
            j += 1
        comparison += 1
    end=timer()
    print(end-start)
    return answer,comparison
    
def intersection_multiple(query):
    d3=dict()
    query_list=query.split()
    term_list=[term for term in query_list if term != "AND"]
    if len(term_list)==2:
         result, total_comparison = intersection(d1[term_list[0]], d1[term_list[1]])
    else:
        for term in term_list:
            d3[term]=len(d1[term])
        b=sorted(d3.items(),key=lambda x:x[1])
        final_term_list=[item[0] for item in b]
        result=d1[final_term_list[0]]
        i=1
        total_comparison=0
        while i<len(final_term_list):
            result,comparison=intersection(result,d1[final_term_list[i]])
            total_comparison += comparison
            i += 1
        return result,total_comparison

def place_skip_pointer(p):
    skip_step=int(math.sqrt(len(p)))
    skip_p=[(term,True) if i % skip_step == 0 and i+skip_step<len(p) else (term,False) for i,term in enumerate(p)]
    return skip_p,skip_step


    

def intersection_skipointer(p1,p2):
    answer,i,j,comparison=[],0,0,0
    skip1=int(math.sqrt(len(p1)))
    skip2=int(math.sqrt(len(p2)))
    start=timer()
    while i< len(p1) and j< len(p2):
        if p1[i]== p2[j]:
            answer.append(p1[i])
            i,j=i+1,j+1
        elif p1[i] < p2[j]:
            if i+skip1<len(p1) and p1[i+skip1] < p2[j]:
                while i+skip1<len(p1) and p1[i+skip1] < p2[j]:
                    comparison+=1
                    i=i+skip1
            else:
                i += 1
            comparison+=1
        elif p1[i] > p2[j]:
            if j+skip2<len(p2) and p2[j+skip2]< p1[i]:
                while j+skip2<len(p2) and p2[j+skip2]< p1[i]:
                    comparison+=1
                    j += skip2
            else:
                j += 1
            comparison+=1
        comparison += 1
    end=timer()
    print(end-start)
    return answer,comparison

def intersection_skipointer2(p1,p2):
    answer,i,j,comparison=[],0,0,0
    p1,skip1=place_skip_pointer(p1)
    p2,skip2=place_skip_pointer(p2)
    start=timer()
    while i< len(p1) and j< len(p2):
        if p1[i][0]== p2[j][0]:
            answer.append(p1[i][0])
            i,j=i+1,j+1
        elif p1[i][0] < p2[j][0]:
            if p1[i][1] and p1[i+skip1][0] <= p2[j][0]:
                while p1[i][1] and p1[i+skip1][0] <= p2[j][0]:
                    comparison+=1
                    i=i+skip1
            else:
                i += 1
            comparison+=1
        elif p2[j][1] and p2[j+skip2][0]<= p1[i][0]:
            while p2[j][1] and p2[j+skip2][0]<=p1[i][0]:
                comparison+=1
                j += skip2
        else:
            j += 1
        comparison += 1
    end=timer()
    print(end-start)
    return answer,comparison



def intersection_multiple_skip(query):
    d3=dict()
    query_list=query.split()
    term_list=[term for term in query_list if term != "and"]
    if len(term_list)==2:
        result, total_comparison = intersection(d1[term_list[0]], d1[term_list[1]])
    else:
        for term in term_list:
            d3[term]=len(d1[term])
        b=sorted(d3.items(),key=lambda x:x[1])
        final_term_list=[item[0] for item in b]
        result=d1[final_term_list[0]]
        i=1
        total_comparison=0
        while i<len(final_term_list):
            result,comparison=intersection_skipointer2(result,d1[final_term_list[i]])
            print(result)
            total_comparison += comparison
            i += 1
        return result,total_comparison        
