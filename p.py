dishes = [["Salad","Tomato","Cucumber","Salad","Sauce"], 
 ["Pizza","Tomato","Sausage","Sauce","Dough"], 
 ["Quesadilla","Chicken","Cheese","Sauce"], 
 ["Sandwich","Salad","Bread","Tomato","Cheese"]]

def solution(dishes):
    groups = {}
    for d, *v in dishes:
        for x in v:
            groups.setdefault(x, []).append(d)
    ans = []
    for x in sorted(groups):
        if len(groups[x]) >= 2:
            ans.append([x] + sorted(groups[x]))
    return ans

print(solution(dishes))