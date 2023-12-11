fakeInputs = [
    "login",
    "Lionel.M",
    "2977",
    "4",
    "1",
    "login",
    "Lionel.M",
    "2977",
    "3",
    "create",
    
];
fakeInputIdx = 0
realInput = input
def fakeInput(text):
    global fakeInputIdx;
    if fakeInputIdx >= len(fakeInputs):
        return realInput(text);
    ret = fakeInputs[fakeInputIdx];
    print(text + ret)
    fakeInputIdx += 1;
    return ret;
import builtins
setattr(builtins, 'input', fakeInput)

import project_manage