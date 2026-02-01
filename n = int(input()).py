n = int(input())
num = list(map(int,input().split()))
num.sort()
maxx = 1;
cnt = 1;
ans = num[0]
for i in range (1,n):
    if num[i] == num[i-1]:
        cnt +=1
    else:
        if cnt>maxx:
            maxx = cnt
            ans = num[i-1]
        elif cnt == maxx and num[i-1] < ans:
            ans = num[i-1]
        cnt = 1

if cnt > maxx:
    ans = num[n-1]
elif cnt == maxx and num[n-1]<ans:
    ans = num[n-1]
print(ans)
