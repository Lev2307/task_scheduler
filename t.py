s = "pwwkew"
longest = ""
for i in s:
    if i not in longest:
        longest += i
print(longest)
print(len(longest))