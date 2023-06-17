const a = [2, 1, 3, 5, 3, 2]

solution = (a) => {
    r = new Set()
    for (e of a)
        if (r.has(e))
            return e
        else
            r.add(e)
    return -1
}

console.log(solution(a))