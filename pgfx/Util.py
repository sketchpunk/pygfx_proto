import inspect
import pygfx as gfx
import threading

# region OBJECT HIERARCHY


# Search scene graph looking for the first object that passes the check lambda
def findFirst(root, fn=lambda o: isinstance(o, gfx.objects.SkinnedMesh)):
    if fn(root):
        return root

    stack = list(root.children)

    while stack:
        o = stack.pop()
        if fn(o):
            return o
        else:
            if o.children:
                stack.extend(o.children)

    return None


# endregion


# region SKELETON


# When loading animations from a different file then the
# character there is an issue where clip tracks are bound
# to the skeleton in the animation file. To make the
# animation work on the character, need to hack the clip
# to swop out bone references to the skeleton that will
# drive the character model
def swopClipSkeleton(clip, skel):
    # Map bone names for the skeleton to target to
    map = {}
    for b in skel.bones:
        map[b.name] = b

    # Loop tracks and swop bones from animation skeleton
    # to the character skeleton
    for t in clip.tracks:
        if t.target.name in map:
            print(f"Found Bone {t.target.name}")
            t.target = map[t.target.name]
        else:
            print(f"Bone not found {t.target.name}")


# Get the first skeleton in gltf
def getGltfSkeleton(gl):
    mesh = findFirst(gl.scene, lambda x: isinstance(x, gfx.objects.SkinnedMesh))
    if mesh:
        return mesh.skeleton
    return None


# endregion


# region DEBUGGING DATA
def inspectObj(obj, showUnderScores=False):
    print(f"INSPECT OBJECT :: {obj.__class__.__name__}")
    for name, member in inspect.getmembers(obj):
        if not showUnderScores and name.startswith("_"):
            continue
        print(f"  {name} : {type(member)}")


def dirObj(obj):
    print(f"DIR OBJECT :: {obj.__class__.__name__}")
    for attr_name in dir(obj):
        if not attr_name.startswith("__"):  # Exclude "dunder" methods
            print(f"  {attr_name}")


def varObj(obj):
    print(f"VAR OBJECT :: {obj.__class__.__name__}")
    # for attr_name, attr_value in vars(obj).items():
    for attr_name, attr_value in obj.__dict__.items():
        print(f"  {attr_name} : {attr_value}")


def printDict(d):
    for k, v in d.items():
        print(f"Key: {k}\n-- Value: {v}")


# endregion


# region MAIN


# Recreating Javascript's setTimeout functionality
def setTimeout(min, fn):
    timer = threading.Timer(min, fn)
    timer.start()


# endregion
