class Solution:

def findPeakElement(self, num):
    if len(num)==0: return None
    if len(num)==1: return 0
    return self.findPeakHelper(num,0,len(num)-1)
def findPeakHelper(self,num,start,end):
    mid = (start+end)/2
    if mid>start and mid < end:
        if(num[mid-1]<num[mid] and num[mid]>num[mid+1]):
            return mid
        if(num[mid-1]>num[mid]):
            return self.findPeakHelper(num,start,mid)
        else:
            return self.findPeakHelper(num,mid,end)
    else:
        if num[mid]>num[mid+1]:
            return mid
        else:return mid+1