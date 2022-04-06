

def Binerysort(arr):
    l = len(arr)
    if l == 0 and l ==1:
        return 0
    mid = l//2
    out1 = Binerysort(arr[0:mid])
    out2 = Binerysort(arr[mid:])

    print('OUT1 :',out1)
    print('OUT1 :', out2)
    return out

def bineryserch(arr):


arr = [2,5,7,8,18,12,23,27,24,19,45,51,22]

out = Binerysort(arr)

