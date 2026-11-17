"""Proportional humanoid, hand-keyed walk cycle, side-view renders. Style "outfit" = low-poly blocks coloured like
the sheet; "neutral" = plain grey artist's mannequin with ball joints. Far-side limbs are darker in both.
N_FRAMES 0 renders a single front-view T-pose instead of the walk.
usage: blender -b --python mannequin.py -- OUT_DIR [N_FRAMES] [outfit|neutral]"""
import bpy, json, math, sys
from bpy_extras.object_utils import world_to_camera_view
from pathlib import Path
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
OUT = Path(argv[0]); OUT.mkdir(parents=True, exist_ok=True)
N = int(argv[1]) if len(argv) > 1 else 8
STYLE = argv[2] if len(argv) > 2 else "outfit"

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

SKIN = (0.93, 0.74, 0.64, 1); HAIR = (0.17, 0.12, 0.10, 1); JACKET = (0.36, 0.24, 0.18, 1)
TOP = (0.93, 0.60, 0.33, 1); SHORTS = (0.13, 0.10, 0.09, 1); SOCK = (0.20, 0.20, 0.21, 1)
BOOT = (0.33, 0.22, 0.15, 1)


def joint(name, parent, loc):
    e = bpy.data.objects.new(name, None)
    scene.collection.objects.link(e)
    e.parent = parent
    e.location = loc
    return e


def seg(name, parent, length, r_top, r_bot, color, depth_scale=1.0, offset=(0, 0, 0)):
    bpy.ops.mesh.primitive_cone_add(vertices=12 if STYLE == "outfit" else 32, radius1=r_bot, radius2=r_top, depth=length)
    o = bpy.context.object
    o.name = name
    o.parent = parent
    o.location = Vector(offset) + Vector((0, 0, -length / 2))
    o.scale = (depth_scale, 1, 1)
    o.color = color
    return o


def box(name, parent, size, loc, color):
    bpy.ops.mesh.primitive_cube_add(size=1)
    o = bpy.context.object
    o.name = name
    o.parent = parent
    o.location = loc
    o.scale = size
    o.color = color
    return o


root = joint("root", None, (0, 0, 0.88))


def ball(name, parent, r, loc, color, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=r)
    o = bpy.context.object
    o.name = name
    o.parent = parent
    o.location = loc
    o.scale = scale
    o.color = color
    return o


def build_neutral():
    body, near_c, far_c = (0.72, 0.72, 0.74, 1), (0.86, 0.86, 0.88, 1), (0.38, 0.38, 0.41, 1)
    seg("hips", root, 0.16, 0.15, 0.13, body, 0.75, (0, 0, 0.08))
    waist = joint("waist", root, (0, 0, 0.08))
    seg("belly", waist, 0.12, 0.12, 0.14, body, 0.7, (0, 0, 0.12))
    chest = joint("chest", waist, (0, 0, 0.10))
    seg("ribs", chest, 0.30, 0.17, 0.13, body, 0.68, (0, 0, 0.30))
    neck = joint("neck", chest, (0, 0, 0.32))
    seg("neckseg", neck, 0.08, 0.045, 0.05, body, 1.0, (0, 0, 0.08))
    head = joint("head", neck, (0.01, 0, 0.07))
    ball("skull", head, 0.105, (0.01, 0, 0.11), body, (1.0, 0.88, 1.15))
    ball("jaw", head, 0.06, (0.06, 0, 0.05), body, (1.0, 1.0, 0.9))
    ball("nose", head, 0.018, (0.115, 0, 0.10), body)
    legs, arms = {}, {}
    for side, y in (("L", 0.085), ("R", -0.085)):
        c = near_c if side == "R" else far_c
        hip = joint(f"hip{side}", root, (0, y, 0))
        ball(f"hipball{side}", hip, 0.075, (0, 0, 0), c)
        seg(f"thigh{side}", hip, 0.40, 0.08, 0.055, c, offset=(0, 0, -0.02))
        knee = joint(f"knee{side}", hip, (0, 0, -0.43))
        ball(f"kneeball{side}", knee, 0.05, (0, 0, 0), c)
        seg(f"shin{side}", knee, 0.38, 0.055, 0.038, c, offset=(0, 0, -0.01))
        ankle = joint(f"ankle{side}", knee, (0, 0, -0.41))
        ball(f"ankleball{side}", ankle, 0.035, (0, 0, 0), c)
        ball(f"foot{side}", ankle, 0.12, (0.05, 0, -0.04), c, (1.0, 0.38, 0.32))
        legs[side] = (hip, knee, ankle)
        sh = joint(f"shoulder{side}", chest, (0, y * 1.9, 0.27))
        ball(f"shoulderball{side}", sh, 0.06, (0, 0, 0), c)
        seg(f"upperarm{side}", sh, 0.26, 0.055, 0.045, c, offset=(0, 0, -0.01))
        elbow = joint(f"elbow{side}", sh, (0, 0, -0.28))
        ball(f"elbowball{side}", elbow, 0.042, (0, 0, 0), c)
        seg(f"forearm{side}", elbow, 0.22, 0.045, 0.035, c, offset=(0, 0, -0.01))
        wrist = joint(f"wrist{side}", elbow, (0, 0, -0.24))
        ball(f"hand{side}", wrist, 0.05, (0.005, 0, -0.05), c, (0.65, 0.45, 1.0))
        ball(f"thumb{side}", wrist, 0.018, (0.035, 0, -0.035), c, (1.0, 1.0, 1.6))
        arms[side] = (sh, elbow)
    for o in scene.objects:
        if o.type == "MESH":
            for poly in o.data.polygons:
                poly.use_smooth = True
    return chest, head, legs, arms


