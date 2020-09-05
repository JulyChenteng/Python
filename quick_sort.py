def partion2(nums,left,right):
    '''
    选取第一个作为主元，从两边进行遍历
    '''
    p = nums[left]
    i = left
    j = right
    while i<j:
        #向左遍历扫描，遇到比主元小的元素停止
        while i < j and nums[j] >= p:
            j -= 1
        nums[i] = nums[j]
        
        #向右遍历扫描，遇到比主元大的元素停止
        while i < j and nums[i] <= p:
            i += 1
        nums[j] = nums[i]

        

        
        # if i >= j:
        #     break
        #temp = nums[j]
        #nums[j] = nums [i]
        #nums[i] = temp
    

    #nums[left] = nums[j]
    nums[j] = p
    return j

def quicksort(nums,left,right):
    if left < right:
        mid = partion2(nums,left,right)
        nums = quicksort(nums,left,mid -1)
        nums = quicksort(nums,mid+1,right)
    return nums




if __name__ == "__main__":
    nums = [4,7,2,1,3,6,5,8,9]
    # print(SelectSort(nums))
    print(quicksort(nums,0,len(nums)-1))