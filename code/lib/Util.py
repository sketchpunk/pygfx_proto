import pygfx as gfx


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