def build_outfit():
    seg("hips", root, 0.16, 0.15, 0.13, SHORTS, 0.75, (0, 0, 0.08))
    waist = joint("waist", root, (0, 0, 0.08))
    seg("belly", waist, 0.10, 0.12, 0.14, SKIN, 0.7, (0, 0, 0.10))
    chest = joint("chest", waist, (0, 0, 0.10))
    seg("top", chest, 0.18, 0.15, 0.13, TOP, 0.72, (0, 0, 0.18))
    seg("jacket", chest, 0.36, 0.20, 0.17, JACKET, 0.62, (-0.015, 0, 0.32))
    neck = joint("neck", chest, (0, 0, 0.32))
    seg("neckseg", neck, 0.07, 0.045, 0.05, SKIN, 1.0, (0, 0, 0.07))
    head = joint("head", neck, (0.01, 0, 0.07))
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.105)
    h = bpy.context.object; h.name = "skull"; h.parent = head; h.location = (0.03, 0, 0.10); h.scale = (1.0, 0.9, 1.12); h.color = SKIN
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.12)
    hr = bpy.context.object; hr.name = "hair"; hr.parent = head; hr.location = (-0.04, 0, 0.15); hr.scale = (0.95, 0.95, 0.95); hr.color = HAIR
    box("hair_back", head, (0.10, 0.20, 0.20), (-0.07, 0, 0.0), HAIR)
    box("nose", head, (0.03, 0.025, 0.03), (0.115, 0, 0.09), SKIN)

    LEGS, ARMS = {}, {}
    for side, y in (("L", 0.085), ("R", -0.085)):
        near = side == "R"
        c = (lambda col: col) if near else (lambda col: tuple(x * 0.5 for x in col[:3]) + (1,))
        hip = joint(f"hip{side}", root, (0, y, 0))
        seg(f"thigh_short{side}", hip, 0.16, 0.085, 0.075, c(SHORTS))
        seg(f"thigh_skin{side}", hip, 0.10, 0.07, 0.065, c(SKIN), offset=(0, 0, -0.16))
        seg(f"thigh_sock{side}", hip, 0.17, 0.066, 0.055, c(SOCK), offset=(0, 0, -0.26))
        knee = joint(f"knee{side}", hip, (0, 0, -0.43))
        seg(f"shin{side}", knee, 0.30, 0.055, 0.042, c(SOCK))
        seg(f"boot{side}", knee, 0.13, 0.058, 0.055, c(BOOT), offset=(0, 0, -0.30))
        ankle = joint(f"ankle{side}", knee, (0, 0, -0.41))
        box(f"foot{side}", ankle, (0.24, 0.10, 0.07), (0.05, 0, -0.035), c(BOOT))
        LEGS[side] = (hip, knee, ankle)
        sh = joint(f"shoulder{side}", chest, (0, y * 2.0, 0.27))
        seg(f"upperarm{side}", sh, 0.28, 0.065, 0.055, c(JACKET))
        elbow = joint(f"elbow{side}", sh, (0, 0, -0.28))
        seg(f"forearm{side}", elbow, 0.24, 0.058, 0.05, c(JACKET))
        wrist = joint(f"wrist{side}", elbow, (0, 0, -0.24))
        box(f"hand{side}", wrist, (0.06, 0.035, 0.09), (0, 0, -0.045), c(SKIN))
        ARMS[side] = (sh, elbow)

    return chest, head, LEGS, ARMS


