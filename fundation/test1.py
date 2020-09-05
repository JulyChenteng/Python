def stringPowerSet(strs):
    N = len(strs)
    res = []
    for i in range(2 ** N):
        temp = ""
        for j in range(N):
           # print('i', i)
           # print('j', j)
           # print('i>>j', i >> j)
            if (i >> j) % 2:
                #print(strs[j])
                temp += strs[j]
        res.append(temp)
    return res

if __name__ == '__main__':
    print(stringPowerSet("abcde"))