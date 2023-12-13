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
    "Automatic Recycle Bin",
    "Create a recycle bin that automatically recycles stuff inside.",
    "5",
    "Manuel.N", # Manuel.N
    "5",
    "5687866", # Robert.L,8176
    "6",
    "2567260", # Paulo.D
    "1",
    "3",
    "0",
    "1",
    "1",
    "login",
    "Manuel.N",
    "1244",
    "2",
    "0",
    "y",
    "exit",
    "3",
    "1",
    "login",
    "Robert.L",
    "8176",
    "2",
    "0",
    "n",
    "exit",
    "3",
    "1",
    "login",
    "Paulo.D",
    "1312",
    "2",
    "0",
    "y",
    "1",
    "login",
    "Lionel.M",
    "2977",
    "3",
    "0",
    "6",
    "1",
    "1",
    "login",
    "Paulo.D",
    "1312"

];
fakeInputIdx = 0
realInput = input
def fakeInput(text):
    global fakeInputIdx;
    if fakeInputIdx >= len(fakeInputs):
        setattr(builtins, 'input', realInput)
        return realInput(text);
    ret = fakeInputs[fakeInputIdx];
    print(text + ret)
    fakeInputIdx += 1;
    return ret;
import builtins
setattr(builtins, 'input', fakeInput)

import project_manage