chest, head, LEGS, ARMS = build_neutral() if STYLE == "neutral" else build_outfit()


def pose(t):
    root.location.z = 0.88
    for side, ph in (("R", 0.0), ("L", math.pi)):
        p = 2 * math.pi * t + ph
        thigh = 24 * math.sin(p)
        knee = 6 + 40 * max(0.0, math.cos(p)) ** 1.6
        hip, kn, an = LEGS[side]
        hip.rotation_euler.y = -math.radians(thigh)
        kn.rotation_euler.y = math.radians(knee)
        an.rotation_euler.y = math.radians(thigh - knee) * 0.85
        sh, el = ARMS[side]
        sh.rotation_euler.y = -math.radians(-20 * math.sin(p))
        el.rotation_euler.y = -math.radians(18 + 10 * max(0.0, -math.sin(p)))
    chest.rotation_euler.y = -math.radians(3)
    head.rotation_euler.y = math.radians(3)
    bpy.context.view_layer.update()
    low = min((o.matrix_world @ Vector(c)).z for o in scene.objects if o.name.startswith("foot") for c in o.bound_box)
    root.location.z -= low
    bpy.context.view_layer.update()


cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
scene.collection.objects.link(cam)
cam.data.type = "ORTHO"
cam.data.ortho_scale = 2.1
cam.location = (0.05, -5, 0.86)
cam.rotation_euler = (math.pi / 2, 0, 0)
scene.camera = cam

scene.render.engine = "BLENDER_WORKBENCH"
scene.display.shading.light = "FLAT" if STYLE == "outfit" else "STUDIO"
scene.display.shading.color_type = "OBJECT"
scene.display.shading.show_cavity = False
scene.render.resolution_x, scene.render.resolution_y = 768, 1024
scene.view_settings.view_transform = "Standard"
scene.world = bpy.data.worlds.new("w")
scene.world.color = (1, 1, 1)
scene.display.shading.background_type = "WORLD"

if N == 0:
    for side, ang in (("L", 88), ("R", -88)):
        ARMS[side][0].rotation_euler.x = math.radians(ang)
        ARMS[side][1].rotation_euler.y = -math.radians(5)
    bpy.context.view_layer.update()
    low = min((o.matrix_world @ Vector(c)).z for o in scene.objects if o.name.startswith("foot") for c in o.bound_box)
    root.location.z -= low
    cam.location = (5, 0, 0.86)
    cam.rotation_euler = (math.pi / 2, 0, math.pi / 2)
    scene.render.resolution_x = 1024
    scene.render.filepath = str(OUT / "tpose.png")
    bpy.ops.render.render(write_still=True)
hands = []
for i in range(N):
    pose(i / N)
    hands.append({s: list(world_to_camera_view(scene, cam, scene.objects[f"hand{s}"].matrix_world.translation))[:2] for s in "LR"})
    scene.render.filepath = str(OUT / f"frame_{i:02d}.png")
    bpy.ops.render.render(write_still=True)
(OUT / "hands.json").write_text(json.dumps(hands))
print("done", N)
